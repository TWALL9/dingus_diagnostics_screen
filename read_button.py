#!/usr/bin/env python3

import gpiod
import select
from datetime import datetime, timedelta
import os
import threading
import time

def edge_type_str(event):
    if event.type is event.FALLING_EDGE:
        return "Falling"
    if event.type is event.RISING_EDGE:
        return "Rising"
    return "Unknown"

def watch_line_value(chip_path, offset, done_fd):
    chip = gpiod.Chip(chip_path)
    line = chip.get_line(offset)
    line.request("test", gpiod.LINE_REQ_EV_FALLING_EDGE, gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)
    debounce_ms = timedelta(milliseconds=150)
    last_change = datetime.now()

    poll = select.poll()
    poll.register(line.event_get_fd(), select.POLLIN)
    poll.register(done_fd, select.POLLIN)

    while True:
        for fd, _event in poll.poll():
            if fd == done_fd:
                line.release()
                return
            event = line.event_read()
            now = datetime.now()
            db_time = now - last_change
            if db_time >= debounce_ms:
                print(db_time, " changed:", edge_type_str(event))
            last_change = now


if __name__ == "__main__":
    done_fd = os.eventfd(0)

    def bg_thread():
        try:
            watch_line_value("/dev/gpiochip0", 16, done_fd)
        except OSError as ex:
            print(ex, "\nCustomise the example configuration to suit your situation")
        finally:
            print("exiting")

    t = threading.Thread(target=bg_thread)
    t.start()

    for i in range(0, 20):
        print("asdf:", i)
        time.sleep(1)

    if t.is_alive():
        os.eventfd_write(done_fd, 1)
        t.join()

    os.close(done_fd)
    print("main thread exiting")

#!/usr/bin/env python3

import gpiod
import select
from datetime import datetime, timedelta
import os
import threading

def edge_type_str(event):
    if event.type is event.FALLING_EDGE:
        return "Falling"
    if event.type is event.RISING_EDGE:
        return "Rising"
    return "Unknown"

def watch_line_value(chip_path, offset):
    chip = gpiod.Chip(chip_path)
    line = chip.get_line(offset)
    line.request("test", gpiod.LINE_REQ_EV_BOTH_EDGES, gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)
    debounce_ms = timedelta(milliseconds=250)
    current_edge = None
    last_change = datetime.now()
    while True:
        event = line.event_read()
        now = datetime.now()
        # print(now, edge_type_str(event))
        if current_edge != event.type:
            db_time = now - last_change
            # print(f"{current_edge} -> {event.type}: {db_time}")
            if db_time >= debounce_ms:
                print("\r\n", db_time, " changed:", edge_type_str(event), "\r\n")
            last_change = now
            current_edge = event.type
            

if __name__ == "__main__":
    done_fd = os.eventfd(0)

    watch_line_value("/dev/gpiochip0", 16)
    # try:
    #     watch_line_value("/dev/gpiochip0", 16)
    # except OSError as ex:
    #     print(ex, "\nCustomise the example configuration to suit your situation")

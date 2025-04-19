import gpiod
import select
from datetime import datetime, timedelta
import os
import threading


def _watch_line_value(line, done_fd, user_callback):
    line.request(
        "diag_mode_change",
        gpiod.LINE_REQ_EV_FALLING_EDGE,
        gpiod.LINE_REQ_FLAG_BIAS_PULL_UP,
    )
    line_fd = line.event_get_fd()

    poll = select.poll()
    poll.register(line_fd, select.POLLIN)
    poll.register(done_fd, select.POLLIN)

    debounce_ms = timedelta(milliseconds=150)
    last_change = datetime.now()

    while True:
        for fd, _event in poll.poll():
            if fd == line_fd:
                line.event_read()
                now = datetime.now()
                db_time = now - last_change
                if db_time >= debounce_ms:
                    user_callback(now)
                last_change = now

            if fd == done_fd:
                line.release()
                return


class GpioModeChange:
    def __init__(self, chip_path, offset, user_callback):
        chip = gpiod.Chip(chip_path)
        line = chip.get_line(offset)

        self._done_fd = os.eventfd(0)
        self._gpio_thread = threading.Thread(
            target=_watch_line_value, args=[line, self._done_fd, user_callback]
        )
        self._gpio_thread.start()

    def __del__(self):
        print("releasing GPIO")
        if self._gpio_thread.is_alive():
            os.eventfd_write(self._done_fd, 1)
            self._gpio_thread.join()
        else:
            print("Error, gpio thread is already dead?")
        os.close(self._done_fd)

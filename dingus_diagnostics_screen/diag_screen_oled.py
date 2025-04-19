#!/usr/bin/env python3

import gpiod
import select
from datetime import datetime, timedelta
import os
import threading
import time
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from queue import Queue

import modes
from utils import get_comp_stats


def watch_line_value(chip_path, offset, done_fd, queue: Queue, kill_queue: Queue):
    chip = gpiod.Chip(chip_path)
    line = chip.get_line(offset)
    line.request(
        "test", gpiod.LINE_REQ_EV_FALLING_EDGE, gpiod.LINE_REQ_FLAG_BIAS_PULL_UP
    )
    debounce_ms = timedelta(milliseconds=150)
    last_change = datetime.now()

    poll = select.poll()
    poll.register(line.event_get_fd(), select.POLLIN)
    poll.register(done_fd, select.POLLIN)

    mode = modes.Mode.COMP_STATS

    while True:
        for fd, _event in poll.poll():
            if fd == done_fd:
                line.release()
                kill_queue.put(-1)
                return
            _line_event = line.event_read()
            now = datetime.now()
            db_time = now - last_change
            if db_time >= debounce_ms:
                print("mode change")
                mode = modes.next_mode(mode)
                queue.put(mode)
            last_change = now


def update_screen(mode_queue: Queue, diag_queue: Queue, kill_queue: Queue):
    i2c = busio.I2C(SCL, SDA)
    disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

    disp.fill(0)
    disp.show()

    width = disp.width
    height = disp.height
    image = Image.new("1", (width, height))
    draw = ImageDraw.Draw(image)

    padding = -2
    top = padding
    x = 0
    font = ImageFont.load_default()

    mode = modes.Mode.COMP_STATS
    diag_text = "None?"

    while True:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        if not mode_queue.empty():
            print("next mode")
            mode = mode_queue.get()
        if not diag_queue.empty():
            diag_text = diag_queue.get()
        if not kill_queue.empty():
            return

        lcd_text = []

        if mode == modes.Mode.COMP_STATS:
            lcd_text = get_comp_stats()
        elif mode == modes.Mode.URGENT_DIAGS:
            lcd_text = diag_text
        else:
            lcd_text = ["None?"]

        y_pad = top
        for line in lcd_text:
            draw.text((x, y_pad), line, font=font, fill=255)
            y_pad += 16

        disp.image(image)
        disp.show()
        time.sleep(0.1)


def main(args=None):
    done_fd = os.eventfd(0)
    mode_queue = Queue()
    kill_queue = Queue()

    t = threading.Thread(
        target=watch_line_value,
        args=["/dev/gpiochip0", 16, done_fd, mode_queue, kill_queue],
    )
    t.start()

    diag_queue = Queue()
    t2 = threading.Thread(
        target=update_screen, args=[mode_queue, diag_queue, kill_queue]
    )
    t2.start()

    i = 0
    try:
        # while True:
        while i < 20:
            time.sleep(1)
            print("asdf:", i)
            diag_queue.put(["asdf", str(i)])
            i += 1
    except KeyboardInterrupt:
        pass

    # for i in range(0, 20):
    #     print("asdf:", i)
    #     diag_queue.put(f"asdf\n{i}")
    #     time.sleep(1)

    if t.is_alive():
        os.eventfd_write(done_fd, 1)
        t.join()
        t2.join()

    os.close(done_fd)
    print("main thread exiting")


if __name__ == "__main__":
    main()

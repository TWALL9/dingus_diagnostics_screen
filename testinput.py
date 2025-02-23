#!/usr/bin/env python3
import gpiod

chip = gpiod.Chip("/dev/gpiochip0")
line = chip.get_line(16)
line.request("asdf", gpiod.LINE_REQ_DIR_IN, gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)

while True:
    print(line.get_value())
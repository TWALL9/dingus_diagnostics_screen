#!/usr/bin/env python3

import gpiod

chip = gpiod.Chip("gpiochip0")
led_line = chip.get_line(20)
led_line.request(consumer="myLed", type=gpiod.LINE_REQ_DIR_OUT)

led_line.set_value(0)
led_line.release()

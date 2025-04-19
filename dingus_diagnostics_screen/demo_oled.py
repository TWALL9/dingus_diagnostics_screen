from display_interfaces.smbus_ssd1306.ssd1306 import SSD1306
from render import Canvas
from PIL import ImageFont
import time

from mode_change_interfaces.gpio import GpioModeChange


class Foo:
    def __init__(self):
        self.i = 0

    def user_callback(self, _now):
        self.i += 1


def draw(ssd, text):
    font = ImageFont.load_default()
    with Canvas(ssd) as draw:
        draw.text((0, 0), text, font=font, fill=255)


ssd = SSD1306()

foo = Foo()
gpio = GpioModeChange("/dev/gpiochip0", 16, foo.user_callback)

try:
    while foo.i < 5:
        time.sleep(0.01)
        if foo.i % 2 == 0:
            draw(ssd, "even")
        else:
            draw(ssd, "odd")
except KeyboardInterrupt:
    pass

del gpio

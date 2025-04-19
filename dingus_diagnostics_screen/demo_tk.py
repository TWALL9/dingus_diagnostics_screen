from render import Canvas
from tk_interface_factory import TkMainRoot
from PIL import ImageFont


class Foo:
    def __init__(self):
        self.i = 0

    def user_callback(self, _now):
        self.i += 1


def draw(interface, text):
    font = ImageFont.load_default()
    with Canvas(interface) as draw:
        draw.text((0, 0), text, font=font, fill=255)


foo = Foo()

tk = TkMainRoot()
lcd = tk.create_screen()
button = tk.create_button(foo.user_callback)


def periodic_task():
    if foo.i % 2 == 0:
        draw(lcd, "even")
    else:
        draw(lcd, "odd")
    tk._root.after(10, periodic_task)


periodic_task()

tk.run()

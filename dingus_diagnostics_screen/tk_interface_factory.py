import tkinter as tk

from display_interfaces.tk.lcd_canvas import LcdCanvas

# from dingus_diagnostics_screen.display_interfaces.tk.lcd_canvas import LcdCanvas
from mode_change_interfaces.tk import TkButton


class TkMainRoot:
    def __init__(self):
        self._root = tk.Tk()
        self._root.title("Dingus Diagnostics")
        self._root.geometry("640x480")

    def run(self):
        self._root.mainloop()

    def create_screen(self):
        return LcdCanvas(self._root, 380, 180)

    def create_button(self, user_callback):
        return TkButton(self._root, user_callback)

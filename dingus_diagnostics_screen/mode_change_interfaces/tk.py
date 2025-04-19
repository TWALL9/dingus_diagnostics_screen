import tkinter as tk
from datetime import datetime


class TkButton:
    def __init__(self, root, user_callback):
        self._root = root
        self._button_canvas = tk.Canvas(self._root, width=200, height=200)
        self._button_canvas.pack(pady=20)
        self._circle = self._button_canvas.create_oval(
            50, 50, 150, 150, fill="red", outline="black"
        )
        self._button_canvas.tag_bind(
            self._circle, "<Button-1>", lambda event: user_callback(datetime.now())
        )

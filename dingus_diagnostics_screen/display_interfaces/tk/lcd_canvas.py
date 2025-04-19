import tkinter as tk
from PIL import Image, ImageTk


class LcdCanvas:
    def __init__(self, root, width, height):
        self._root = root
        self._width = width
        self._height = height
        self._line_width = 3
        self._canvas = tk.Canvas(
            self._root,
            width=self._width,
            height=self._height,
            bg="black",
            bd=10,
            relief="sunken",
        )
        self._canvas.pack(pady=20)
        self._canvas.create_rectangle(
            20, 20, self._width, self._height, outline="green", width=self._line_width
        )

    def get_default_image(self):
        return Image.new(
            "RGB", (int(self._width / 2), int(self._height / 2)), color="black"
        )

    def update(self, image):
        tk_image = ImageTk.PhotoImage(image)
        self._canvas.delete("diag")
        self._canvas.create_image(35, 35, anchor=tk.NW, image=tk_image, tags="diag")
        self._image = tk_image

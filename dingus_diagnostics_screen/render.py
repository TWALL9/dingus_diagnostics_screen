from PIL import Image, ImageDraw


class Canvas(object):
    def __init__(self, device):
        self._draw = None
        self._image = device.get_default_image()
        self._device = device

    def __enter__(self):
        self._draw = ImageDraw.Draw(self._image)
        return self._draw

    def __exit__(self, type, value, traceback):
        if type is None:
            self._device.update(self._image)

        del self._draw
        return False

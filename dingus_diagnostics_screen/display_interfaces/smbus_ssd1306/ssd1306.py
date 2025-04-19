from .interface.i2c import I2cInterface
from PIL import Image, ImageDraw


class SSD1306Commands:
    CMD_PREFIX = 0x00
    DATA_PREFIX = 0x40

    MEMORY_MODE = 0x20
    COL_ADDR = 0x21
    PAGE_ADDR = 0x22
    DISABLE_SCROLL = 0x2E
    SET_START_LINE = 0x40
    SET_CONTRAST = 0x81
    SET_CHARGE_PUMP = 0x8D
    SET_SEGMENT_REMAP = 0xA0
    DISPLAY_VRAM = 0xA4
    DISPLAY_FORCE_WHITE = 0xA5
    DISPLAY_NORMAL = 0xA6
    MULTIPLEX_RATIO = 0xA8
    DISPLAY_OFF = 0xAE
    DISPLAY_ON = 0xAF
    SET_COM_SCAN_DIR = 0xC8
    SET_DISPLAY_OFFSET = 0xD3
    SET_DISPLAY_CLK_DIV = 0xD5
    SET_PRECHARGE_PERIOD = 0xD9
    SET_COMPINS = 0xDA
    SET_VCOM_LEVEL = 0xDB
    CONT_RHOR_SCROLL = 0x29
    ACTIVATE_SCROLL = 0x2F


class SSD1306:
    def __init__(self, bus=1, addr=0x3C, width=128, height=64):
        self._bus = I2cInterface(bus, addr)
        self._width = width
        self._height = height
        self._pages = int(self._height / 8)

        self.init_display()

        self._img = Image.new("1", (width, height), 0)
        self._draw = ImageDraw.Draw(self._img)

    def init_display(self):
        self.command(
            SSD1306Commands.DISPLAY_OFF,
            SSD1306Commands.SET_DISPLAY_CLK_DIV,
            0x80,
            SSD1306Commands.MULTIPLEX_RATIO,
            63,
            SSD1306Commands.SET_DISPLAY_OFFSET,
            0,
            SSD1306Commands.SET_START_LINE,
            SSD1306Commands.SET_CHARGE_PUMP,
            0x14,
            SSD1306Commands.MEMORY_MODE,
            0,
            SSD1306Commands.SET_SEGMENT_REMAP,
            SSD1306Commands.SET_COM_SCAN_DIR,
            SSD1306Commands.SET_COMPINS,
            0x12,
            SSD1306Commands.SET_CONTRAST,
            0xFF,
            SSD1306Commands.SET_PRECHARGE_PERIOD,
            0xF1,
            SSD1306Commands.SET_VCOM_LEVEL,
            0x40,
            SSD1306Commands.DISPLAY_VRAM,
            SSD1306Commands.DISPLAY_NORMAL,
            SSD1306Commands.DISPLAY_ON,
        )

    def command(self, *cmd):
        if len(cmd) <= 32:
            self._bus.cmd(SSD1306Commands.CMD_PREFIX, list(cmd))

    def data(self, data):
        for i in range(0, len(data), 32):
            self._bus.cmd(SSD1306Commands.DATA_PREFIX, list(data[i : i + 32]))

    def get_default_image(self):
        return Image.new("1", (self._width, self._height))

    def update(self, image):
        self.command(
            SSD1306Commands.COL_ADDR,
            0x00,
            self._width - 1,
            SSD1306Commands.PAGE_ADDR,
            0x00,
            self._pages - 1,
        )

        pix = list(image.getdata())
        step = self._width * 8
        buf = []
        for y in range(0, self._pages * step, step):
            i = y + self._width - 1
            while i >= y:
                byte = 0
                for n in range(0, step, self._width):
                    byte |= (pix[i + n] & 0x01) << 8
                    byte >>= 1

                buf.append(byte)
                i -= 1

        self.data(buf)

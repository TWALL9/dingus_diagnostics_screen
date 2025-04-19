from smbus2 import SMBus
from .interface import Interface


class I2cInterface(Interface):
    def __init__(self, bus=None, addr=0):
        self._bus = SMBus(bus)
        self._addr = addr

    def cmd(self, mode, args: list):
        self._bus.write_i2c_block_data(self._addr, mode, args)

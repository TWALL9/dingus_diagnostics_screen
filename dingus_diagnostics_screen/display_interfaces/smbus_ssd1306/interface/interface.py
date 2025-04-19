from abc import ABC, abstractmethod


class Interface:
    @abstractmethod
    def cmd(self, cmd, *args):
        pass

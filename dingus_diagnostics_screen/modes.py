from enum import IntEnum


class Mode(IntEnum):
    COMP_STATS = 0
    URGENT_DIAGS = 1


def next_mode(mode) -> Mode:
    if mode == Mode.COMP_STATS:
        mode = Mode.URGENT_DIAGS
    elif mode == Mode.URGENT_DIAGS:
        mode = Mode.COMP_STATS
    return mode

from enum import IntEnum

class Mode(IntEnum):
    COMP_STATS = 0
    URGENT_DIAGS = 1

def next_mode(mode) -> Mode:
    next_mode = mode + 1
    if next_mode not in Mode:
        return Mode.COMP_STATS
    else:
        return Mode(next_mode)

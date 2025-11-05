import evdev
_ec = evdev.ecodes


def is_arrow(code: int):
    arrows = [_ec.KEY_LEFT, _ec.KEY_UP, _ec.KEY_DOWN, _ec.KEY_RIGHT]
    return code in arrows


def is_shift(code: int):
    return code == _ec.KEY_LEFTSHIFT or code == _ec.KEY_RIGHTSHIFT


def is_ctrl(code: int):
    return code == _ec.KEY_LEFTCTRL or code == _ec.KEY_RIGHTCTRL


def is_alt(code: int):
    return code == _ec.KEY_LEFTALT or code == _ec.KEY_RIGHTALT


def is_meta(code: int):
    return code == _ec.KEY_LEFTMETA or code == _ec.KEY_RIGHTMETA


def is_space(code: int):
    return code == _ec.KEY_SPACE

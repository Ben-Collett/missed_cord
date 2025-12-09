def is_arrow(name: str):
    arrows = ["left", "down", "up", "right"]
    return name in arrows


def is_shift(name: str):
    return name == "shift"


def is_ctrl(name: str):
    return name == "ctrl"


def is_alt(name: str):
    return name == "alt"


def is_meta(name: str):
    return name == "windows"


def is_space(name: str):
    return name == "space"

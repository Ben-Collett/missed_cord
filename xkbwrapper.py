import ctypes
from ctypes import c_int, c_char_p


class XKBKeyLookup(ctypes.Structure):
    _fields_ = [
        ("keycode", ctypes.c_int),
        ("modifiers", ctypes.c_ulong)
    ]


class XKBWrapper:
    def __init__(self, lib_path="./libxkbwrap.so", layout="us"):
        self.lib = ctypes.CDLL(lib_path)

        # Define argument and return types
        self.lib.xkb_init.argtypes = [c_char_p]
        self.lib.xkb_init.restype = c_int

        self.lib.xkb_set_modifiers.argtypes = [c_int, c_int, c_int]
        self.lib.xkb_set_modifiers.restype = None

        self.lib.xkb_translate_key.argtypes = [c_int]
        self.lib.xkb_translate_key.restype = ctypes.c_char_p

        self.lib.xkb_cleanup.argtypes = []
        self.lib.xkb_cleanup.restype = None

        # Initialize C library
        if not self.lib.xkb_init(layout.encode("utf-8")):
            raise RuntimeError("Failed to initialize XKB")

        # Internal modifier states
        self.shift = False
        self.ctrl = False
        self.alt = False

    def __del__(self):
        """Ensure cleanup on object destruction"""
        try:
            self.lib.xkb_cleanup()
        except Exception:
            pass

    # ---- Modifier setters ----
    def setShiftModifier(self, state: bool):
        self.shift = bool(state)
        self._update_modifiers()

    def setCtrlModifier(self, state: bool):
        self.ctrl = bool(state)
        self._update_modifiers()

    def setAltModifier(self, state: bool):
        self.alt = bool(state)
        self._update_modifiers()

    def _update_modifiers(self):
        """Send current modifier state to C side"""
        self.lib.xkb_set_modifiers(
            int(self.shift),
            int(self.ctrl),
            int(self.alt)
        )

    # ---- Key translation ----
    def translateKeycode(self, keycode: int) -> str | None:
        """Translate keycode + modifiers to a Unicode character (if any)"""
        res = self.lib.xkb_translate_key(keycode)
        if not res:
            return None
        out = ctypes.string_at(res).decode("utf-8")
        return out if out else None

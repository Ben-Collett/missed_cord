import evdev
import selectors
# heuristic to help listen to only real keyboards
keyboard_like = {
    evdev.ecodes.KEY_A,
    evdev.ecodes.KEY_Z,
    evdev.ecodes.KEY_1,
    evdev.ecodes.KEY_Q,
}


# WARNING: doesn't register devices grabbed by another program
def _regiseter_devices() -> selectors.DefaultSelector:
    sel = selectors.DefaultSelector()

    # Find all devices that can generate letters and numbers, grabbed devices won't appear
    devices = [
        d for d in map(evdev.InputDevice, evdev.list_devices())
        if evdev.ecodes.EV_KEY in d.capabilities()
        and any(code in d.capabilities()[evdev.ecodes.EV_KEY] for code in keyboard_like)
    ]

    # Register all keyboard-capable devices
    for dev in devices:
        sel.register(dev, selectors.EVENT_READ)
    return sel


def main():
    sel = _regiseter_devices()
    while True:
        for key, _ in sel.select():
            device = key.fileobj
            for event in device.read():
                if event.type == evdev.ecodes.EV_KEY:
                    print(event.code, event.value)


if __name__ == "__main__":
    main()

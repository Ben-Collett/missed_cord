import subprocess
import utils
import evdev
from xkbwrapper import XKBWrapper
from collections import deque
import keyboard_utils
import config


def reverse_dict(d: dict):
    """Reverse the key/value mapping of a dictionary.

    If multiple keys share the same value, the reversed dict maps that value
    to a list of all original keys.
    """
    rev = {}
    for k, v in d.items():
        rev.setdefault(v, []).append(k)
    return rev


def sets_to_string(sets: list[frozenset[str]]) -> list[str]:
    out = []
    for s in sets:
        out.append("")
        for char in s:
            out[-1] += char
    return out


class Event:
    def __init__(self, code, value):
        self.code = int(code)
        self.value = int(value)


def main():
    xkb = XKBWrapper()

    shift_counter = 0
    meta_counter = 0

    json = utils.load_json()
    chords = utils.ascii_only(json)
    reversed_chords = reverse_dict(chords)
    max_output_length = max(map(len, chords.values()))
    queue = deque(maxlen=max_output_length+1)
    backspace_queue = deque()

    probably_chording = False

    prev_chord = ""
    probably_chording_string = ""
    expected_chording_string = ""

    def process_event(event):
        nonlocal shift_counter
        nonlocal meta_counter
        nonlocal probably_chording
        nonlocal expected_chording_string
        nonlocal probably_chording_string
        nonlocal prev_chord

        code = event.code
        pressed_key = event.value == 1
        held_key = event.value == 2
        released_key = event.value == 0

        is_meta = keyboard_utils.is_meta(code)
        is_shift = keyboard_utils.is_shift(code)
        # TODO: shift,both ways

        if code == evdev.ecodes.KEY_BACKSPACE and (pressed_key or held_key):
            if len(queue) > 0:
                backspace_queue.append(queue.pop())
                if frozenset(backspace_queue) in chords.keys():
                    probably_chording = True
                    expected_chording_string = chords[frozenset(
                        backspace_queue)]
                    print(expected_chording_string)
                return

        if code != evdev.ecodes.KEY_BACKSPACE and (pressed_key or held_key):
            backspace_queue.clear()
        if is_meta and pressed_key:
            meta_counter += 1
        elif is_meta and released_key:
            meta_counter -= 1

        if released_key:
            return
        if meta_counter > 0 or keyboard_utils.is_arrow(code):
            queue.clear()
            return

        xkb_code = code + 8
        utf = xkb.translateKeycode(xkb_code)
        if utf is not None and utf.isprintable():
            queue.append(utf)
            if probably_chording:
                probably_chording_string += utf
            elif keyboard_utils.is_space(code):
                tmp = ""
                for i in range(2, max_output_length+1):
                    if i > len(queue):
                        break
                    tmp = queue[-i]+tmp
                    behind_is_space = True  # default to true if the buffer is to small
                    if i+1 <= len(queue):
                        behind_is_space = queue[-i-1] == " "

                    # print(queue, behind_is_space, tmp,
                    #      tmp in reversed_chords.keys())
                    if tmp in reversed_chords.keys() and behind_is_space:
                        inputs = reversed_chords[tmp]
                        options = sets_to_string(inputs)
                        config.display_message(tmp, options)

            # auto handles stopping when typign space
            if not expected_chording_string.startswith(probably_chording_string):
                if expected_chording_string == probably_chording_string.strip():
                    prev_chord = expected_chording_string
                probably_chording_string = ""
                expected_chording_string = ""
                probably_chording = False

    # Start the subprocess
    # `text=True` gives you strings instead of bytes
    # `bufsize=1` + `universal_newlines=True` ensures line-buffered reading
    proc = subprocess.Popen(
        ["sudo", "python", "-u", "t2.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    # Process output line by line as it arrives
    try:
        for line in proc.stdout:
            event = Event(*line.strip().split(" "))
            process_event(event)

    except KeyboardInterrupt:
        print("Interrupted, terminating subprocess…")
        proc.terminate()

    # Optionally wait for subprocess to end (won’t block forever if it runs indefinitely)
    proc.wait()


if __name__ == "__main__":
    main()

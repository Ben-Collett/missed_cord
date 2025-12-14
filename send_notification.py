
import subprocess
import config

missed_chords: dict[str, int] = {}

if config.qt_mode:
    from qt_bridge import bridge


def display_message(chord: str, triggers: list[str]):
    title = "possible missed chord"
    message = f'{triggers} = "{chord}" '

    if message not in missed_chords:
        missed_chords[message] = 0
    missed_chords[message] += 1
    _print_map()

    if config.qt_mode:
        # 🔥 THREAD-SAFE
        bridge.notify.emit(title, message)
    else:
        subprocess.run(
            ['notify-send', '-t', '4000', title, message]
        )


def _print_map():
    for k, v in missed_chords.items():
        print(k, v)
    print("-------------------------------")

import subprocess


missed_chords: dict[str, int] = {}


def display_message(chord: str, triggers: list[str]):
    popup_time_in_milliseconds = "4000"
    command = 'notify-send'
    title = "possible missed chord"
    message = f'you could have typed: {triggers}\n to type "{chord}" '
    if message not in missed_chords:
        missed_chords[message] = 0
    missed_chords[message] += 1
    _print_map()
    subprocess.run([command, '-t', popup_time_in_milliseconds, title, message])


def _print_map():
    for k, v in missed_chords.items():
        print(k, v)
    print("-------------------------------")


# for testing
if __name__ == "__main__":
    display_message("that", ["th", "tg"])

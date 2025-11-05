import subprocess


def display_message(chord: str, triggers: list[str]):
    command = "notify-send"
    title = "possible missed chord"
    message = f'you could have typed: {triggers}\n to type "{chord}" '
    subprocess.run([command, title, message])


# for testing
if __name__ == "__main__":
    display_message("that", ["th", "tg"])

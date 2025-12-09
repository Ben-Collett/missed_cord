import keyboard


def output_event(event: keyboard.KeyboardEvent):
    value = 0
    if event.event_type == keyboard.KEY_DOWN:
        value = 1
    print(event.name, value)


def main():
    keyboard.hook(output_event)
    keyboard.wait()


if __name__ == "__main__":
    main()

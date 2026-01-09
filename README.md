# Missed Cord

A Windows/Linux program designed to work alongside a Charachorder keyboard when practicing. It monitors your typing and sends a notification when you miss an opportunity to use a chord shortcut and type the text manually instead.

## Overview

Missed Cord detects when you type the output of a chord manually instead of using the chord shortcut. When this happens, it sends a notification showing what chord you could have used to type that text, helping you learn and improve your chord typing skills.

## Disclaimer 
This project has no affilination with charachorder as a company. This project is simply developed and maintained by someone who is trying to get good at using a charachorder.

## Requirements

### System Dependencies
- **Linux** (Wayland support)
- **libxkbcommon** - Keyboard handling library
- **notify-send** - Desktop notification utility
- **Notification daemon** - Such as:
  - dunst
  - SwatNotificationCenter
  - Or any other D-Bus compatible notification service

### Python Dependencies
- **Python 3**

## Installation

1. Install system dependencies (example for Debian/Ubuntu):
```bash
sudo apt-get install make gcc libxkbcommon-dev python3-evdev libnotify dunst
```

1. Clone or download this repository

1. Build the C code:
```bash
make
```

1. Export your Charachorder chord library:
   - Open the Charachorder Manager application
   - Export your chord library for backup
   - Copy the exported file to the project directory
   - Rename it to `chords.json`

## Usage

**Important:** The program must be run in user mode, not with `sudo`. The script will prompt you for your admin password when needed to access keyboard input on Wayland.

1. Build the project (if not already done):
```bash
make
```

1. Run the program:
```bash
python main.py
```

1. When prompted, enter your admin password to grant the program permission to read keyboard input in the background on Wayland.

1. The program will now monitor your typing and send notifications when you miss chord opportunities.

## How It Works

The program monitors keyboard events and detects when you:
1. Type the trigger for a chord (which gets deleted)
2. Then type the text output of that chord manually

When this pattern is detected, it sends a notification showing what chord you could have used instead.

## Configuration

You can customize the notification behavior by modifying the `display_message` function in `config.py`. By default, it uses `notify-send` to display notifications.

Example configuration in `config.py`:
```python
def display_message(chord: str, triggers: list[str]):
    popup_time_in_milliseconds = "4000"
    command = 'notify-send'
    title = "possible missed chord"
    message = f'you could have typed: {triggers}\n to type "{chord}" '
    subprocess.run([command, '-t', popup_time_in_milliseconds, title, message])
```

## Limitations and Edge Cases

1. **Charachorder Mode**: This program only works with Charachorder's default mode, **not** in "spurgging mode".

1. **Detection Method**: The program relies on the trigger being deleted in order to detect a chord. This means the detection works by observing when the chord trigger is typed and then removed.

1. **Edge Case**: If you type the trigger for a chord, then press backspace, and then type the text of the chord, the program will treat it as if you executed the chord. This is a known limitation.

1. **Linux Only**: Currently, this program only supports Linux systems.

## D-Bus Requirement

It's important to note that the script needs to run in user mode (not with `sudo`) because:
- The program needs admin privileges to read keyboard input on Wayland
- However, it also needs access to D-Bus to send notifications
- Running as root (`sudo python main.py`) will prevent the notification service from working because D-Bus is not accessible to root processes

The program handles this by running as a regular user and only using `sudo` for the specific keyboard input access subprocess.

## Troubleshooting

- **Notifications not appearing**: Make sure you have a notification daemon running (like dunst or SwatNotificationCenter)
- **Permission denied**: Make sure you're running the program as a regular user (not with `sudo`) and enter the password when prompted
- **chords.json not found**: Ensure you've exported your chord library from Charachorder Manager and placed it in the project directory as `chords.json`

##Roadmap
- add support for windows notifications
- add ability to read chords directly from charachorder if enabled,

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details



import tomllib
import os
from utils import uncapitalize
from duration import Duration
from chording_modes import ChordingModes
from logger import log_warning
from my_config_manager import config_manager
from constants import FILE_NAME


from pathlib import Path


def safe_get_map(m, *args, default=None):
    if len(args) == 0:
        return default

    for arg in args:
        if m is not None and arg in m:
            m = m[arg]
        else:
            return default

    if m is None:
        return default
    return m


def get_config_path() -> Path:
    if Path(FILE_NAME).is_file():
        return Path(FILE_NAME)

    path = config_manager.find_config_file(FILE_NAME)
    print(path)
    if path and path.is_file():
        return path


def read_config(path: Path | None):
    if not path:
        return {}
    with open(path.absolute(), "rb") as f:
        data = tomllib.load(f)
        return data


def is_on_wayland():
    return os.environ.get("WAYLAND_DISPLAY") is not None


DEFAULT_MAX_QT_NOTIFICATIONS = 3
# if <0 then there is no maximum
max_qt_notifications = DEFAULT_MAX_QT_NOTIFICATIONS

DEFAULT_DURATION = Duration(seconds=4)
DEFAULT_NOTIFICATION_TITLE = "possible missed chord"
DEFAULT_NOTIFICATION_MESSAGE = "$triggers = $chord"
DEFAULT_WINDOW_WIDTH = 400
DEFAULT_WINDOW_HEIGHT = 100
DEFAULT_DURATION_HEIGHT = 4


class Config:
    def __init__(self, config_map={}):
        self.update_config(config_map)

    def notification_message(self, triggers, message):
        return self.notification_message_template.replace("$triggers", str(triggers)).replace("$chord", message)

    def update_config(self, config_map):
        def general_setting(label, default):
            return safe_get_map(config_map, "general", label, default=default)

        def qt_setting(label, default):
            return safe_get_map(config_map, "qt", label, default=default)

        def notification_setting(label, default):
            return safe_get_map(config_map, "notification", label, default=default)

        def filter_setting(label, default=[]):
            return safe_get_map(config_map, "filter", label, default=default)

        duration_s = notification_setting("duration_seconds", None)
        duration_ms = notification_setting("duration_milliseconds", None)

        if duration_ms:
            self.duration = Duration(milliseconds=duration_ms)
        elif duration_s:
            self.duration = Duration(seconds=duration_s)
        else:
            self.duration = DEFAULT_DURATION

        self.max_qt_notifications = qt_setting(
            "max_notifications", DEFAULT_MAX_QT_NOTIFICATIONS)

        self.show_duration_bar = qt_setting("show_duration", default=True)

        self.excluded_chords = filter_setting("excluded_chords")
        self.excluded_chords = [uncapitalize(c) for c in self.excluded_chords]

        mode = notification_setting("mode", "auto")

        if mode == "qt":
            self.qt_mode = True
        elif mode == "notify":
            self.qt_mode = False
        elif mode == "auto":
            self.qt_mode = not is_on_wayland()
        else:
            log_warning("invalid mode selected, defaulting to auto")
            self.qt_mode = not is_on_wayland()

        self.notification_title = notification_setting(
            "title", DEFAULT_NOTIFICATION_TITLE)
        self.notification_message_template = notification_setting(
            "message", DEFAULT_NOTIFICATION_MESSAGE)

        self.window_width = qt_setting("window_width", DEFAULT_WINDOW_WIDTH)
        self.window_height = qt_setting("window_height", DEFAULT_WINDOW_HEIGHT)
        self.duration_height = qt_setting(
            "duration_height", DEFAULT_DURATION_HEIGHT)
        mode = general_setting("mode", "charachorder")
        try:
            self.mode = ChordingModes(mode)
        except ValueError:
            log_warning("invalid mode, defaulting to charachorder")
            self.mode = ChordingModes.CHARA_CHORDER

    def __str__(self):
        lines = "\n".join(f"  {k}: {v!r}" for k, v in vars(self).items())
        return f"{self.__class__.__name__} {{\n{lines}\n}}"


print(get_config_path())
current_config = Config(read_config(get_config_path()))

if __name__ == "__main__":
    print(get_config_path())
    print(current_config)

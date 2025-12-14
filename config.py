import platform
import os
# TODO: read a config file


def update_from_file():
    pass


def is_on_wayland():
    return os.environ.get("WAYLAND_DISPLAY") is not None


qt_mode = not is_on_wayland()

DEFAULT_MAX_QT_NOTIFICATIONS = 3
# if <0 then there is no maximum
max_qt_notifications = DEFAULT_MAX_QT_NOTIFICATIONS

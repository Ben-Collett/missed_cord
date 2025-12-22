import platform
import os
import pwd
from pathlib import Path
PROGRAM_NAME = "missed_chord"
FILE_NAME = "config.toml"
is_on_windows = platform.system() == "Window"
is_on_linux = platform.system() == "Linux"
is_on_mac = platform.system() == "Darwin"


class Platform:
    @property
    def linux_config_path(self):
        sudo_uid = os.environ.get("SUDO_UID")

        if sudo_uid:
            # Script was run via sudo
            pw = pwd.getpwuid(int(sudo_uid))
            home = Path(pw.pw_dir)
        else:
            # Not run via sudo
            home = Path.home()

        config_home = os.getenv("XDG_CONFIG_HOME")
        if not config_home:
            config_home = home.joinpath(".config/")
        return config_home.joinpath(PROGRAM_NAME, FILE_NAME).expanduser()

    @property
    def windows_config_path(self):
        appdata = os.getenv("APPDATA")
        if not appdata:
            # extremely rare, but a safe fallback
            appdata = Path.home() / "AppData" / "Roaming"
        return Path(appdata) / PROGRAM_NAME / FILE_NAME

    @property
    def macos_config_path(self):
        return (
            Path.home()
            / "Library"
            / "Application Support"
            / PROGRAM_NAME
            / FILE_NAME
        )

    @property
    def on_linux(self):
        return is_on_linux

    @property
    def on_windows(self):
        return is_on_windows

    @property
    def on_mac(self):
        return is_on_mac

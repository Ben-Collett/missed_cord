import platform
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"


def log_warning(msg):
    if platform.system() == "Windows":
        print(str(msg))
    else:
        print(f"{YELLOW}{str(msg)}{RESET}")

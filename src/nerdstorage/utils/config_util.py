import os

from nerdstorage import config

VERSION = "0.2.0"

HELP = ["-h", "--help"]


class Color:
    RED = "\033[1;31m"
    YELLOW = "\033[1;33m"
    GREEN = "\033[1;32m"
    BLUE = "\033[1;34m"
    END = "\033[0m"


def args_parser(argv):
    if len(argv) <= 1:
        return True

    if argv[1] in HELP:
        help()
    else:
        print("Invalid parameter.")

    return False


def help():
    print(
        f"Nerd-Storage {VERSION}\n0xHaru <0xharu.git@gmail.com>\n"
        "Project home page: https://github.com/0xHaru/Nerd-Storage\n\n"
        "A simple LAN storage.\n\n"
        f"{Color.BLUE}USAGE:{Color.END}\n\tnerdstorage\n\n"
        f"{Color.BLUE}CONFIG:{Color.END}\n\t"
        "1) Run hash.py to set the login password.\n\t"
        "2) Edit config.py to set the storage path.\n\n\t"
        "This command will output the full path of hash.py and config.py:\n\t    "
        f"{Color.GREEN}pip show Nerd-Storage | "
        "grep 'Location' | grep -o -E '[/].+' | "
        r"xargs -I@ printf '@/nerdstorage/hash/hash.py\n@/nerdstorage/config.py\n'"
    )


def check_config():
    is_instance(config.USER_ID, int, "USER_ID", "integer")
    is_instance(config.USERNAME, str, "USERNAME", "string")
    is_instance(config.STORAGE_PATH, str, "STORAGE_PATH", "string")
    is_instance(config.SECURITY_ALERT, str, "SECURITY_ALERT", "string")

    check_path(config.STORAGE_PATH)

    return True


def is_instance(arg, typeof, name, typeof_str):
    if not isinstance(arg, typeof):
        raise TypeError(f"{name} must be a/an {typeof_str}.")


def check_path(path):
    if not os.path.isabs(path):
        raise TypeError("STORAGE_PATH must be an absolute path.")

    if not os.path.isdir(path):
        raise TypeError("STORAGE_PATH must be an existing directory.")

import sys

from NERD import create_app
from NERD.config import PORT
from NERD.utils.config_util import args_parser, check_config

app = create_app()


def main():
    try:
        if args_parser(sys.argv) and check_config():
            app.run(host="0.0.0.0", port=PORT, debug=True)
    except TypeError as e:
        print(e)


if __name__ == "__main__":
    main()

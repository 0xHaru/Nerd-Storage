import sys

from nerdstorage import create_app
from nerdstorage.config import PORT
from nerdstorage.utils.config_util import args_parser, check_config

app = create_app()


def main():
    try:
        if args_parser(sys.argv) and check_config():
            app.run(host="0.0.0.0", port=PORT, debug=True)
    except TypeError as e:
        print(e)


if __name__ == "__main__":
    main()

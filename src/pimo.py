# !/home/pi/venvs/inky/bin/python
import sys
import argparse
import pathlib
import os
import time
import random
import datetime
from PIL import Image
import logging

__author__ = "Michael Mussato"
__copyright__ = "Michael Mussato"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

PHOTOS = f"/home/pi/images"
PYTHON = "/home/pi/venvs/inky/bin/python"
PY = "/home/pi/git/inky/examples/7color/image.py"
SATURATION = 0.0
FORCE_ORIENTATION = True
ORIENTATION = ['portrait', 'landscape', 'square'][0]


# ---- Python API ----


def set_pimo():
    while not pathlib.Path(PHOTOS).exists():
        print(f"No images folder found ({PHOTOS}).\nRetrying in 10 seconds...\n")
        time.sleep(10)

    print(f'Images folder found at {PHOTOS}.')

    # while True:
    print('Searching...')

    jpg = list(pathlib.Path(f"{PHOTOS}").rglob("*.[jJpP][pPnN][gG]"))

    while True:
        choice = random.choice(jpg)

        img = Image.open(choice)
        size = img.size

        if size[0] > size[1]:  # landscape
            orientation = 'landscape'
        elif size[0] < size[1]:  # portrait
            orientation = 'portrait'
        else:  # square
            orientation = 'square'

        print(f'Image orientation is {orientation} ({size[0]} x {size[1]})')
        print(f'Frame orientation is {ORIENTATION}')

        if FORCE_ORIENTATION:
            if orientation == 'square' \
                    or orientation == ORIENTATION:
                break
        else:
            break

        choice = random.choice(jpg)

    print(f"Setting image: {choice}")

    os.popen(f'{PYTHON} {PY} {choice} {SATURATION}').read()


# ---- CLI ----


def parse_args(args):

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    # subparsers = parser.add_subparsers(
    #     required=True,
    #     dest="sub_command",
    # )

    # parser_c = subparsers.add_parser(
    #     "compress",
    #     aliases=["c"],
    # )

    # parser_c.add_argument(
    #     "-src",
    #     "--source-directory",
    #     dest="src",
    #     required=True,
    #     default=None,
    #     type=pathlib.Path,
    #     help="The source directory to encrypt.",
    # )

    # parser_c.add_argument(
    #     "-dest",
    #     "--destination-directory",
    #     dest="dest",
    #     required=True,
    #     default=None,
    #     type=pathlib.Path,
    #     help="The source directory to encrypt.",
    # )

    # parser_e = subparsers.add_parser(
    #     "extract",
    #     aliases=["e"],
    # )

    # parser_e.add_argument(
    #     "-i",
    #     "--in-file",
    #     dest="in_file",
    #     required=True,
    #     default=None,
    #     type=pathlib.Path,
    # )

    # parser_e.add_argument(
    #     "-o",
    #     "--out-root",
    #     dest="out_root",
    #     required=True,
    #     default=None,
    #     type=pathlib.Path,
    # )

    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    args = parse_args(args)
    setup_logging(args.loglevel)

    if any([sc == args.sub_command for sc in ["compress", "c"]]):
        pass
    elif any([sc == args.sub_command for sc in ["extract", "e"]]):
        pass

    set_pimo()

    sys.exit(0)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()

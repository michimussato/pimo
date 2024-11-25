import sys
import argparse
import pathlib
import random
import time
import os
import datetime

from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageFont, ImageDraw
# from pillow_lut import load_cube_file

from inky.auto import auto
from inky import Inky7Colour
# from inky.inky import Inky
from inky.mock import InkyMockImpression
import logging

__author__ = "Michael Mussato"
__copyright__ = "Michael Mussato"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


SATURATION = 0.0
SHOW_PATH = False

FORCE_ORIENTATION = True
ORIENTATION_ = ["square", "portrait", "landscape", "portrait_reverse", "landscape_reverse"]


pimo_downvoted = r'/home/pi/pimo_downvoted'
pimo_current = r'/home/pi/pimo_current'
pimo_history = r'/home/pi/pimo_history'


# ---- Python API ----


def get_rand_gdrive_image(
        force_aspect: bool,
        frame_orientation: str,
        search_dir: pathlib.Path = pathlib.Path(f"{os.environ['GDRIVE_MOUNT']}/media/images/scan/processed"),
) -> pathlib.Path:
    while not pathlib.Path(search_dir).exists():
        _logger.info(f"Google Drive ({search_dir}) connected?\nRetrying in 10 seconds...\n")
        time.sleep(10)

    _logger.info(f'Google Drive found at {search_dir}.')

    with open(f'{pimo_current}') as fi:
        current = fi.read().splitlines()

    _logger.info(f'current is: {current}')

    # while True:
    _logger.info('Searching...')

    jpg = list(pathlib.Path(f"{search_dir}").rglob("*.[jJ][pP][gG]"))

    choice = None

    with open(f'{pimo_downvoted}') as fi:
        while choice is None \
                or str(choice) in fi.read() \
                or str(choice) in current:
            choice = random.choice(jpg)

    _logger.info(f"Setting image: {choice}")

    with open(f'{pimo_current}', 'w') as fo:
        fo.write(f'{choice}\n')

    with open(f'{pimo_history}', 'a') as fo:
        fo.write(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}: {choice}\n')

    return choice


def get_rand_image(
        force_aspect: bool,
        frame_orientation: str,
        search_dir: pathlib.Path = pathlib.Path("/home/pi/images"),
) -> pathlib.Path:

    while not pathlib.Path(search_dir).exists():
        _logger.info(f"No images folder found ({search_dir}).\nRetrying in 10 seconds...\n")
        time.sleep(10)

    _logger.info(f'Images folder found at {search_dir}.')

    # while True:
    _logger.info('Searching...')

    jpg = list(pathlib.Path(f"{search_dir}").rglob("*.[jJpP][pPnN][gG]"))

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

        _logger.info(f'Image orientation is {orientation} ({size[0]} x {size[1]})')
        _logger.info(f'Frame orientation is {frame_orientation}')

        if force_aspect:
            if orientation == 'square' \
                    or orientation == frame_orientation:
                break
        else:
            break

    return choice


def bg_black() -> Image:
    inky = auto(ask_user=True, verbose=True)
    return Image.new(mode='RGB', size=inky.resolution, color=(0, 0, 0))


def bg_white() -> Image:
    inky = auto(ask_user=True, verbose=True)
    return Image.new(mode='RGB', size=inky.resolution, color=(255, 255, 255))


def clear_inky(
        saturation: float = SATURATION,
) -> None:
    bg = bg_black()

    inky = auto(ask_user=True, verbose=True)

    inky.set_image(bg, saturation=saturation)
    inky.show()


def test_bars(
        inky: [Inky7Colour, InkyMockImpression] = auto(ask_user=True, verbose=True),
        background_image: Image = bg_black(),
) -> Image:

    strip_size = int(inky.resolution[0] / 8)

    strip_hight = int(inky.resolution[1])

    red = Image.new(mode='RGB', size=(strip_size, strip_hight), color=(255, 0, 0))
    background_image.paste(im=red, box=(strip_size * 1, 0))

    yellow = Image.new(mode='RGB', size=(strip_size, strip_hight), color=(255, 255, 0))
    background_image.paste(im=yellow, box=(strip_size * 2, 0))

    green = Image.new(mode='RGB', size=(strip_size, strip_hight), color=(0, 255, 0))
    background_image.paste(im=green, box=(strip_size * 3, 0))

    cyan = Image.new(mode='RGB', size=(strip_size, strip_hight), color=(0, 100, 255))
    background_image.paste(im=cyan, box=(strip_size * 4, 0))

    blue = Image.new(mode='RGB', size=(strip_size, strip_hight), color=(0, 0, 255))
    background_image.paste(im=blue, box=(strip_size * 5, 0))

    # magenta = Image.new(mode='RGB', size=(strip_size, strip_hight), color=(255, 64, 192))
    magenta = Image.new(mode='RGB', size=(strip_size, strip_hight), color=(255, 0, 100))
    background_image.paste(im=magenta, box=(strip_size * 6, 0))

    white = Image.new(mode='RGB', size=(strip_size, strip_hight), color=(255, 255, 255))
    background_image.paste(im=white, box=(strip_size * 7, 0))

    grey1 = Image.new(mode='RGB', size=(strip_size, 100), color=(36, 36, 36))
    background_image.paste(im=grey1, box=(strip_size * 1, 348))

    grey2 = Image.new(mode='RGB', size=(strip_size, 100), color=(72, 72, 72))
    background_image.paste(im=grey2, box=(strip_size * 2, 348))

    grey3 = Image.new(mode='RGB', size=(strip_size, 100), color=(108, 108, 108))
    background_image.paste(im=grey3, box=(strip_size * 3, 348))

    grey4 = Image.new(mode='RGB', size=(strip_size, 100), color=(144, 144, 144))
    background_image.paste(im=grey4, box=(strip_size * 4, 348))

    grey5 = Image.new(mode='RGB', size=(strip_size, 100), color=(180, 180, 180))
    background_image.paste(im=grey5, box=(strip_size * 5, 348))

    grey6 = Image.new(mode='RGB', size=(strip_size, 100), color=(216, 216, 216))
    background_image.paste(im=grey6, box=(strip_size * 6, 348))

    return background_image


def get_image_from_file(
        frame_orientation: str,
        from_file: pathlib.Path,
) -> Image:
    img = Image.open(from_file)

    if frame_orientation == 'landscape_reverse':
        img = img.rotate(angle=0, expand=True)
    elif frame_orientation == 'portrait_reverse':
        img = img.rotate(angle=90, expand=True)
    elif frame_orientation == 'landscape':
        img = img.rotate(angle=180, expand=True)
    elif frame_orientation == 'portrait':
        img = img.rotate(angle=270, expand=True)

    return img


def set_inky_image(
        img: Image,
        inky: [Inky7Colour, InkyMockImpression] = auto(ask_user=True, verbose=True),
        saturation: float = SATURATION,
        clear_inky: bool = False,
        show_path: bool = SHOW_PATH,
        background_image: Image = bg_black(),
        enhance: bool = True,
) -> None:

    resizedimage = ImageOps.contain(img, inky.resolution, method=Image.BICUBIC)

    if enhance:
        # resizedimage = resizedimage.rotate(180)
        # resizedimage = ImageOps.contain(resizedimage, inky.resolution)

        # lut = load_cube_file(r'/home/pi/OnlineLUTCreator.CUBE')
        # resizedimage = resizedimage.filter(lut)

        converter = ImageEnhance.Color(resizedimage)
        resizedimage = converter.enhance(3.0)

        converter = ImageEnhance.Sharpness(resizedimage)
        resizedimage = converter.enhance(10.0)

    # _logger.info(f'Image: {img.filename}\n')

    background_image.paste(im=resizedimage, box=(
    int(inky.resolution[0] / 2 - resizedimage.size[0] / 2), int(inky.resolution[1] / 2 - resizedimage.size[1] / 2)))

    if show_path:
        font_size = 12
        with background_image.convert('RGBA') as base:
            # src = src.replace('/data/GDRIVE/media/images/scan/processed/', '')

            fnt = ImageFont.truetype(pathlib.Path("data/ttf/ipag.ttf").resolve(), font_size)
            length = fnt.getlength(img.filename)

            # txt = Image.new('RGBA', size=inky.resolution, color=(0, 0, 0, 0))
            txt = Image.new('RGBA', size=(int(length // 1 + 1), font_size), color=(0, 0, 0, 192))
            d = ImageDraw.Draw(txt, mode='RGBA')

            # d.text((10, 10), src, font=fnt, fill=(255, 255, 255, 255))
            border = 12
            # d.text((round(txt.size[0] - length - border), border), src, font=fnt, fill=(255, 255, 255, 255))
            d.text((0, 0), img.filename, font=fnt, fill=(255, 255, 255, 255))

            txt_ = Image.new('RGBA', size=inky.resolution, color=(0, 0, 0, 0))

            ## top
            # txt_.paste(im=txt, box=(border, border))
            ## bottom
            txt_.paste(im=txt, box=(border, inky.resolution[1] - txt.size[1] - 2))

            background_image = Image.alpha_composite(base, txt_)

    inky.set_image(background_image, saturation=saturation)
    inky.show()


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

    subparsers = parser.add_subparsers(
        dest="sub_command",
        required=True,
    )

    subparser_set = subparsers.add_parser(
        "set",
        aliases=["s"],
    )

    subparser_set.add_argument(
        "--saturation",
        "-sat",
        dest="saturation",
        default=SATURATION,
        type=float,
        required=False,
        help="Saturation factor (0.0-1.0)",
    )

    subparser_set.add_argument(
        "--show-path",
        "-p",
        dest="show_path",
        default=SHOW_PATH,
        type=bool,
        required=False,
        help="Burn path onto image.",
    )

    subparser_set.add_argument(
        "--frame-orientation",
        "-o",
        choices=ORIENTATION_,
        dest="frame_orientation",
        default=None,
        type=str,
        required=True,
        help=f"Frame Orientation: {','.join(ORIENTATION_)}",
    )

    subparser_set.add_argument(
        "--force-aspect",
        "-a",
        dest="force_aspect",
        action="store_true",
        default=False,
        required=False,
        help="Force image aspect ratio to match Frame Orientation",
    )

    subparser_set_group = subparser_set.add_mutually_exclusive_group(
        required=False,
    )

    subparser_set_group.add_argument(
        "-f",
        "--from-file",
        dest="from_file",
        required=False,
        default=False,
        type=pathlib.Path,
        help="Set an image from file.",
    )

    subparser_set_group.add_argument(
        "-t",
        "--test-bars",
        dest="test_bars",
        required=False,
        default=False,
        action="store_true",
        help="Set a test bar image.",
    )

    subparser_set_group.add_argument(
        "-g",
        "--from-gdrive",
        dest="from_gdrive",
        required=False,
        default=False,
        action="store_true",
        help="Set a random image from GDrive.",
    )

    subparser_set_group.add_argument(
        "-d",
        "--from-local-directory",
        dest="from_local",
        required=False,
        default=False,
        action="store_true",
        help="Set a random image from local directory.",
    )

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

    if any([sc == args.sub_command for sc in ["set", "s"]]):

        if args.from_file:
            image = get_image_from_file(
                frame_orientation=args.frame_orientation,
                from_file=args.from_file,
            )
        elif args.test_bars:
            image = test_bars()

        elif args.from_gdrive:
            image_file = get_rand_gdrive_image(
                force_aspect=args.force_aspect,
                frame_orientation=args.frame_orientation,
            )
            image = get_image_from_file(
                frame_orientation=args.frame_orientation,
                from_file=image_file,
            )

        elif args.from_local:
            image_file = get_rand_image(
                force_aspect=args.force_aspect,
                frame_orientation=args.frame_orientation,
            )
            image = get_image_from_file(
                frame_orientation=args.frame_orientation,
                from_file=image_file,
            )

        set_inky_image(
            img=image,
            saturation=args.saturation,
            show_path=args.show_path,
        )

    sys.exit(0)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()

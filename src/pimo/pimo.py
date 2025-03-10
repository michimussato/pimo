"""
pimo is a little module that turns a
Raspberry Pi with a Pimoroni Inky
color e-ink display into a foto frame
or (using moon-clock) into a clock.
"""

import argparse
import subprocess
import datetime
import logging
import os
import pathlib
import random
import sys
import time

from ascii_magic import AsciiArt
from inky.auto import auto
from inky.inky import Inky
from inky.inky_uc8159 import Inky as InkyUC8159
from moon_clock import MoonClock
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

__author__ = "Michael Mussato"
__copyright__ = "Michael Mussato"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent
RESOURCES: pathlib.Path = BASE_DIR / "data"
ASCII_ART_COLUMNS = 80
SATURATION = 0.0

FORCE_ORIENTATION = True
ORIENTATION: list[str] = [
    "square",
    "portrait",
    "landscape",
    "portrait_reverse",
    "landscape_reverse",
]

PIMO_FILES: pathlib.Path = pathlib.Path.home() / ".pimo"
PIMO_DOWNVOTED: pathlib.Path = PIMO_FILES / "pimo_downvoted"
PIMO_UPVOTED: pathlib.Path = PIMO_FILES / "pimo_upvoted"
PIMO_CURRENT: pathlib.Path = PIMO_FILES / "pimo_current"
PIMO_HISTORY: pathlib.Path = PIMO_FILES / "pimo_history"

PIMO_LOCAL_SEARCH_DIR: pathlib.Path = pathlib.Path.home() / "images"
PIMO_DRIVE_MOUNT_DIR = os.environ.get("GDRIVE_MOUNT", None)
if PIMO_DRIVE_MOUNT_DIR is None:
    PIMO_GDRIVE_SEARCH_DIR = None
    _logger.warning("GDRIVE_MOUNT not set")
else:
    PIMO_GDRIVE_SEARCH_DIR: pathlib.Path = (
        pathlib.Path(PIMO_DRIVE_MOUNT_DIR) / "media" / "images" / "scan" / "processed"
    )


# ---- Python API ----


def init_files() -> None:
    PIMO_FILES.mkdir(parents=True, exist_ok=True)

    for i in [PIMO_UPVOTED, PIMO_CURRENT, PIMO_DOWNVOTED, PIMO_HISTORY]:

        if i.exists():
            _logger.info("Existing %s was found.", i)
        else:
            open(i, "w", encoding="utf-8").close()
            _logger.info("%s was created.", i)


def get_rand_image(
    match_aspect: bool,
    frame_orientation: str,
    search_dir: pathlib.Path,
    ascii_art: bool,
) -> pathlib.Path:

    tried = 0
    while not pathlib.Path(search_dir).exists():
        if tried > 3:
            raise FileNotFoundError(f"Search directory {search_dir} was not found.")
        _logger.info(
            "search_dir %s not found.\nRetrying in 10 seconds...\n", search_dir
        )
        time.sleep(5)
        tried += 1

    _logger.info("search_dir %s found.", search_dir)

    with open(f"{PIMO_CURRENT}", "r", encoding="utf-8") as fi:
        current = fi.read().splitlines()

    _logger.info("current = %s", current)
    if bool(current):
        if ascii_art:
            img_ascii_current = AsciiArt.from_image(path=current[0])
            _logger.info("\n%s", img_ascii_current.to_ascii(columns=ASCII_ART_COLUMNS))

    _logger.info("Searching...")

    # Todo:
    #  - [ ] Improve Regex
    jpg = list(pathlib.Path(f"{search_dir}").rglob("*.[jJpP][pPnN][gG]"))

    if not bool(jpg):
        raise FileNotFoundError(f"No images found in {search_dir}.")

    while True:
        choice = random.choice(jpg)

        with open(f"{PIMO_DOWNVOTED}", "r", encoding="utf-8") as fi:
            while choice is None or str(choice) in fi.read() or str(choice) in current:
                choice = random.choice(jpg)

        img = Image.open(choice)
        size = img.size

        if size[0] > size[1]:  # landscape
            image_orientation = "landscape"
        elif size[0] < size[1]:  # portrait
            image_orientation = "portrait"
        else:  # square
            image_orientation = "square"

        _logger.info(
            "Image orientation is %s (%i x %i)", image_orientation, size[0], size[1]
        )
        _logger.info("Frame orientation is %s", frame_orientation)

        # Do we want to allow portrait images on landscape frames
        # or landscape images on portrait frames?
        if not match_aspect:
            break

        # A picture is either square, landscape or portrait.
        # No *_reverse. Hence, check if image_orientation in frame_orientation.
        if image_orientation == "square" or image_orientation in frame_orientation:
            break

    _logger.info("Setting image: %s", choice)

    with open(f"{PIMO_CURRENT}", "w", encoding="utf-8") as fo:
        fo.write(f"{choice}\n")

    with open(f"{PIMO_HISTORY}", "a", encoding="utf-8") as fo:
        fo.write(f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}: {choice}\n")

    if ascii_art:
        img_ascii_choice = AsciiArt.from_image(path=choice)
        _logger.info("\n%s", img_ascii_choice.to_ascii(columns=ASCII_ART_COLUMNS))

    return choice


def inky_bg(
    inky: [Inky, InkyUC8159],
    color: tuple[int, int, int],
    alpha: int = 255,
) -> Image:
    return Image.new(
        mode="RGBA", size=inky.resolution, color=(color[0], color[1], color[2], alpha)
    )


def _clear_inky(
    inky: [Inky, Inky],
    saturation: float = SATURATION,
) -> None:
    bg = inky_bg(
        inky=inky,
        color=(0, 0, 0),
    )

    inky.set_image(bg, saturation=saturation)
    inky.show()


def test_bars(
    inky: Inky,
) -> Image:

    background_image: Image = inky_bg(
        inky=inky,
        color=(0, 0, 0),
    )

    strip_size = int(inky.resolution[0] / 8)

    strip_hight = int(inky.resolution[1])

    red = Image.new(mode="RGB", size=(strip_size, strip_hight), color=(255, 0, 0))
    background_image.paste(im=red, box=(strip_size * 1, 0))

    yellow = Image.new(mode="RGB", size=(strip_size, strip_hight), color=(255, 255, 0))
    background_image.paste(im=yellow, box=(strip_size * 2, 0))

    green = Image.new(mode="RGB", size=(strip_size, strip_hight), color=(0, 255, 0))
    background_image.paste(im=green, box=(strip_size * 3, 0))

    cyan = Image.new(mode="RGB", size=(strip_size, strip_hight), color=(0, 100, 255))
    background_image.paste(im=cyan, box=(strip_size * 4, 0))

    blue = Image.new(mode="RGB", size=(strip_size, strip_hight), color=(0, 0, 255))
    background_image.paste(im=blue, box=(strip_size * 5, 0))

    # magenta = Image.new(mode="RGB", size=(strip_size, strip_hight), color=(255, 64, 192))
    magenta = Image.new(mode="RGB", size=(strip_size, strip_hight), color=(255, 0, 100))
    background_image.paste(im=magenta, box=(strip_size * 6, 0))

    white = Image.new(mode="RGB", size=(strip_size, strip_hight), color=(255, 255, 255))
    background_image.paste(im=white, box=(strip_size * 7, 0))

    grey1 = Image.new(mode="RGB", size=(strip_size, 100), color=(36, 36, 36))
    background_image.paste(im=grey1, box=(strip_size * 1, 348))

    grey2 = Image.new(mode="RGB", size=(strip_size, 100), color=(72, 72, 72))
    background_image.paste(im=grey2, box=(strip_size * 2, 348))

    grey3 = Image.new(mode="RGB", size=(strip_size, 100), color=(108, 108, 108))
    background_image.paste(im=grey3, box=(strip_size * 3, 348))

    grey4 = Image.new(mode="RGB", size=(strip_size, 100), color=(144, 144, 144))
    background_image.paste(im=grey4, box=(strip_size * 4, 348))

    grey5 = Image.new(mode="RGB", size=(strip_size, 100), color=(180, 180, 180))
    background_image.paste(im=grey5, box=(strip_size * 5, 348))

    grey6 = Image.new(mode="RGB", size=(strip_size, 100), color=(216, 216, 216))
    background_image.paste(im=grey6, box=(strip_size * 6, 348))

    return background_image


def get_rotation_angle(
    frame_orientation: str,
) -> int:

    if frame_orientation == "landscape_reverse":
        angle = 0
    elif frame_orientation == "portrait_reverse":
        angle = 90
    elif frame_orientation == "landscape":
        angle = 180
    elif frame_orientation == "portrait":
        angle = 270
    else:
        raise NotImplementedError("Invalid orientation")

    return angle


def set_inky_image(
    img: Image,
    expand: bool,
    frame_orientation: str,
    ascii_art: bool,
    show_path: bool,
    inky: [Inky, InkyUC8159],
    border: int,
    background_color: tuple[int, int, int],
    border_color: tuple[int, int, int, int],
    saturation: float = SATURATION,
    clear_inky: bool = False,
    enhance: bool = True,
) -> None:

    _max_border_value = int(min(inky.resolution) / 2) - 1

    assert (
        border <= _max_border_value
    ), f"Max border value for {inky.resolution} is {_max_border_value}."
    assert all(0 <= i <= 255 for i in background_color)
    assert all(0 <= i <= 255 for i in border_color)

    background_image: Image = inky_bg(
        inky=inky,
        color=background_color,
        alpha=255,
    )

    _logger.debug("background_image.size = %s", background_image.size)
    _logger.debug("inky.resolution = %s", inky.resolution)
    _logger.debug("img.size = %s", img.size)
    _logger.debug("img.mode = %s", img.mode)

    angle = get_rotation_angle(frame_orientation)

    _img = img.rotate(angle, expand=True)

    # Make sure we have an alpha channel if not present
    if not _img.mode == "RGBA":
        _img = _img.convert("RGBA")

    _logger.info("img.mode = %s", img.mode)
    _logger.info("_img.mode = %s", _img.mode)
    _logger.info("background_image.mode = %s", background_image.mode)

    if clear_inky:
        _clear_inky(inky=inky)

    if border:
        size = _img.size
        new_size = (
            size[0] - border * 2,
            size[1] - border * 2,
        )

        _img_bg: Image = inky_bg(
            inky=inky,
            color=background_color,
            alpha=255,
        )

        _img_bg.paste(
            ImageOps.pad(image=_img, size=new_size, color=border_color),
            box=(
                int(inky.resolution[0] / 2 - new_size[0] / 2),
                int(inky.resolution[1] / 2 - new_size[1] / 2),
            ),
        )

        _img = _img_bg

    # https://pillow.readthedocs.io/en/stable/reference/ImageOps.html#resize-relative-to-a-given-size
    if expand:
        resizedimage = ImageOps.fit(
            image=_img,
            size=inky.resolution,
            method=Image.Resampling.BICUBIC,
        )
    else:
        resizedimage = ImageOps.contain(
            image=_img,
            size=inky.resolution,
            method=Image.Resampling.BICUBIC,
        )

    if enhance:
        # resizedimage = resizedimage.rotate(180)
        # resizedimage = ImageOps.contain(resizedimage, inky.resolution)

        # lut = load_cube_file(r'/home/pi/OnlineLUTCreator.CUBE')
        # resizedimage = resizedimage.filter(lut)

        converter = ImageEnhance.Color(resizedimage)
        resizedimage = converter.enhance(3.0)

        converter = ImageEnhance.Sharpness(resizedimage)
        resizedimage = converter.enhance(10.0)

    _logger.debug("background_image.size = %s", background_image.size)
    _logger.debug("background_image.mode = %s", background_image.mode)
    _logger.debug("resizedimage.size = %s", resizedimage.size)
    _logger.debug("resizedimage.mode = %s", resizedimage.mode)
    background_image = Image.alpha_composite(
        background_image,
        # https://pillow.readthedocs.io/en/stable/reference/ImageOps.html#resize-relative-to-a-given-size
        ImageOps.pad(
            image=resizedimage,
            size=background_image.size,
            color=(0, 0, 0, 0),
        ),
    )

    if show_path:
        font_size = 12
        with background_image.convert("RGBA") as base:

            _logger.debug("TTF from %s", RESOURCES / "ttf" / "ipag.ttf")

            fnt = ImageFont.truetype(RESOURCES / "ttf" / "ipag.ttf", font_size)
            length = fnt.getlength(img.filename)

            # txt = Image.new('RGBA', size=inky.resolution, color=(0, 0, 0, 0))
            txt = Image.new(
                "RGBA", size=(int(length // 1 + 1), font_size), color=(0, 0, 0, 192)
            )
            d = ImageDraw.Draw(txt, mode="RGBA")

            border = 12
            d.text((0, 0), img.filename, font=fnt, fill=(255, 255, 255, 255))

            txt_ = Image.new("RGBA", size=inky.resolution, color=(0, 0, 0, 0))

            if inky.resolution == (600, 448):
                passe_partout_long_edges = 0
            elif inky.resolution == (800, 480):
                passe_partout_long_edges = 25
            else:
                raise NotImplementedError("Resolution not supported.")
            _logger.debug("passe_partout_long_edges = %i", passe_partout_long_edges)

            ## landscape/landscape_reverse: top-right
            txt_.paste(
                im=txt,
                box=(
                    inky.resolution[0]
                    - txt.size[0]
                    - border
                    - passe_partout_long_edges,
                    border,
                ),
            )
            ## portrait/portrait_reverse:
            # txt_.paste(im=txt, box=(border, inky.resolution[1] - txt.size[1] - 2))

            _logger.debug("txt_.size = %s", txt_.size)
            _logger.debug("border = %i", border)
            _logger.debug("txt.size = %s", txt.size)

            if "landscape_reverse" == frame_orientation:
                pass
            elif "landscape" == frame_orientation:
                txt_ = txt_.rotate(180)
            elif "portrait" == frame_orientation:
                pass
            elif "portrait_reverse" == frame_orientation:
                txt_ = txt_.rotate(180)

            background_image = Image.alpha_composite(base, txt_)

    if ascii_art:
        _logger.info("Final Render:")
        img_ascii = AsciiArt.from_pillow_image(background_image)
        _logger.info("\n%s", img_ascii.to_ascii(columns=ASCII_ART_COLUMNS))

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

    # subparser_system_timezone = subparsers.add_parser(
    #     "timezone",
    #     aliases=["tz"],
    # )

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
        default=False,
        action="store_true",
        required=False,
        help="Burn path onto image.",
    )

    subparser_set.add_argument(
        "--ascii-art",
        "-a",
        dest="ascii_art",
        default=False,
        action="store_true",
        required=False,
        help="Log AsciiArt image previews.",
    )

    subparser_set.add_argument(
        "--frame-orientation",
        "-o",
        choices=ORIENTATION,
        dest="frame_orientation",
        default=None,
        type=str,
        required=True,
        help=f"Frame Orientation: {','.join(ORIENTATION)}",
    )

    subparser_set.add_argument(
        "--match-aspect",
        "-m",
        dest="match_aspect",
        action="store_true",
        default=False,
        required=False,
        help="Force image aspect ratio to match Frame Orientation",
    )

    subparser_set.add_argument(
        "--expand",
        "-e",
        dest="expand",
        action="store_true",
        default=False,
        required=False,
        help="Expand image to cover full frame",
    )

    subparser_set.add_argument(
        "--border",
        "-b",
        dest="border",
        default=0,
        type=int,
        required=False,
        help="Add border around image",
    )

    subparser_set.add_argument(
        "--border-color",
        "-bc",
        dest="border_color",
        nargs=4,
        default=[0, 0, 0, 0],
        type=int,
        required=False,
        help="Set border color (RGBA tuple). " "Default is transparent.",
    )

    subparser_set.add_argument(
        "--background-color",
        "-bg",
        dest="background_color",
        nargs=3,
        default=[0, 0, 0],
        type=int,
        required=False,
        help="Set background color (RGB tuple).",
    )

    subparser_set.add_argument(
        "--moon-shadow-opacity",
        "-s",
        dest="moon_shadow_opacity",
        default=127,
        type=int,
        required=False,
        help="Black dial background or transparent. (0<=moon-shadow<=255).",
    )

    subparser_set.add_argument(
        "--timezone",
        "-tz",
        dest="timezone",
        default=None,
        type=str,
        required=False,
        help="Set System Timezone to timezone",
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
        "--moon-clock",
        "-c",
        dest="moon_clock",
        default=None,
        type=str,
        required=False,
        help="Display moon-clock based on location",
    )

    subparser_set_group.add_argument(
        "-g",
        "--from-gdrive",
        dest="from_gdrive",
        required=False,
        default=False,
        action="store_true",
        help=(
            f"Set a random image from GDrive. " f"Defaults to {PIMO_GDRIVE_SEARCH_DIR}."
            if PIMO_GDRIVE_SEARCH_DIR is not None
            else argparse.SUPPRESS
        ),
    )

    subparser_set_group.add_argument(
        "-d",
        "--from-local-directory",
        dest="from_local",
        required=False,
        default=False,
        action="store_true",
        help=f"Set a random image from local directory. "
        f"Defaults to {PIMO_LOCAL_SEARCH_DIR}",
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

    init_files()

    inky: Inky = auto(ask_user=True, verbose=True)

    image = None

    if any(sc == args.sub_command for sc in ["set", "s"]):

        if args.timezone:
            _logger.info("Setting System Timezone to %s", args.timezone)

            result = subprocess.run(
                args=f"sudo timedatectl set-timezone {args.timezone}",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                shell=True,
            )

            _logger.info("timedatectl %s", result)

        if args.from_file:
            image_file = args.from_file

            image = Image.open(image_file)

        elif args.test_bars:
            image = test_bars(inky=inky)

        elif args.moon_clock:
            size = min(inky.resolution)
            image = MoonClock().get_clock(
                address=args.moon_clock,
                size=size,
                dial_shadow_opacity=args.moon_shadow_opacity,
            )

        elif args.from_gdrive:
            image_file = get_rand_image(
                search_dir=PIMO_GDRIVE_SEARCH_DIR,
                match_aspect=args.match_aspect,
                frame_orientation=args.frame_orientation,
                ascii_art=args.ascii_art,
            )

            image = Image.open(image_file)

        elif args.from_local:
            image_file = get_rand_image(
                search_dir=PIMO_LOCAL_SEARCH_DIR,
                match_aspect=args.match_aspect,
                frame_orientation=args.frame_orientation,
                ascii_art=args.ascii_art,
            )

            image = Image.open(image_file)

        if image is None:
            raise RuntimeError("Image could not be created.")

        set_inky_image(
            img=image,
            ascii_art=args.ascii_art,
            expand=args.expand,
            inky=inky,
            frame_orientation=args.frame_orientation,
            saturation=args.saturation,
            show_path=args.show_path,
            border=args.border,
            border_color=(
                int(args.border_color[0]),
                int(args.border_color[1]),
                int(args.border_color[2]),
                int(args.border_color[3]),
            ),
            background_color=(
                int(args.background_color[0]),
                int(args.background_color[1]),
                int(args.background_color[2]),
            ),
        )

    sys.exit(0)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()

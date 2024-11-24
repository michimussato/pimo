# !/home/pi/venvs/inky/bin/python

import sys
# import time

from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageFont, ImageDraw
# from pillow_lut import load_cube_file

from inky.auto import auto
import logging

__author__ = "Michael Mussato"
__copyright__ = "Michael Mussato"
__license__ = "MIT"


# ---- Python API ----


def func():
    inky = auto(ask_user=True, verbose=True)
    saturation = 0.0
    frame_orientation = ['portrait', 'landscape'][0]

    clear_inky = False
    show_path = False

    print(sys.argv)

    bg_black = Image.new(mode='RGB', size=inky.resolution, color=(0, 0, 0))
    bg_white = Image.new(mode='RGB', size=inky.resolution, color=(255, 255, 255))
    backgrounds = [bg_black, bg_white]
    background_clear = backgrounds[0]
    background_image = backgrounds[1]

    if clear_inky:
        inky.set_image(background_clear, saturation=saturation)
        inky.show()

    if len(sys.argv) == 1:

        src = 'Test Bars'

        strip_size = int(inky.resolution[0] / 8)

        strip_hight = int(inky.resolution[1])

        # bg = Image.new(mode='RGB', size=inky.resolution, color=(0, 0, 0))

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

    elif len(sys.argv) > 1:

        enhance = True

        src = sys.argv[1]

        if src == 'inky':
            enhance = False
            img = Image.open(f'/home/pi/git/inky/examples/7color/images/inky-7.3-ships.jpg')
        else:
            # ['/home/pi/git/inky/examples/7color/image.py', '/data/GDRIVE/media/images/scan/processed/reflecta_mf_5000__2022-04-17__Film_0002/jpg__2023-05-07__22-16-14/2022-04-17__Film_0002__1280__0006', '(2).jpg', '0.0']
            # /data/GDRIVE/media/images/scan/processed/reflecta_mf_5000__2022-04-17__Film_0002/jpg__2023-05-07__22-16-14/2022-04-17__Film_0002__1280__0006 (2).jpg
            # FileNotFoundError: [Errno 2] No such file or directory: '/data/GDRIVE/media/images/scan/processed/reflecta_mf_5000__2022-04-17__Film_0002/jpg__2023-05-07__22-16-14/2022-04-17__Film_0002__1280__0006'
            img = Image.open(src)

            if frame_orientation == 'portrait':
                img = img.rotate(angle=270, expand=True)
            elif frame_orientation == 'landscape':
                img = img.rotate(angle=180, expand=True)

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

        print(f'Image: {src}\n')

        background_image.paste(im=resizedimage, box=(
        int(inky.resolution[0] / 2 - resizedimage.size[0] / 2), int(inky.resolution[1] / 2 - resizedimage.size[1] / 2)))

        if len(sys.argv) > 2:
            try:
                saturation = float(sys.argv[2])
            except ValueError:
                saturation = saturation

    if show_path:
        font_size = 12
        with background_image.convert('RGBA') as base:
            # src = src.replace('/data/GDRIVE/media/images/scan/processed/', '')

            fnt = ImageFont.truetype("/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf", font_size)
            length = fnt.getlength(src)

            # txt = Image.new('RGBA', size=inky.resolution, color=(0, 0, 0, 0))
            txt = Image.new('RGBA', size=(int(length // 1 + 1), font_size), color=(0, 0, 0, 192))
            d = ImageDraw.Draw(txt, mode='RGBA')

            # d.text((10, 10), src, font=fnt, fill=(255, 255, 255, 255))
            border = 12
            # d.text((round(txt.size[0] - length - border), border), src, font=fnt, fill=(255, 255, 255, 255))
            d.text((0, 0), src, font=fnt, fill=(255, 255, 255, 255))

            txt_ = Image.new('RGBA', size=inky.resolution, color=(0, 0, 0, 0))

            ## top
            # txt_.paste(im=txt, box=(border, border))
            ## bottom
            txt_.paste(im=txt, box=(border, inky.resolution[1] - txt.size[1] - 2))

            background_image = Image.alpha_composite(base, txt_)

    # if frame_orientation == 'portrait':
    #    background_image = background_image.rotate(angle=270)
    ##elif frame_orientation == 'landscape':
    #    background_image = background_image.rotate(angle=180)

    print(f'Saturation: {saturation}\n')
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

    # if any([sc == args.sub_command for sc in ["compress", "c"]]):
    #     pass
    # elif any([sc == args.sub_command for sc in ["extract", "e"]]):
    #     pass

    func()

    sys.exit(0)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()


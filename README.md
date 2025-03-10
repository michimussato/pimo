<!-- TOC -->
* [pimo](#pimo)
  * [venv](#venv)
  * [Installation](#installation)
    * [Known Issues](#known-issues)
      * ["setup.py" not found.](#setuppy-not-found)
      * [Woah there, some pins we need are in use!](#woah-there-some-pins-we-need-are-in-use)
  * [Usage](#usage)
    * [CLI](#cli)
    * [Sub Commands](#sub-commands)
      * [`set`](#set)
  * [Examples](#examples)
    * [moode-oroni](#moode-oroni)
    * [frame-oroni](#frame-oroni)
      * [frame landscape (frame-vertical)](#frame-landscape-frame-vertical)
      * [frame portrait (frame)](#frame-portrait-frame)
  * [pre-commit](#pre-commit)
  * [nox](#nox)
  * [SBOM](#sbom)
<!-- TOC -->

---

# pimo

Todo:
- [ ] Migrage Info from https://github.com/michimussato/moode-oroni/blob/main/README_INKY_RASPIOS.md to here

## venv

```shell
source ~/venvs/inky/bin/activate
```

## Installation

```shell
pip install git+https://github.com/michimussato/pimo.git
```

or

```shell
git clone https://github.com/michimussato/pimo.git
cd pimo
pip install -e .
```

### Known Issues

#### "setup.py" not found.

```
$ pip install -e .
ERROR: File "setup.py" not found. Directory cannot be installed in editable mode: /home/pi/git/pimo
(A "pyproject.toml" file was found, but editable mode currently requires a setup.py based build.)
```

```shell
pip install pip --upgrade
```

#### Woah there, some pins we need are in use!

```
$ pimo -v s -t -o landscape_reverse
Detected 7-Colour (UC8159)
Detected 7-Colour (UC8159)
Detected 7-Colour (UC8159)
Detected 7-Colour (UC8159)
Woah there, some pins we need are in use!
  ⚠️   Chip Select: (line 8, SPI_CE0_N) currently claimed by spi0 CS0
```

```
gpiod==2.2.2
gpiodevice==0.0.5
inky==2.0.0
numpy==2.0.2
pillow==11.0.0
pillow-lut==1.0.1
pimo @ git+https://github.com/michimussato/pimo.git@5dae016860aadbdef093d91803429f54165b9dc9
smbus2==0.5.0
spidev==3.6
```

Happens for `inky[rpi]==2.0.0`. Temporary solution is to
lock `inky[rpi]>=1.5.0,<1.6`.
Mentioned [here](https://github.com/pimoroni/inky?tab=readme-ov-file#install-stable-library-from-pypi-and-configure-manually)

```
inky==1.5.0
numpy==2.0.2
pillow==11.0.0
pillow-lut==1.0.1
pimo @ git+https://github.com/michimussato/pimo.git@7afbc61518c456c0822d95cdc8b4c804dfc0b7ad
RPi.GPIO==0.7.1
smbus2==0.5.0
spidev==3.6
```

Todo: Try to go through the whole setup procedure:
https://github.com/pimoroni/inky?tab=readme-ov-file#install-stable-library-from-pypi-and-configure-manually

For reference:
```
beautifulsoup4==4.12.3
certifi==2024.2.2
charset-normalizer==3.3.2
click==8.1.7
decorator==5.1.1
font-fredoka-one==0.0.4
font-hanken-grotesk==0.0.2
font-intuitive==0.0.4
font-source-serif-pro==0.0.1
future==0.18.3
geocoder==1.38.1
idna==3.6
inky==1.5.0
numpy==1.26.4
pillow==10.2.0
pillow-lut==1.0.1
-e git+https://github.com/michimussato/pimo.git@1d0bdff77f6ab5c3c230e63fa3650bada96f71c8#egg=pimo
pkg_resources==0.0.0
ratelim==0.1.6
requests==2.31.0
RPi.GPIO==0.7.1
six==1.16.0
smbus2==0.4.3
soupsieve==2.5
spidev==3.6
urllib3==2.2.0
```

## Usage

### CLI

```
$ pimo -h
usage: pimo [-h] [-v] [-vv] {set,s} ...

positional arguments:
  {set,s}

optional arguments:
  -h, --help           show this help message and exit
  -v, --verbose        set loglevel to INFO
  -vv, --very-verbose  set loglevel to DEBUG
```

### Sub Commands

#### `set`

```
$ pimo set --help
usage: pimo set [-h] [--saturation SATURATION] [--show-path] [--ascii-art] --frame-orientation {square,portrait,landscape,portrait_reverse,landscape_reverse} [--match-aspect]
                [--expand] [--border BORDER] [--border-color BORDER_COLOR BORDER_COLOR BORDER_COLOR BORDER_COLOR]
                [--background-color BACKGROUND_COLOR BACKGROUND_COLOR BACKGROUND_COLOR] [--moon-shadow-opacity MOON_SHADOW_OPACITY]
                [-f FROM_FILE | -t | --moon-clock MOON_CLOCK | -g | -d]

optional arguments:
  -h, --help            show this help message and exit
  --saturation SATURATION, -sat SATURATION
                        Saturation factor (0.0-1.0)
  --show-path, -p       Burn path onto image.
  --ascii-art, -a       Log AsciiArt image previews.
  --frame-orientation {square,portrait,landscape,portrait_reverse,landscape_reverse}, -o {square,portrait,landscape,portrait_reverse,landscape_reverse}
                        Frame Orientation: square,portrait,landscape,portrait_reverse,landscape_reverse
  --match-aspect, -m    Force image aspect ratio to match Frame Orientation
  --expand, -e          Expand image to cover full frame
  --border BORDER, -b BORDER
                        Add border around image
  --border-color BORDER_COLOR BORDER_COLOR BORDER_COLOR BORDER_COLOR, -bc BORDER_COLOR BORDER_COLOR BORDER_COLOR BORDER_COLOR
                        Set border color (RGBA tuple). Default is transparent.
  --background-color BACKGROUND_COLOR BACKGROUND_COLOR BACKGROUND_COLOR, -bg BACKGROUND_COLOR BACKGROUND_COLOR BACKGROUND_COLOR
                        Set background color (RGB tuple).
  --moon-shadow-opacity MOON_SHADOW_OPACITY, -s MOON_SHADOW_OPACITY
                        Black dial background or transparent. (0<=moon-shadow<=255).
  -f FROM_FILE, --from-file FROM_FILE
                        Set an image from file.
  -t, --test-bars       Set a test bar image.
  --moon-clock MOON_CLOCK, -c MOON_CLOCK
                        Display moon-clock based on location
  -g, --from-gdrive     Set a random image from GDrive. Defaults to /data/GDRIVE/media/images/scan/processed
  -d, --from-local-directory
                        Set a random image from local directory. Defaults to /home/pi/images
```

## Examples

### moode-oroni

https://github.com/michimussato/moode-oroni/blob/main/README.md

From Google Drive

```shell
pimo -v s -g -o landscape_reverse -m -e -a -p
```

Set a `moon-clock`

```shell
pimo -v s -tz "Australia/Sydney" -c "Sydney" -o landscape_reverse -b 40 -bc 255 0 0 255 -bg 255 0 0
```

### frame-oroni

https://github.com/michimussato/moode-oroni/blob/main/README_INKY_RASPIOS.md

#### frame landscape (frame-vertical)

```shell
pimo -v s -d -o landscape -m -e -a -p
```

#### frame portrait (frame)

```shell
pimo -v s -d -o portrait -m -e -a -p
```

## pre-commit

- https://pre-commit.com/
- https://pre-commit.com/hooks.html

## nox

```shell
nox --no-error-on-missing-interpreters --report .nox-report.json
```

## SBOM

[JSON](.sbom)

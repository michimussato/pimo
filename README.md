<!-- TOC -->
* [pimo](#pimo)
  * [venv](#venv)
  * [Installation](#installation)
    * ["setup.py" not found.](#setuppy-not-found)
  * [Usage](#usage)
    * [CLI](#cli)
    * [Sub Commands](#sub-commands)
      * [`set`](#set)
  * [Examples](#examples)
    * [moode-oroni](#moode-oroni)
    * [frame-oroni](#frame-oroni)
<!-- TOC -->

---

# pimo

## venv

```shell
source ~/venvs/inky/bin/activate
```

## Installation

```shell
pip install git+https://github.com/michimussato/pimo.git
```

### "setup.py" not found.

```
$ pip install -e .
ERROR: File "setup.py" not found. Directory cannot be installed in editable mode: /home/pi/git/pimo
(A "pyproject.toml" file was found, but editable mode currently requires a setup.py based build.)
```

```shell
pip install pip --upgrade
```

## Usage

### CLI

```
$ pimo --help
Detected 7-Colour (UC8159)
Detected 7-Colour (UC8159)
Detected 7-Colour (UC8159)
Detected 7-Colour (UC8159)
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
$ pimo s --help
Detected 7-Colour (UC8159)
Detected 7-Colour (UC8159)
Detected 7-Colour (UC8159)
Detected 7-Colour (UC8159)
usage: pimo set [-h] [--saturation SATURATION] [--show-path SHOW_PATH] --frame-orientation {square,portrait,landscape,portrait_reverse,landscape_reverse} [--force-aspect] [-f FROM_FILE | -t | -g | -d]

optional arguments:
  -h, --help            show this help message and exit
  --saturation SATURATION, -sat SATURATION
                        Saturation factor (0.0-1.0)
  --show-path SHOW_PATH, -p SHOW_PATH
                        Burn path onto image.
  --frame-orientation {square,portrait,landscape,portrait_reverse,landscape_reverse}, -o {square,portrait,landscape,portrait_reverse,landscape_reverse}
                        Frame Orientation: square,portrait,landscape,portrait_reverse,landscape_reverse
  --force-aspect, -a    Force image aspect ratio to match Frame Orientation
  -f FROM_FILE, --from-file FROM_FILE
                        Set an image from file.
  -t, --test-bars       Set a test bar image.
  -g, --from-gdrive     Set a random image from GDrive.
  -d, --from-local-directory
                        Set a random image from local directory.
```

## Examples

### moode-oroni

https://github.com/michimussato/moode-oroni/blob/main/README.md

```shell
pimo -v s -g -o landscape_reverse -a
```

```shell
pimo -v s -t -o landscape_reverse
```

### frame-oroni

https://github.com/michimussato/moode-oroni/blob/main/README_INKY_RASPIOS.md

TBD

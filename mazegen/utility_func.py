import time
from math import sqrt
from typing import Any
from sys import argv

# ██████ ▄▄ ▄▄ ▄▄  ▄▄  ▄▄▄▄ ▄▄▄▄▄▄ ▄▄  ▄▄▄  ▄▄  ▄▄  ▄▄▄▄
# ██▄▄   ██ ██ ███▄██ ██▀▀▀   ██   ██ ██▀██ ███▄██ ███▄▄
# ██     ▀███▀ ██ ▀██ ▀████   ██   ██ ▀███▀ ██ ▀██ ▄▄██▀


def to_colhex(r: int | float, g: int | float,
              b: int | float, a: int | float = 255) -> int:
    r = int(r)
    g = int(g)
    b = int(b)
    a = int(a)
    color = 0
    color = color | (a << 24)
    color = color | (r << 16)
    color = color | (g << 8)
    color = color | (b << 0)
    return (color)


def magnitude(x1: int, y1: int, x2: int, y2: int) -> int:
    val = (x2 - x1)**2 + (y2 - y1)**2
    if val < 0:
        val *= -1
    val = int(sqrt(val))
    return val if val >= 0 else val * -1


def funny_magnitude(x1: int, y1: int, x2: int, y2: int) -> int:
    val = (int(sqrt((x1 * x1 + y1 * y1)) -
               sqrt((x2 * x2 + y2 * y2))))
    return val


def wait(val: int | float) -> None:
    start = time.time()
    while (time.time() - start < val):
        pass


def parse_configs() -> dict[str, Any]:
    configs: dict[str, Any] = dict()
    key = ""
    val: Any = None
    iskey = True
    active = True
    with open(argv[1], "r") as settings:
        for char in settings.read():
            if char == "#":
                active = False
                continue
            if char == '\n' or char == '':
                if val is None and active is True and key != "":
                    raise Exception("Invalid config file: KEY=VALUE expected")
                if val == "True":
                    val = True
                elif val == "False":
                    val = False
                configs.update({key.lower(): val})
                iskey = True
                active = True
                key = ""
                val = None
                continue
            if active is False:
                continue
            if char == " ":
                continue
            if char == "=" and iskey is True:
                val = 0
                iskey = False
                continue
            if iskey is True:
                key += char
            else:
                if char == "," and not isinstance(val, list):
                    val = [val]
                    val.append(0)
                    continue
                elif char == ",":
                    val.append(0)
                    continue
                else:
                    if isinstance(val, int):
                        try:
                            int(char)
                            val *= 10
                            val += int(char)
                        except ValueError:
                            val = ""
                            val = str(val) + char
                    elif isinstance(val, str):
                        val += char
                    elif char == "-" and isinstance(val, list):
                        val[len(val) - 1] *= -1
                    else:
                        int(char)
                        val[len(val) - 1] *= 10
                        val[len(val) - 1] += int(char)
    if val is None and active is True and key != "":
        raise Exception(f"Invalid config file: KEY=VALUE expected {key}")
    if val == "True":
        val = True
    elif val == "False":
        val = False
    configs.update({key.lower(): val})
    iskey = True
    active = True
    key = ""
    val = None
    return configs

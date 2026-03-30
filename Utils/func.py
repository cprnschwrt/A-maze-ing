import time
from math import sqrt


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

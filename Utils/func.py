import time
from math import sqrt


def to_colhex(r, g, b, a: int = 255) -> int:
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


def magnitude(x1, y1, x2, y2) -> int:
    val = (x2 - x1)**2 + (y2 - y1)**2
    if val < 0:
        val *= -1
    val = int(sqrt(val))
    return val if val >= 0 else val * -1


def funny_magnitude(x1, y1, x2, y2) -> int:
    val = (int(sqrt((x1 * x1 + y1 * y1)) -
               sqrt((x2 * x2 + y2 * y2))))
    return val


def wait(val: int) -> None:
    start = time.time()
    while (time.time() - start < val):
        pass

from pydantic import BaseModel, model_validator
from math import floor
from mlx import Mlx


icon4 = (
    "SX",
    "ES",
    "XX"
    )

icon2 = (
    "ES",
    "SW",
    "ES"
)


def color(message: any, tcol: tuple = (255, 255, 255),
          bcol: tuple = None,
          bold: bool = False, ita: bool = False, under: bool = False,
          finish: str = '\n', f: any = None) -> None:
    if tcol is None:
        tcol = (255, 255, 255)
    style = "1;" if bold else ""
    italic = "3;" if ita else ""
    underline = "4;" if under else ""
    bcolor = f"48;2;{bcol[0]};{bcol[1]};{bcol[2]};" if bcol else ""
    style = bcolor+style+italic+underline
    if (type(message) is dict or type(message) is list):
        for mes in message:
            print(f"\033[{style}38;2;{tcol[0]};{tcol[1]};{tcol[2]}"
                  f"m{mes}\033[0m", end=finish, file=f)
            print("")
    else:
        print(f"\033[{style}38;2;{tcol[0]};{tcol[1]};{tcol[2]}"
              f"m{message}\033[0m",
              end=finish, file=f)


class Vector2(BaseModel):
    x: int
    y: int

    def __str__(self):
        return f"{self.x, self.y}"


class MazePart():
    def __init__(self, pos: Vector2):
        self.position: Vector2 = pos
        self.active: bool = True
        self.N: int = 1
        self.S: int = 1
        self.E: int = 1
        self.W: int = 1


wall = "██"
door = "  "


def get_slot_print(self, x: int, y: int, grid: int,
                   size: int, line: int) -> str:
    p1, p2, p3 = wall, wall, wall

    currentX = x % (3 + size)
    currentY = y % (3 + size)

    return p1 + p2 + p3


class MazeGrid(BaseModel):
    x: int
    y: int
    objects: list = []

    @model_validator(mode="after")
    def init(self):
        for y in range(self.y):
            list.append(self.objects, [])
            for x in range(self.x):
                list.append(self.objects[y], [])
                self.objects[y][x] = MazePart(Vector2(x=x, y=y))
        return self

    def display(self) -> None:
        size = 3
        for line in range(size):
            for y in range(self.y):
                for grid in range(3):
                    printed = False
                    for x in range(self.x):
                        toprint = get_slot_print(self, x, y, grid, size, line)
                        color(toprint, (0, 0, 255), bcol=(105, 105, 255),
                              finish="")
                        if toprint != "":
                            printed = True
                if printed:
                    print()

    def getCell(self, x, y) -> None:
        return self.objects[x][y].W

    def __len__(self):
        return f"{self.x, self.y}"


grid = MazeGrid(x=5, y=5)
grid.display()

m = Mlx()
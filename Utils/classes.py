from pydantic import BaseModel, model_validator
from typing import Any


class Vector2(BaseModel):
    x: int
    y: int

    def __str__(self) -> str:
        return f"{self.x, self.y}"


class MazePart():
    def __init__(self, pos: Vector2):
        self.position: Vector2 = pos
        self.active: bool = True
        self.N: int = 1
        self.S: int = 1
        self.E: int = 1
        self.W: int = 1
        self.Status: str | None | int = None
        self.checked: bool = False


def check_next(direc: str, cell: MazePart, maze: Any) -> None:
    from algo_backtrack_recursive import get_oppposite, update_cell
    directions: dict = {"N": -1, "S": 1, "E": 1, "W": -1}
    x, y = cell.position.x, cell.position.y
    direc = get_oppposite(direc)
    targ = None
    dir = directions.get(direc) or 0
    if direc == "N" or direc == "S":
        targ = maze.objects[y - dir][x]
    else:
        targ = maze.objects[y][x - dir]
    update_cell(targ, direc)
    targ.Status = 42
    targ.checked = True


def check_char(char: str, cell: MazePart, maze: Any) -> None:
    if char == "S":
        cell.S = 0
        cell.checked = True
        cell.Status = 42
    elif char == "E":
        cell.E = 0
        cell.checked = True
        cell.Status = 42
    elif char == "W":
        cell.W = 0
        cell.checked = True
        cell.Status = 42
    elif char == "N":
        cell.N = 0
        cell.checked = True
        cell.Status = 42
    elif char == "O":
        cell.checked = True
        cell.Status = 42
    if char != "O" and char != "X":
        check_next(char, cell, maze)


class MazeGrid(BaseModel):
    x: int
    y: int
    objects: list = []

    @model_validator(mode="after")
    def start(self: Any) -> Any:
        for y in range(self.y):
            list.append(self.objects, [])
            for x in range(self.x):
                list.append(self.objects[y], [])
                self.objects[y][x] = MazePart(Vector2(x=x, y=y))
        if self.x >= 8 and self.y >= 7:
            self.make42()
        return self

    def make42(self: Any) -> None:
        icon4 = ("SS",
                 "ES",
                 "XO")

        icon2 = ("ES",
                 "SW",
                 "EO")

        targX = int((self.x - 4) / 2)
        targY = int((self.y - 3) / 2)
        for line in range(len(icon4)):
            for idx in range(len(icon4[line])):
                cell = self.objects[targY + line][targX + idx]
                char = icon4[line][idx]
                check_char(char, cell, self)
        for line in range(len(icon2)):
            for idx in range(len(icon2[line])):
                cell = self.objects[targY + line][targX + idx + 2]
                char = icon2[line][idx]
                check_char(char, cell, self)

    def __len__(self: Any) -> Any:
        return self.x * self.y

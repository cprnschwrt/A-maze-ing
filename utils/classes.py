from pydantic import BaseModel, model_validator
from display_strings import StringDisplay

class Vector2(BaseModel):
    x: int
    y: int

    def __str__(self):
        return f"{self.x, self.y}"


class MazePart():
    def __init__(self, pos: Vector2):
        self.position: Vector2 = pos
        self.active: bool = True
        self.N: int = 0
        self.S: int = 0
        self.E: int = 0
        self.W: int = 0


wall = "██"
door = "  "


def get_slot_print(self, x: int, y: int, line: int) -> str:
    p1 = wall
    p2 = wall
    p3 = wall

    current = self.objects[x][y]

    modulo = 3
    modx = x % modulo
    mody = y % modulo

    if line == 0 and current.N == 1:
        p2 = door
    if line == 1 and current.E:
        p1 = door
    if line == 1 and current.W:
        p3 = door
    if line == 2 and current.S:
        p2 = door

    if line == 1:
        p2 = door
    if 0 < x < self.x and line == 0:
        p1, p2, p3 = "", "", ""
    if 0 < y < self.y:
        p1 = ""

    return p1 + p2 + p3


class MazeGrid(BaseModel):
    x: int
    y: int
    objects: list = []

    @model_validator(mode="after")
    def init(self):
        for x in range(self.x):
            list.append(self.objects, [])
            for y in range(self.y):
                list.append(self.objects[x], [])
                self.objects[x][y] = MazePart(Vector2(x=x, y=y))
        return self

    def display(self) -> None:
        for x in range(self.x):
            for i in range(3):
                printed = False
                for y in range(self.y):
                    toprint = get_slot_print(self, x, y, i)
                    print(toprint, end="")
                    if toprint != "":
                        printed = True
                if printed:
                    print()

    def getCell(self, x, y) -> None:
        return self.objects[x][y].N

    def __len__(self):
        return f"{self.x, self.y}"


grid = MazeGrid(x=10, y=10)
grid.objects[4][5].S = 1
grid.objects[4][5].W = 1
grid.objects[3][5].W = 1
grid.objects[3][5].S = 1
grid.display()

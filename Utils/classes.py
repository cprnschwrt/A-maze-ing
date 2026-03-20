from pydantic import BaseModel, model_validator
import random


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
        self.Status = None
        self.checked: bool = False
        self.x = pos.x
        self.y = pos.y


def check_char(char: str, cell: MazePart) -> None:
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


class MazeGrid(BaseModel):
    x: int
    y: int
    objects: list = []

    @model_validator(mode="after")
    def start(self):
        for y in range(self.y):
            list.append(self.objects, [])
            for x in range(self.x):
                list.append(self.objects[y], [])
                self.objects[y][x] = MazePart(Vector2(x=x, y=y))
        if self.x >= 8 and self.y >= 7:
            self.make42()
        return self

    def make42(self):
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
                check_char(char, cell)
        for line in range(len(icon2)):
            for idx in range(len(icon2[line])):
                cell = self.objects[targY + line][targX + idx + 2]
                char = icon2[line][idx]
                check_char(char, cell)

    def __len__(self):
        return f"{self.x, self.y}"

    def generate_maze(self):
        start_cell = self.objects[0][0]
        stack = [start_cell]
        start_cell.checked = True
        print("Maze Generation Started")

        directions = [(0, -1, 'N'), (0, 1, 'S'), (-1, 0, 'W'), (1, 0, 'E')]

        while stack:
            current_cell = stack[-1]
            neighbors = []

            for dx, dy, direction in directions:
                nx, ny = current_cell.x + dx, current_cell.y + dy
                if 0 <= nx < self.x and 0 <= ny < self.y \
                    and self.objects[ny][nx].checked is False \
                        and self.objects[ny][nx].Status != 42:
                    neighbors.append((nx, ny, direction))

            if neighbors:
                nx, ny, direction = random.choice(neighbors)
                next_cell = self.objects[ny][nx]

                if direction == 'N':
                    current_cell.N = 0
                    next_cell.S = 0
                elif direction == 'S':
                    current_cell.S = 0
                    next_cell.N = 0
                elif direction == 'E':
                    current_cell.E = 0
                    next_cell.W = 0
                elif direction == 'W':
                    current_cell.W = 0
                    next_cell.E = 0

                next_cell.checked = True
                stack.append(next_cell)
            else:
                stack.pop()

        print("Maze Generation Finished")

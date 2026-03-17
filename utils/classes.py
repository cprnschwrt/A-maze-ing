from pydantic import BaseModel, model_validator
from utils.hexa import binar_cell, hexa_grid
import random


class Vector2(BaseModel):
    x: int
    y: int
    def __str__(self):
        return f"{self.x, self.y}"


class MazePart():
    def __init__(self, pos: Vector2):
        self.position: Vector2 = pos
        self.active: bool = True
        self.N = 0
        self.S = 0
        self.E = 0
        self.W = 0


wall = "██"
door = "  "

CLR_END = "\033[0m"


def random_base_colour():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b


def random_gradation(r_base, g_base, b_base, x_pos, y_pos, width, height):
    r = int(r_base + (255 - r_base) * (x_pos / max(1, height - 1)))
    g = int(g_base + (255 - g_base) * (y_pos / max(1, width - 1)))
    b = int(b_base)
    return f"\033[38;2;{r};{g};{b}m"


def get_slot_print(self, x: int, y: int, line: int) -> str:
    current = self.objects[x][y]
    p1 = wall
    p2 = wall
    p3 = wall

    # maze doors
    if line == 0 and current.N:
        p2 = door
    if line == 1:
        if current.W:
            p3 = door
        if current.E:
            p1 = door
        p2 = door
    if line == 2 and current.S:
        p2 = door

    # pattern
    if (x, y) in motif_cells:
        x_step = x - motif_px
        y_step = y - motif_py
        color = random_gradation(
            r0, g0, b0, 
            x_step, y_step,
            width=len(ft_pattern[0]),
            height=len(ft_pattern))
        if p1 == door:
            p1 = f"{color}██{CLR_END}"
        if p2 == door:
            p2 = f"{color}██{CLR_END}"
        if p3 == door:
            p3 = f"{color}██{CLR_END}"

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
            self.objects.append([])
            for y in range(self.y):
                self.objects[x].append(MazePart(Vector2(x=x, y=y)))
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


max_x = 5
max_y = 7
grid = MazeGrid(x=max_x, y=max_y)

ft_pattern = ["C04084", "C084C0", "00009"]
motif_height = len(ft_pattern) + 1
motif_width = len(ft_pattern[0])

r0, g0, b0 = random_base_colour()

motif_px = random.randint(0, grid.x - motif_height)
motif_py = random.randint(0, grid.y - motif_width)

motif_cells = [
    (motif_px + x, motif_py + y)
    for x in range(len(ft_pattern))
    for y in range(len(ft_pattern[0]))]

for x, line in enumerate(ft_pattern):
    for y, hex_char in enumerate(line):
        binar_cell(grid, motif_px + x, motif_py + y, hex_char)

hex_lines = hexa_grid(grid)
for hx, line in enumerate(hex_lines):
    colored_line = ""
    for hy, c in enumerate(line):
        if (hx, hy) in motif_cells:
            x_step = hx - motif_px
            y_step = hy - motif_py
            color = random_gradation(
                r0, g0, b0, 
                x_step, y_step, 
                width=len(ft_pattern[0]), 
                height=len(ft_pattern))
            colored_line += f"{color}{c}{CLR_END}"
        else:
            colored_line += c
    print(colored_line)

grid.display()
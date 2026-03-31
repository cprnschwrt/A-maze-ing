from pydantic import BaseModel, model_validator
from typing import Any, Callable, Generator
from random import randint, seed
from .utility_func import parse_configs

# ▄█████ ▄▄     ▄▄▄   ▄▄▄▄  ▄▄▄▄ ▄▄▄▄▄  ▄▄▄▄
# ██     ██    ██▀██ ███▄▄ ███▄▄ ██▄▄  ███▄▄
# ▀█████ ██▄▄▄ ██▀██ ▄▄██▀ ▄▄██▀ ██▄▄▄ ▄▄██▀


class Vector2(BaseModel):
    """ 2D vector composed of x and y """
    x: int
    y: int

    def __str__(self) -> str:
        return f"{self.x, self.y}"


class MazePart():
    """A cell used for a maze grid"""
    def __init__(self, pos: Vector2):
        self.position: Vector2 = pos
        self.active: bool = True
        self.N: int = 1
        self.S: int = 1
        self.E: int = 1
        self.W: int = 1
        self.Status: str | None | int = None
        self.checked: bool = False

    def update_cell(self, target: str) -> str:
        """Update the cell's wall based on the direction sent"""
        if target == "N":
            self.N = 0
            return "S"
        elif target == "S":
            self.S = 0
            return "N"
        elif target == "E":
            self.E = 0
            return "W"
        elif target == "W":
            self.W = 0
            return "E"
        return ""


class MazeGrid(BaseModel):
    """A maze that generate it self and output it as a file."""
    x: int = 0
    y: int = 0
    objects: list[Any] = []
    algo: Callable[[Any, Vector2, bool], Generator[None]]
    step: Any = None
    count: int = 0
    entry: Vector2 = Vector2(x=0, y=0)
    exit: Vector2 = Vector2(x=1, y=1)
    seed: int = -1
    visualize: bool = False
    settings: dict[str, Any] = {}
    output: str = "maze.txt"
    perfect: bool = False
    visualizer: Any
# Setup

    @model_validator(mode="after")
    def start(self: Any) -> Any:
        """Initialize and start the maze generation."""
        self.verif()
        seed(self.seed)
        self.count = 0
        if self.visualize is True:
            self.visualizer(self, self.settings)
        else:
            while self.step is not None:
                self.generate_step()
            print(f"Maze generated in {self.count} moves")
            self.save()
        return self

    def clear_cells(self) -> None:
        for y in range(self.y):
            list.append(self.objects, [])
            for x in range(self.x):
                list.append(self.objects[y], [])
                self.objects[y][x] = MazePart(Vector2(x=x, y=y))

    def save(self) -> None:
        """Save the maze's data as a file."""
        vals = self.get_shortest_path(self.entry, self.exit)
        if vals[0] is None:
            print("Exit not found.")
            return
        cells = vals[0]
        path = vals[1]
        for pos in cells:
            self.objects[pos.y][pos.x].Status = "path"
        print("Generation completed.")
        hex = self.hexa_grid()
        with open(self.output, "w") as file:
            for line in hex:
                file.write(line + "\n")
            file.write("\n")
            file.write(f"{self.entry.y}, {self.entry.x}\n")
            file.write(f"{self.exit.y}, {self.exit.x}\n")
            file.write(f"{path}\n")

    def verif(self) -> None:
        """Parse and verify the settings sent.\n
        --> No settings will result in default settings"""

        self.settings = parse_configs()
        settings = self.settings
        x, y = 20, 20
        try:
            self.y = settings["height"]
        except KeyError:
            pass
        try:
            self.x = settings["width"]
        except KeyError:
            pass
        self.clear_cells()
        try:
            self.entry = Vector2(x=settings["entry"][0] - 1,
                                 y=settings["entry"][1] - 1)
        except KeyError:
            self.entry = Vector2(x=0, y=0)

        try:
            self.exit = Vector2(x=settings["exit"][0] - 1,
                                y=settings["exit"][1] - 1)
        except KeyError:
            self.exit = Vector2(x=x-1, y=x-1)

        try:
            self.visualize = settings["visualize"]
        except KeyError:
            self.visualize = False

        try:
            self.seed = settings["seed"]
        except KeyError:
            pass

        try:
            self.perfect = settings["perfect"]
        except KeyError:
            pass

        if self.x >= 8 and self.y >= 7:
            self.make42()
        if (self.entry.x > self.x or
                self.entry.y > self.y):
            print("Invalid Entry Point ! Exit is out of bound.")
            raise ValueError
        elif (self.exit.x > self.x or
                self.exit.y > y):
            print("Invalid Exit Point ! Exit is out of bound.")
            raise ValueError
        elif (self.objects[self.entry.y][self.entry.x].Status == 42):
            print("Invalid Entry Point ! Position conflict with 42 icon.")
            raise ValueError
        elif (self.objects[self.exit.y][self.exit.x].Status == 42):
            print("Invalid Exit Point ! Position conflict with 42 icon.")
            raise ValueError
        elif (self.entry.y == self.exit.y and self.entry.x == self.exit.x):
            print("Invalid Exit And Entry Point ! "
                  "Position conflict with each others.")
            raise ValueError
        if self.seed == -1:
            self.seed = randint(0, randint(1, 1000000000))
        self.step = self.algo(self, self.entry, perfect=self.perfect)

# Generation

    def make42(self: Any) -> None:
        """Generate closed 42 shaped cells at the center of the maze"""
        icon4 = ("SS",
                 "ES",
                 "XO")

        icon2 = ("ES",
                 "SW",
                 "EO")

        targX = int((self.x - 3) / 2)
        targY = int((self.y - 4) / 2)
        for line in range(len(icon4)):
            for idx in range(len(icon4[line])):
                cell = self.objects[targY + line][targX + idx]
                char = icon4[line][idx]
                self.check_char(char, cell)
        for line in range(len(icon2)):
            for idx in range(len(icon2[line])):
                cell = self.objects[targY + line][targX + idx + 2]
                char = icon2[line][idx]
                self.check_char(char, cell)

    def generate_step(self) -> None:
        """Step into the maze generation and increment the count."""
        self.step = next(self.step)
        self.count += 1

    def hexa_grid(self) -> list[str]:
        """Return the maze as hexadecimal values."""
        result = []
        for y in range(self.y):
            row = []
            for x in range(self.x):
                row.append(hexa_cell(self.objects[y][x]))
            result.append("".join(row))
        return result

    def get_shortest_path(self, position: Vector2,
                          target: Vector2, trail: list[Vector2] | None = None,
                          origin: str = "", current_path: str = "",
                          current: list[MazePart] | None = None,
                          path: str = "") -> Any:
        """Find the shortest path possible in the maze.\n
        Returns a list of cells and a string of movements"""
        if trail is None:
            trail = []
        directions: dict[str, int] = {"N": -1, "S": 1, "E": 1, "W": -1}
        cell = self.objects[position.y][position.x]
        for val in trail:
            if val == position:
                return current, current_path
        trail.append(position)
        if current is not None and len(trail) > len(current):
            return current, current_path
        if position == target:
            return trail, path
        re: list[MazePart] | None = None
        fpath = ""
        for key in directions:
            value: int = directions.get(key) or 0
            if cell.__dict__.get(key) == 0 and key != get_oppposite(origin):
                temp_path = path + key
                if key == "E" or key == "W":
                    re, fpath = self.get_shortest_path(Vector2(
                                                       x=position.x + value,
                                                       y=position.y),
                                                       target,
                                                       trail.copy(),
                                                       key, current_path,
                                                       current,
                                                       temp_path)
                if key == "S" or key == "N":
                    re, fpath = self.get_shortest_path(Vector2(x=position.x,
                                                       y=position.y + value),
                                                       target,
                                                       trail.copy(), key,
                                                       current_path,
                                                       current,
                                                       temp_path)
                if re is not None:
                    current = re
                    current_path = fpath
        return current, current_path

    def __len__(self: Any) -> Any:
        return self.x * self.y

# Manipulation

    def check_next(self, direc: str, cell: MazePart) -> None:
        """Go inside the cells from a direction and define it as checked"""
        directions: dict[str, int] = {"N": -1, "S": 1, "E": 1, "W": -1}
        x, y = cell.position.x, cell.position.y
        direc = get_oppposite(direc)
        targ = None
        dir = directions.get(direc) or 0
        if direc == "N" or direc == "S":
            targ = self.objects[y - dir][x]
        else:
            targ = self.objects[y][x - dir]
        targ.update_cell(direc)
        targ.Status = 42
        targ.checked = True

    def check_char(self, char: str, cell: MazePart) -> None:
        """Open walls of a decided cell"""
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
            self.check_next(char, cell)

    def get_cell(self, direction: str,
                 position: Vector2, val: Any) -> Any:
        """Find the cells based on direcion and return it.\n
        Return None if no cells are found"""
        next = None
        pos = position
        if direction == "N" or direction == "S":
            posY = pos.y + val
            if not posY < 0 and not posY >= self.y:
                next = self.objects[posY][pos.x]
        elif direction == "E" or direction == "W":
            posX = pos.x + val
            if not posX < 0 and not posX >= self.x:
                next = self.objects[pos.y][posX]
        return (next)

# ██████ ▄▄ ▄▄ ▄▄  ▄▄  ▄▄▄▄ ▄▄▄▄▄▄ ▄▄  ▄▄▄  ▄▄  ▄▄  ▄▄▄▄
# ██▄▄   ██ ██ ███▄██ ██▀▀▀   ██   ██ ██▀██ ███▄██ ███▄▄
# ██     ▀███▀ ██ ▀██ ▀████   ██   ██ ▀███▀ ██ ▀██ ▄▄██▀


def hexa_cell(cell: MazePart) -> str:
    val = 0
    if cell.W:
        val |= 8
    if cell.S:
        val |= 4
    if cell.E:
        val |= 2
    if cell.N:
        val |= 1
    return hex(val)[2:].upper()


def binar_cell(grid: MazeGrid, x: int, y: int, hex_val: str) -> None:
    if x < 0 or x >= len(grid.objects) or y < 0 or y >= len(grid.objects[0]):
        raise IndexError(f"Les indices (x={x}, y={y}) sont hors de la grille.")

    val = int(hex_val, 16)
    cell = grid.objects[x][y]

    cell.N = 1 if val & 1 else 0
    cell.E = 1 if val & 2 else 0
    cell.S = 1 if val & 4 else 0
    cell.W = 1 if val & 8 else 0


def get_oppposite(target: str) -> str:
    if target == "N":
        return "S"
    elif target == "S":
        return "N"
    elif target == "E":
        return "W"
    elif target == "W":
        return "E"
    return ""

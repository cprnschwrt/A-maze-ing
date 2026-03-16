from Utils.classes import MazeGrid, MazePart, Vector2
from random import choice
from Utils.func import wait
from mlx_screen import update_cell_frame


wait_time = 0


def check_cell(cell: MazeGrid) -> bool:
    if cell is None:
        return False
    elif cell.checked is True:
        return False
    return True


def update_cell(cell: MazePart, target: str) -> str:
    if target == "N":
        cell.N = 0
        return "S"
    elif target == "S":
        cell.S = 0
        return "N"
    elif target == "E":
        cell.E = 0
        return "W"
    elif target == "W":
        cell.W = 0
        return "E"


def backtracking_recursive(self, maze: MazeGrid, startingpos: Vector2, r = None, comefrom=None) -> None:
    directions = {"N": -1, "S": 1, "E": 1, "W": -1}

    def step(parent) -> None:
        pos = startingpos
        cell = maze.objects[pos.y][pos.x]
        cell.checked = True
        if comefrom is not None:
            directions.pop(comefrom)
            update_cell(cell, comefrom)
        while len(directions) > 0:
            next: MazePart = None
            targ = choice(list(directions.items()))
            direction, val = targ[0], targ[1]
            directions.pop(direction)
            if direction == "N" or direction == "S":
                posY = pos.y + val
                if not posY < 0 and not posY >= maze.y:
                    next = maze.objects[posY][pos.x]
            elif direction == "E" or direction == "W":
                posX = pos.x + val
                if not posX < 0 and not posX >= maze.x:
                    next = maze.objects[pos.y][posX]
            if check_cell(next):
                newpos = next.position
                revdirec = update_cell(cell, direction)
                wait(wait_time)
                update_cell_frame(self, pos.x, pos.y)
                yield backtracking_recursive(self, maze, newpos, root, revdirec)
        yield parent
        if parent:
            parent.close()
    root = step(r)
    return root

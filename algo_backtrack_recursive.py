from Utils.classes import MazeGrid, MazePart, Vector2
from random import choice
from Utils.func import wait
from typing import Generator, Any

wait_time = 1/60


def check_cell(cell: MazePart) -> bool:
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
    return ""


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


def get_cell(self: Any, direction: str, position: Vector2, val: Any) -> Any:
    next = None
    pos = position
    if direction == "N" or direction == "S":
        posY = pos.y + val
        if not posY < 0 and not posY >= self.maze.y:
            next = self.maze.objects[posY][pos.x]
    elif direction == "E" or direction == "W":
        posX = pos.x + val
        if not posX < 0 and not posX >= self.maze.x:
            next = self.maze.objects[pos.y][posX]
    return (next)


def backtracking_recursive(self: Any, maze: MazeGrid, startingpos: Vector2,
                           parent: Any = None, comefrom: str | None = None,
                           perfect: bool = False) -> Any:
    directions: dict = {"N": -1, "S": 1, "E": 1, "W": -1}
    Dupdirections: dict[str, int] = {"N": -1, "S": 1, "E": 1, "W": -1}

    def step() -> Generator[None]:
        pos = startingpos
        cell = maze.objects[pos.y][pos.x]
        cell.checked = True
        changed = False

        if comefrom is not None:
            directions.pop(comefrom)
            update_cell(cell, comefrom)

        while len(directions) > 0:
            targ = choice(list(directions.items()))
            direction, val = targ[0], targ[1]
            directions.pop(direction)
            nextcell: MazePart = get_cell(self, direction, pos, val)
            if check_cell(nextcell):
                changed = True
                newpos = nextcell.position
                revdirec = update_cell(cell, direction)
                child = backtracking_recursive(self, maze, newpos, root,
                                               revdirec, perfect=perfect)
                wait(wait_time)
                yield child
                if child is not None:
                    child.close()
        if comefrom is not None and changed is False:
            tmpcell = get_cell(self, get_oppposite(comefrom), pos,
                               Dupdirections.get(get_oppposite(comefrom)))
            if perfect is False \
                    and tmpcell is not None \
                    and not tmpcell.Status == 42:
                update_cell(cell, get_oppposite(comefrom))
                update_cell(tmpcell, comefrom)
        if parent is not None:
            yield parent
        else:
            yield None

    root = step()
    return root

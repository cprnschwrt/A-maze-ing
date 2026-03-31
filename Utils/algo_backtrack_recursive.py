from .mazeclass import MazeGrid, MazePart, Vector2
from .utility_func import wait
from random import choice
from typing import Generator, Any

# ██████ ▄▄ ▄▄ ▄▄  ▄▄  ▄▄▄▄ ▄▄▄▄▄▄ ▄▄  ▄▄▄  ▄▄  ▄▄  ▄▄▄▄
# ██▄▄   ██ ██ ███▄██ ██▀▀▀   ██   ██ ██▀██ ███▄██ ███▄▄
# ██     ▀███▀ ██ ▀██ ▀████   ██   ██ ▀███▀ ██ ▀██ ▄▄██▀


def check_cell(cell: MazePart) -> bool:
    if cell is None:
        return False
    elif cell.checked is True:
        return False
    return True


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


def backtracking_recursive(maze: MazeGrid, startingpos: Vector2,
                           parent: Any = None, comefrom: str | None = None,
                           perfect: bool = False) -> Any:
    directions: dict[str, int] = {"N": -1, "S": 1, "E": 1, "W": -1}
    Dupdirections: dict[str, int] = {"N": -1, "S": 1, "E": 1, "W": -1}

    def step() -> Generator[None]:
        pos = startingpos
        cell = maze.objects[pos.y][pos.x]
        cell.checked = True
        changed = False

        if comefrom is not None:
            directions.pop(comefrom)
            cell.update_cell(comefrom)

        while len(directions) > 0:
            targ = choice(list(directions.items()))
            direction, val = targ[0], targ[1]
            directions.pop(direction)
            nextcell: MazePart = maze.get_cell(direction, pos, val)
            if check_cell(nextcell):
                changed = True
                newpos = nextcell.position
                revdirec = cell.update_cell(direction)
                child = backtracking_recursive(maze, newpos, root,
                                               revdirec, perfect=perfect)
                if maze.visualize is True:
                    wait(0)
                yield child
                if child is not None:
                    child.close()
        if comefrom is not None and changed is False:
            tmpcell = maze.get_cell(get_oppposite(comefrom), pos,
                                    Dupdirections.get(get_oppposite(comefrom)))
            if perfect is False \
                    and tmpcell is not None \
                    and not tmpcell.Status == 42:
                cell.update_cell(get_oppposite(comefrom))
                tmpcell.update_cell(comefrom)
        if parent is not None:
            yield parent
        else:
            yield None

    root = step()
    return root

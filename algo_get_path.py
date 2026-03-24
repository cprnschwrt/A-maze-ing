from Utils.classes import MazeGrid, MazePart
from algo_backtrack_recursive import get_oppposite
from typing import Any
directions: dict[str, int] = {"N": -1, "S": 1, "E": 1, "W": -1}


def get_shortest_path(maze: MazeGrid, position: list[int],
                      target: list[int], trail: list[list[int]] = [],
                      origin: str = "", current_path: str = "",
                      current: list[MazePart] | None = None,
                      path: str = "") -> Any:
    cell = maze.objects[position[1]][position[0]]
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
                re, fpath = get_shortest_path(maze,
                                              [position[0] + value,
                                               position[1]], target,
                                              trail.copy(), key, current_path,
                                              current,
                                              temp_path)
            if key == "S" or key == "N":
                re, fpath = get_shortest_path(maze,
                                              [position[0],
                                               position[1] + value], target,
                                              trail.copy(), key, current_path,
                                              current,
                                              temp_path)
            if re is not None:
                current = re
                current_path = fpath
    return [current, current_path]

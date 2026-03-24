#!/usr/bin/env python
from Utils.classes import MazeGrid
from sys import argv


def parse_configs():
    configs: dict = dict()
    key = ""
    val = 0
    iskey = True
    active = True
    with open(argv[1], "r") as settings:
        for char in settings.read():
            if char == "#":
                active = False
                continue
            if char == '\n':
                if val == "True":
                    val = True
                elif val == "False":
                    val = False
                if active:
                    configs.update({key.lower(): val})
                iskey = True
                active = True
                key = ""
                val = 0
                continue
            if char == " ":
                continue
            if char == "=":
                iskey = False
                continue
            if iskey is True:
                key += char
            else:
                if char == ",":
                    val = [val, 0]
                    continue
                else:
                    if isinstance(val, int):
                        try:
                            int(char)
                            val *= 10
                            val += int(char)
                        except ValueError:
                            val = ""
                            val = str(val) + char
                    elif isinstance(val, str):
                        val += char
                    else:
                        int(char)
                        val[1] *= 10
                        val[1] += int(char)
    return configs


def main() -> None:
    settings = parse_configs()
    x, y = 20, 20
    try:
        x = settings["height"],
    except KeyError:
        pass

    try:
        y = settings["width"]
    except KeyError:
        pass
    maze = MazeGrid(x=x, y=y)
    import mlx_screen
    mlx_screen.Screen(maze, settings)


if __name__ == "__main__":
    main()

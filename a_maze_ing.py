#!/usr/bin/env python
from Utils.classes import MazeGrid
from seeker_head import Screen as MazeScreen


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
    style = style+italic+underline+bcolor
    if (type(message) is dict or type(message) is list):
        for mes in message:
            print(f"\033[{style}38;2;{tcol[0]};{tcol[1]};{tcol[2]}"
                  f"m{mes}\033[0m", end=finish, file=f)
            print("")
    else:
        print(f"\033[{style}38;2;{tcol[0]};{tcol[1]};{tcol[2]}"
              f"m{message}\033[0m",
              end=finish, file=f)


def main() -> None:
    maze = MazeGrid(x=42, y=42)

    

    try:
        from mlx_screen import Screen
        Screen(maze)
    except ModuleNotFoundError:
        color("Warning: mlx not downloaded, executing without visuals.",
              (155, 155, 0), bold=True)


if __name__ == "__main__":
    main()
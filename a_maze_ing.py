#!/usr/bin/env python
from Utils.mazeclass import MazeGrid
from Utils.algo_backtrack_recursive import backtracking_recursive
from Utils.mlx_screen import Screen


def main() -> MazeGrid:
    newmaze = MazeGrid(algo=backtracking_recursive, visualizer=Screen)
    return newmaze


if __name__ == "__main__":
    main()

from mlx import Mlx
from math import floor
from Utils.classes import MazeGrid, Vector2
from Utils.func import wait
from typing import Generator
import inspect


mult = 100
steps = 0
paused = False
finished = False
startpos = Vector2(x=2, y=2)
sizemult = 1.4

def close_screen(key: int, self) -> any:
    if key == 65307:
        self.mlx.mlx_loop_exit(self.initScreen)
    elif key == 112:
        global paused
        if paused is False:
            paused = True
            print("Paused")
        else:
            paused = False
            print("Unpaused")
    elif key == 65363:
        render(self, True)
    else:
        print(key)


def show_grid(self) -> None:
    cell_size = int(floor(mult / 2))
    cell_dimention = int(cell_size * sizemult)
    maze = self.maze
    for y in range(maze.y):
        for x in range(maze.x):
            posX = x * mult
            posY = y * mult
            pixel(0xFF0000FF, posX, posY, self, mult)
            posX = int((x * mult) - cell_dimention / 2)
            posY = int((y * mult) - cell_dimention / 2)
            pixel(0xFF000099, posX + cell_size, posY + cell_size,
                  self, cell_dimention)


def update_cell_frame(self, x, y) -> None:
    maze: MazeGrid = self.maze
    cell = maze.objects[y][x]

    posX = x * mult
    posY = y * mult

    cell_size = int(floor(mult / 2))
    cell_dimention = int(cell_size * sizemult)

    if cell.N == 0:
        pos = (int(posX - cell_dimention / 2) + cell_size)
        pixel(0xFF000099, pos, posY - cell_size,
              self, cell_dimention)
    if cell.S == 0:
        pos = (int(posX - cell_dimention / 2) + cell_size)
        pixel(0xFF000099, pos, posY + cell_size,
              self, cell_dimention)
    if cell.E == 0:
        pos = (int(posY - cell_dimention / 2) + cell_size)
        pixel(0xFF000099, posX + cell_size, pos,
              self, cell_dimention)
    if cell.W == 0:
        pos = (int(posY - cell_dimention / 2) + cell_size)
        pixel(0xFF000099, posX - cell_size, pos,
              self, cell_dimention)


def pixel(color: int, nx: int, ny: int, self, size: int = mult) -> None:
    pixel_size = size
    image = Mlx.mlx_new_image(self.mlx, self.initScreen,
                              pixel_size, pixel_size)
    pixelbuff = Mlx.mlx_get_data_addr(self.mlx, image)
    pixelbuff = list(pixelbuff)
    for y in range(pixel_size):
        for x in range(pixel_size):
            pixel = (y * pixelbuff[2]) + (x * 4)
            pixelbuff[0][pixel] = (color) & 0xFF
            pixelbuff[0][pixel + 1] = (color >> 8) & 0xFF
            pixelbuff[0][pixel + 2] = (color >> 16) & 0xFF
            pixelbuff[0][pixel + 3] = (color >> 24)
    Mlx.mlx_put_image_to_window(self.mlx, self.initScreen, self.screen,
                                image, nx, ny)


def render(self, force: bool = False) -> None:
    maze: MazeGrid = self.maze
    global finished
    global steps
    steps += 1
    if paused is True and force is not True:
        return
    if finished == True:
        return
    if self.step is not None and inspect.getgeneratorstate(self.step) != "GEN_CLOSED":
        self.step = next(self.step)
    elif self.step is None:
        print(f"Maze Finished in {steps} steps")
        finished = True



class Screen:
    def __init__(self, maze: MazeGrid) -> None:
        from algo_backtrack_recursive import backtracking_recursive
        self.mlx = Mlx()
        self.initScreen = self.mlx.mlx_init()
        self.maze = maze
        self.screen = (
            self.mlx.mlx_new_window(
                self.initScreen,
                maze.x * mult,
                maze.y * mult,
                "A-MAZE-ING"))
        m: Mlx = self.mlx
        show_grid(self)
        self.step = backtracking_recursive(self, maze, startpos)
        self.func = m.mlx_loop_hook(self.initScreen, render, self)
        m.mlx_key_hook(self.screen, close_screen, self)
        for y in range(maze.y):
            for x in range(maze.x):
                update_cell_frame(self, x, y)
        m.mlx_loop(self.initScreen)


from mlx import Mlx
from math import floor
from Utils.classes import MazeGrid


mult = 100


def close_screen(key: int, self) -> None:
    if key == 65307:
        self.mlx.mlx_loop_exit(self.initScreen)


def show_grid(self) -> None:
    cell_size = int(floor(mult / 2))
    cell_dimention = int(cell_size * 1.5)
    maze = self.maze
    for y in range(maze.y):
        for x in range(maze.x):
            posX = x * mult
            posY = y * mult
            pixel(0xFF0000FF, posX, posY, self, mult)

    for y in range(maze.y):
        for x in range(maze.x):
            posX = int((x * mult) - cell_dimention / 2)
            posY = int((y * mult) - cell_dimention / 2)
            pixel(0xFF000099, posX + cell_size, posY + cell_size,
                  self, cell_dimention)


def update_cell(self, x, y) -> None:
    maze: MazeGrid = self.maze
    cell = maze.objects[y][x]

    posX = x * mult
    posY = y * mult

    cell_size = int(floor(mult / 2))
    cell_dimention = int(cell_size * 1.5)

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
        pixel(0xFF000099, posX + cell_size, pos,
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


def render(self) -> None:
    maze: MazeGrid = self.maze
    for y in range(maze.y):
        for x in range(maze.x):
            update_cell(self, x, y)
    from random import randint
    roll = randint(0, 3)
    if roll == 0:
        maze.objects[randint(0, maze.y)][randint(0, maze.x)].N = 0
    elif roll == 1:
        maze.objects[randint(0, maze.y)][randint(0, maze.x)].S = 0
    elif roll == 2:
        maze.objects[randint(0, maze.y)][randint(0, maze.x)].E = 0
    elif roll == 3:
        maze.objects[randint(0, maze.y)][randint(0, maze.x)].W = 0


class Screen:
    def __init__(self, maze: MazeGrid) -> None:
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
        m.mlx_key_hook(self.screen, close_screen, self)
        m.mlx_loop_hook(self.initScreen, render, self)
        show_grid(self)
        m.mlx_loop(self.initScreen)

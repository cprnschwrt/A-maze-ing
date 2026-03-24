from mlx import Mlx
from math import floor
from Utils.classes import MazeGrid, Vector2
import inspect
from random import randint
from Utils.characters import Characters
from menu import BUTTONS, selected_button, draw_menu, menu_manager

primaryCol = 0xFF0000FF
secondaryCol = 0xFF000099

max_size = 1250
mult = 100
steps = 0
paused = False
finished = False
sizemult = 1.4
offsety = 250
offsetx = 50


def pixel(nx: int, ny: int, self, size: int = mult, color: int = None) -> None:
    if color is None:
        color = primaryCol
    posx, posy = (size.x, size.y) if isinstance(size, Vector2) else (size, size)
    image = Mlx.mlx_new_image(self.mlx, self.initScreen, posx, posy)
    pixelbuff = Mlx.mlx_get_data_addr(self.mlx, image)
    for y in range(posy):
        for x in range(posx):
            pixel = (y * pixelbuff[2]) + (x * 4)
            pixelbuff[0][pixel] = color & 0xFF
            pixelbuff[0][pixel + 1] = (color >> 8) & 0xFF
            pixelbuff[0][pixel + 2] = (color >> 16) & 0xFF
            pixelbuff[0][pixel + 3] = (color >> 24)
    Mlx.mlx_put_image_to_window(self.mlx, self.initScreen, self.screen, image, nx + 50, ny + offsety)


def pixel_character(nx, ny, self, charList: list[str], sx, sy) -> None:
    charList = charList.value
    if not charList:
        return
    posx, posy = sx, sy
    image = Mlx.mlx_new_image(self.mlx, self.initScreen, posx, posy)
    pixelbuff = Mlx.mlx_get_data_addr(self.mlx, image)
    pixelbuff = list(pixelbuff)
    for y in range(posy):
        ymult = min(y // (posy // len(charList)) if len(charList) else 0, len(charList) - 1)
        for x in range(posx):
            xmult = min(x // (posx // len(charList[ymult])) if len(charList[ymult]) else 0, len(charList[ymult]) - 1)
            if charList[ymult][xmult] == "X":
                pixel = (y * pixelbuff[2]) + (x * 4)
                pixelbuff[0][pixel] = primaryCol & 0xFF
                pixelbuff[0][pixel + 1] = (primaryCol >> 8) & 0xFF
                pixelbuff[0][pixel + 2] = (primaryCol >> 16) & 0xFF
                pixelbuff[0][pixel + 3] = (primaryCol >> 24)
            else:
                pixel = (y * pixelbuff[2]) + (x * 4)
                pixelbuff[0][pixel] = secondaryCol & 0xFF
                pixelbuff[0][pixel + 1] = (secondaryCol >> 8) & 0xFF
                pixelbuff[0][pixel + 2] = (secondaryCol >> 16) & 0xFF
                pixelbuff[0][pixel + 3] = (secondaryCol >> 24)
    Mlx.mlx_put_image_to_window(self.mlx, self.initScreen, self.screen, image, nx, ny)



def show_grid(self) -> None:
    Decorate(self)
    cell_size = int(floor(mult / 2))
    cell_dimention = int(cell_size * sizemult)
    maze = self.maze
    pixel(0, 0, self, Vector2(y=(mult * maze.y), x=(mult * maze.x)))
    for y in range(maze.y):
        for x in range(maze.x):
            posX = int((x * mult) - cell_dimention / 2)
            posY = int((y * mult) - cell_dimention / 2)
            pixel(posX + cell_size, posY + cell_size, self, cell_dimention, color=secondaryCol)
    draw_menu(self)


def update_cell_frame(self, x, y) -> None:
    maze: MazeGrid = self.maze
    cell = maze.objects[y][x]
    posX, posY = x * mult, y * mult
    cell_size = int(floor(mult / 2))
    cell_dimention = int(cell_size * sizemult)
    if cell.N == 0:
        pixel(posX, posY - cell_size, self, cell_dimention, color=secondaryCol)
    if cell.S == 0:
        pixel(posX, posY + cell_size, self, cell_dimention, color=secondaryCol)
    if cell.E == 0:
        pixel(posX + cell_size, posY, self, cell_dimention, color=secondaryCol)
    if cell.W == 0:
        pixel(posX - cell_size, posY, self, cell_dimention, color=secondaryCol)


def render(self, force: bool = False) -> None:
    global finished, steps
    steps += 1
    if paused and not force:
        return
    if finished or not self.generation_started:
        return
    if self.step is not None and inspect.getgeneratorstate(self.step) != "GEN_CLOSED":
        self.step = next(self.step)
    elif self.step is None:
        print(f"Maze Finished in {steps} steps")
        finished = True


def Decorate(self) -> None:
    maze = self.maze
    size1x = maze.x * mult + (offsetx * 2) - offsetx
    pixel_character(0, offsety, self, Characters.up, offsetx, maze.y * mult)
    pixel_character(size1x, offsety, self, Characters.up, offsetx, maze.y * mult)
    pixel_character(offsetx, offsety - 50, self, Characters.side, maze.x * mult, offsetx)
    pixel_character(offsetx, maze.y * mult + offsety, self, Characters.side, maze.x * mult, offsetx)
    pixel_character(0, offsety - offsetx, self, Characters.corner1, offsetx, offsetx)
    pixel_character(0, maze.y * mult + offsety, self, Characters.corner2, offsetx, offsetx)
    pixel_character(size1x, offsety - offsetx, self, Characters.corner4, offsetx, offsetx)
    pixel_character(size1x, maze.y * mult + offsety, self, Characters.corner3, offsetx, offsetx)



class Screen:
    def __init__(self, maze: MazeGrid) -> None:
        from algo_backtrack_recursive import backtracking_recursive
        self.mlx = Mlx()
        self.initScreen = self.mlx.mlx_init()
        self.maze = maze
        global mult

        if maze.x * mult > max_size or maze.y * mult > max_size:
            val = maze.x * mult if maze.y * mult <= max_size else maze.y * mult
            mult = int(floor(mult * (((max_size / val))) + 1))

        self.screen = self.mlx.mlx_new_window(
            self.initScreen,
            maze.x * mult + (offsetx * 2),
            maze.y * mult + 400 + offsety,
            "cschwart | A-MAZE-ING | bgix")
        self.mouse_x = 0
        self.mouse_y = 0
        self.generation_started = False
        self.wall_color = 0xFF0000FF
        self.cell_color = 0xFF000099
        self.pattern = Characters.up

        self.mlx.mlx_key_hook(self.screen, menu_manager, self)
        self.mlx.mlx_mouse_hook(self.screen, self.mouse_hook, self)

        show_grid(self)

        startpos = None
        while True:
            randX, randY = randint(0, maze.x - 1), randint(0, maze.y - 1)
            if maze.objects[randY][randX].Status != 42:
                startpos = Vector2(x=randX, y=randY)
                break

        self.step = backtracking_recursive(self, maze, startpos)
        self.func = self.mlx.mlx_loop_hook(self.initScreen, render, self)
        self.mlx.mlx_loop(self.initScreen)

    def mouse_hook(self, x, y, button, state):
        self.mouse_x = x
        self.mouse_y = y

    def start_generation_seeker(self):
        self.generation_started = False
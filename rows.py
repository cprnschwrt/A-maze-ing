from mlx import Mlx
from math import floor
from Utils.classes import MazeGrid, Vector2
import inspect
from Utils.characters import Characters
from menu import draw_menu, menu_manager


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
selected_button = 0


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
            pixel(posX + cell_size, posY + cell_size, self, cell_dimention,
                  color=secondaryCol)
    draw_menu(self)


def update_cell_frame(self, x, y) -> None:
    maze: MazeGrid = self.maze
    cell = maze.objects[y][x]

    posX = x * mult
    posY = y * mult

    cell_size = int(floor(mult / 2))
    cell_dimention = int(cell_size * sizemult)

    if cell.N == 0:
        pos = (int(posX - cell_dimention / 2) + cell_size)
        pixel(pos, posY - cell_size, self, cell_dimention, color=secondaryCol)
    if cell.S == 0:
        pos = (int(posX - cell_dimention / 2) + cell_size)
        pixel(pos, posY + cell_size, self, cell_dimention, color=secondaryCol)
    if cell.E == 0:
        pos = (int(posY - cell_dimention / 2) + cell_size)
        pixel(posX + cell_size, pos, self, cell_dimention, color=secondaryCol)
    if cell.W == 0:
        pos = (int(posY - cell_dimention / 2) + cell_size)
        pixel(posX - cell_size, pos, self, cell_dimention, color=secondaryCol)


def pixel_character(nx, ny, self, charList: list[str], sx, sy) -> None:
    charList = charList.value

    posx, posy = sx, sy

    image = Mlx.mlx_new_image(self.mlx, self.initScreen, posx, posy)
    pixelbuff = Mlx.mlx_get_data_addr(self.mlx, image)
    pixelbuff = list(pixelbuff)

    if not charList:
        return

    for y in range(posy):
        ymult = min(y // (posy // len(charList)) if len(charList) > 0 else 0,
                    len(charList) - 1)

        for x in range(posx):
            xmult = min(x // (posx // len(charList[ymult])) if len(
                charList[ymult]) > 0 else 0, len(charList[ymult]) - 1)

            if charList[ymult][xmult] == "X":
                pixel = (y * pixelbuff[2]) + (x * 4)
                pixelbuff[0][pixel] = (primaryCol) & 0xFF
                pixelbuff[0][pixel + 1] = (primaryCol >> 8) & 0xFF
                pixelbuff[0][pixel + 2] = (primaryCol >> 16) & 0xFF
                pixelbuff[0][pixel + 3] = (primaryCol >> 24)
            else:
                pixel = (y * pixelbuff[2]) + (x * 4)
                pixelbuff[0][pixel] = (secondaryCol) & 0xFF
                pixelbuff[0][pixel + 1] = (secondaryCol >> 8) & 0xFF
                pixelbuff[0][pixel + 2] = (secondaryCol >> 16) & 0xFF
                pixelbuff[0][pixel + 3] = (secondaryCol >> 24)

    Mlx.mlx_put_image_to_window(self.mlx, self.initScreen, self.screen, image,
                                nx, ny)


def pixel(nx: int, ny: int, self, size: int = mult, color: int = None) -> None:
    if color is None:
        color = primaryCol
    posx, posy = 0, 0
    if type(size) is Vector2:
        posx, posy = size.x, size.y
    else:
        posx, posy = size, size

    image = Mlx.mlx_new_image(self.mlx, self.initScreen, posx, posy)
    pixelbuff = Mlx.mlx_get_data_addr(self.mlx, image)

    for y in range(posy):
        for x in range(posx):
            pixel = (y * pixelbuff[2]) + (x * 4)
            pixelbuff[0][pixel] = (color) & 0xFF
            pixelbuff[0][pixel + 1] = (color >> 8) & 0xFF
            pixelbuff[0][pixel + 2] = (color >> 16) & 0xFF
            pixelbuff[0][pixel + 3] = (color >> 24)

    Mlx.mlx_put_image_to_window(self.mlx, self.initScreen, self.screen,
                                image, nx + 50, ny + offsety)


def render(self, force: bool = False) -> None:
    global finished, steps
    steps += 1
    if paused and not force:
        return
    if finished or not self.generation_started:
        return
    if self.step is not None and (
            inspect.getgeneratorstate(self.step) != "GEN_CLOSED"):
        self.step = next(self.step)
    elif self.step is None:
        print(f"Maze Finished in {steps} steps")
        finished = True


def Decorate(self) -> None:
    maze = self.maze
    size1x = maze.x * mult + (offsetx * 2) - offsetx
    pixel_character(0, offsety, self, Characters.up, offsetx,
                    maze.y * mult)
    pixel_character(size1x, offsety, self, Characters.up, offsetx,
                    maze.y * mult)
    pixel_character(offsetx, offsety - 50, self, Characters.side,
                    maze.x * mult, offsetx)
    pixel_character(offsetx, offsety - 50, self, Characters.side,
                    maze.x * mult, offsetx)
    pixel_character(offsetx, maze.y * mult + offsety, self, Characters.side,
                    maze.x * mult, offsetx)
    pixel_character(0, offsety - offsetx, self, Characters.corner1, offsetx,
                    offsetx)
    pixel_character(0, maze.y * mult + offsety, self, Characters.corner2,
                    offsetx, offsetx)
    pixel_character(size1x, offsety - offsetx, self, Characters.corner4,
                    offsetx, offsetx)
    pixel_character(size1x, maze.y * mult + offsety, self, Characters.corner3,
                    offsetx, offsetx)


class Screen:
    def __init__(self, maze: MazeGrid) -> None:
        self.mlx = Mlx()
        self.initScreen = self.mlx.mlx_init()
        self.maze = maze
        global mult

        if maze.x * mult > max_size or maze.y * mult > max_size:
            val = maze.x * mult if maze.y * mult <= max_size else maze.y * mult
            mult = int(floor(mult * (((max_size / val))) + 1))

        self.screen = self.mlx.mlx_new_window(
            self.initScreen, maze.x * mult + (offsetx * 2),
            maze.y * mult + 400 + offsety, "cschwart | A-MAZE-ING | bgix")
        self.wall_color = 0xFF0000FF
        self.cell_color = 0xFF000099
        self.mlx.mlx_key_hook(self.screen, menu_manager, self)
        show_grid(self)
        for y in range(maze.y):
            for x in range(maze.x):
                update_cell_frame(self, x, y)

        self.mlx.mlx_loop(self.initScreen)

    def start_generation_rows(self):
        self.maze.generate_maze()

        print("Maze Generated")

        print("Maze Grid Redrawn")

        Decorate(self)
        print("Decoration Completed")

        for y in range(self.maze.y):
            for x in range(self.maze.x):
                update_cell_frame(self, x, y)
        print("Cell Frames Updated")

        print("Buttons Redrawn")

    def solve_maze(self):
        pass

    # def change_colours(self):
    #     self.wall_color = 0x00FF00
    #     self.cell_color = 0x0000FF
    #     show_grid(self)

    def change_colours(self):
        pass

    def change_pattern(self):
        pass
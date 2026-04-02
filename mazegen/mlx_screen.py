from math import floor
from .mazeclass import MazeGrid, Vector2
from .utility_func import to_colhex, magnitude
from .mlxcharacters import MlxCharacters
import inspect
from typing import Any
from mlx import Mlx  # type: ignore


class Screen:
    def __init__(self, maze: MazeGrid, settings: dict[str, Any]) -> None:
        self.mlx = Mlx()
        self.initScreen = self.mlx.mlx_init()
        self.maze = maze
        self.total_count: int = int(maze.x * maze.y)
        self.count = -1
        self.settings = settings
        self.mult = 100
        self.max_size_y = 1250
        self.max_size_x = 1250
        self.pixelbuff: Any | list[Any] = None
        self.solved = False
        self.maze_image = None
        self.offsety = 250
        self.load: int = 0
        self.primaryCol: int = 0
        self.secondaryCol: int = 0
        self.tertiaryCol: int = 0
        self.colorIndex = 0
        self.paused = False
        self.finished = False
        self.border_size = 10 * 2
        self.offsetx = 50
        self.maze_hex: list[str] = []
        self.change_color()

        try:
            self.output = settings["maze.txt"]
        except KeyError:
            self.output = "maze.txt"

        self.entry = maze.entry
        self.exit = maze.exit
        self.x = maze.x
        self.y = maze.y

        try:
            self.exit = settings["exit"]
        except KeyError:
            self.exit = Vector2(x=maze.x - 1, y=maze.y - 1)

        try:
            self.lights_on = settings["lights"]
        except KeyError:
            self.lights_on = False

        try:
            self.perfect = settings["perfect"]
        except KeyError:
            self.perfect = True

        if maze.x * self.mult > self.max_size_x or\
                maze.y * self.mult > self.max_size_y:
            val = maze.x * self.mult if maze.y * self.mult <= self.max_size_y \
                    else maze.y * self.mult
            self.mult = int(floor(self.mult * (((self.max_size_y / val))) + 1))

        self.screen = (
            self.mlx.mlx_new_window(
                self.initScreen,
                maze.x * self.mult + (self.offsetx * 2),
                maze.y * self.mult + 400 + self.offsety,
                "cschwart | A-MAZE-ING | bgix    "))
        for y in range(self.maze.y):
            self.maze_hex.append("")
            for x in range(self.maze.x):
                self.maze_hex[y] += "0"
        self.x = int(maze.x * self.mult)
        self.y = int(maze.y * self.mult)
        self.generation_started = True

        self.lights = [Vector2(x=int(self.x/2), y=int(self.y/2)),
                       Vector2(x=0, y=0), Vector2(x=self.x, y=0),
                       Vector2(x=self.x, y=self.y), Vector2(x=0, y=self.y)]

        m: Mlx = self.mlx
        self.func = m.mlx_loop_hook(self.initScreen, self.render, self)
        m.mlx_key_hook(self.screen, self.keybind_manager, self)
        self.Decorate()
        self.refresh(redo=True)
        m.mlx_loop(self.initScreen)

    @staticmethod
    def pixel_character(nx: int, ny: int, self: Any,
                        charList: MlxCharacters, sx: int, sy: int) -> None:
        posx, posy = sx, sy
        image = Mlx.mlx_new_image(self.mlx, self.initScreen,
                                  posx, posy)
        pixelbuff = Mlx.mlx_get_data_addr(self.mlx, image)
        pixelbuff = list(pixelbuff)
        if charList.value is not None:
            tabs = list(charList.value)
            ymult = 0
            for y in range(posy):
                xmult = 0
                if y >= (posy / len(tabs)) * ymult:
                    ymult += 1
                for x in range(posx):
                    if x >= (posx / len(tabs[ymult - 1])) * xmult:
                        xmult += 1
                    if tabs[ymult - 1][xmult - 1] == "X":
                        pixel = (y * pixelbuff[2]) + (x * 4)
                        pixelbuff[0][pixel] = (self.primaryCol) & 0xFF
                        pixelbuff[0][pixel + 1] = ((self.primaryCol >> 8)
                                                   & 0xFF)
                        pixelbuff[0][pixel + 2] = ((self.primaryCol >> 16)
                                                   & 0xFF)
                        pixelbuff[0][pixel + 3] = (self.primaryCol >> 24)
                    else:
                        pixel = (y * pixelbuff[2]) + (x * 4)
                        pixelbuff[0][pixel] = (self.secondaryCol) & 0xFF
                        pixelbuff[0][pixel + 1] = ((self.secondaryCol >> 8)
                                                   & 0xFF)
                        pixelbuff[0][pixel + 2] = ((self.secondaryCol >> 16)
                                                   & 0xFF)
                        pixelbuff[0][pixel + 3] = (self.secondaryCol >> 24)
        else:
            col = self.tertiaryCol
            for y in range(posy):
                for x in range(posx):
                    pixel = (y * pixelbuff[2]) + (x * 4)
                    pixelbuff[0][pixel] = (col) & 0xFF
                    pixelbuff[0][pixel + 1] = (col >> 8) & 0xFF
                    pixelbuff[0][pixel + 2] = (col >> 16) & 0xFF
                    pixelbuff[0][pixel + 3] = (col >> 24)
        Mlx.mlx_put_image_to_window(self.mlx, self.initScreen, self.screen,
                                    image, nx, ny)

    def render(self: Any, force: bool = False, Kill: bool = False) -> None:
        maze: MazeGrid = self.maze
        if self.paused is True and force is not True and Kill is False:
            return
        if self.finished is True or self.generation_started is False \
                and Kill is False:
            return
        if Kill is True or (maze.step is not None
                            and inspect.getgeneratorstate(maze.step) !=
                            "GEN_CLOSED"):
            status = inspect.getgeneratorstate(maze.step)
            if status != "GEN_CLOSED" and maze.step is not None:
                maze.generate_step()
                self.refresh(self)
                self.update_loading()
        elif maze.step is None:
            self.finished = True
            maze.save()

    def draw_wallpaper(self, col: int = 0xFFFFFFFF,
                       px: int | float = 0, py: int | float = 0) -> None:
        maze = self.maze
        divider = None
        mult = 100
        while divider is None or divider != floor(divider):
            divider = mult / 2
            mult -= 1
        divider = int(divider)
        size_x = (maze.x * self.mult + self.offsetx * 2) / divider
        size_y = (maze.y * self.mult + 400 + self.offsety) / divider
        line_size = 4
        for x in range(divider):
            for y in range(divider):
                addx = int(x * size_x) + px
                addy = int(y * size_y) + py
                self.draw_line(addx + size_x / 2, addy, addx,
                               addy + size_y/2, line_size, col)
                self.draw_line(addx + size_x / 2, addy, addx + size_x,
                               addy + size_y/2, line_size, col)
                self.draw_line(addx + size_x / 2, addy + size_y, addx,
                               addy + size_y/2, line_size, col)
                self.draw_line(addx + size_x / 2, addy + size_y, addx + size_x,
                               addy + size_y/2, line_size, col)

    def Decorate(self) -> None:
        maze = self.maze
        size1x = maze.x * self.mult + (self.offsetx * 2) - self.offsetx
        posend = maze.y * self.mult + self.offsety + 400 - self.offsetx

        self.draw_wallpaper(self.tertiaryCol, 11, 0)
        self.draw_wallpaper(self.secondaryCol)
        self.pixel_character(0, 0, self, MlxCharacters.up, self.offsetx,
                             maze.y * self.mult + self.offsety + 400)
        self.pixel_character(size1x,
                             0, self, MlxCharacters.up, self.offsetx,
                             maze.y * self.mult + self.offsety + 400)
        self.pixel_character(self.offsetx,
                             self.offsety - 50, self, MlxCharacters.side,
                             self.x,
                             self.offsetx)
        self.pixel_character(self.offsetx,
                             self.offsety - 50, self, MlxCharacters.side,
                             self.x,
                             self.offsetx)
        self.pixel_character(self.offsetx,
                             self.y + self.offsety, self,
                             MlxCharacters.side,
                             self.x, self.offsetx)
        self.pixel_character(self.offsetx,
                             maze.y * self.mult + self.offsety + 100, self,
                             MlxCharacters.side,
                             self.x, self.offsetx)

        self.pixel_character(0,
                             self.offsety - self.offsetx, self,
                             MlxCharacters.tcorner1,
                             self.offsetx, self.offsetx)
        self.pixel_character(0,
                             self.y + self.offsety, self,
                             MlxCharacters.tcorner1,
                             self.offsetx, self.offsetx)

        self.pixel_character(size1x,
                             self.offsety - self.offsetx, self,
                             MlxCharacters.tcorner3,
                             self.offsetx, self.offsetx)
        self.pixel_character(size1x,
                             self.y + self.offsety, self,
                             MlxCharacters.tcorner3,
                             self.offsetx, self.offsetx)
        self.pixel_character(0,
                             self.y + self.offsety + 100, self,
                             MlxCharacters.tcorner1,
                             self.offsetx, self.offsetx)
        self.pixel_character(size1x,
                             self.y + self.offsety + 100, self,
                             MlxCharacters.tcorner3,
                             self.offsetx, self.offsetx)
        self.pixel_character(self.offsetx,
                             self.y + self.offsety + 50, self,
                             MlxCharacters.none,
                             self.x, self.offsetx)

        self.pixel_character(0, posend, self, MlxCharacters.side,
                             self.x + self.offsetx, self.offsetx)
        self.pixel_character(0, posend, self, MlxCharacters.corner2,
                             self.offsetx, self.offsetx)
        self.pixel_character(size1x, posend, self, MlxCharacters.corner3,
                             self.offsetx, self.offsetx)

        self.pixel_character(0, 0, self, MlxCharacters.side,
                             self.x + self.offsetx, self.offsetx)
        self.pixel_character(0, 0, self, MlxCharacters.corner1,
                             self.offsetx, self.offsetx)
        self.pixel_character(size1x, 0, self, MlxCharacters.corner4,
                             self.offsetx, self.offsetx)

    def solve_maze(self) -> None:
        col3 = self.tertiaryCol if self.solved is False else self.secondaryCol
        maze: MazeGrid = self.maze
        cell_size = self.mult
        cell_dimention = cell_size - self.border_size
        if self.finished is not True:
            print("The maze is still generating...")
            return
        if self.solved is not True:
            print("Solving Maze...")
        else:
            print("Hiding Maze...")
        for y in range(maze.y):
            for x in range(maze.x):
                cell = maze.objects[y][x]
                ty = int(((cell_size) * y) + self.border_size / 2)
                tx = int(((cell_size) * x) + self.border_size / 2)
                if cell.Status == "path" and self.finished is True:
                    if cell.S == 0 and maze.objects[y + 1][x].Status == "path":
                        self.fill_image(self.pixelbuff,
                                        tx + self.border_size / 2,
                                        int(ty + (cell_size / 2) -
                                            cell_dimention / 2),
                                        cell_dimention - self.border_size,
                                        cell_dimention * 2,
                                        col3)
                    if cell.N == 0 and maze.objects[y - 1][x].Status == "path":
                        self.fill_image(self.pixelbuff,
                                        tx + self.border_size / 2,
                                        int(ty - (cell_size / 2) -
                                            cell_dimention / 2),
                                        cell_dimention - self.border_size,
                                        cell_dimention * 2,
                                        col3)
                    if cell.E == 0 and maze.objects[y][x + 1].Status == "path":
                        self.fill_image(self.pixelbuff,
                                        int(tx + (cell_size / 2) -
                                            cell_dimention / 2),
                                        ty + self.border_size / 2,
                                        cell_dimention * 2,
                                        cell_dimention - self.border_size,
                                        col3)
                    if cell.W == 0 and maze.objects[y][x - 1].Status == "path":
                        self.fill_image(self.pixelbuff,
                                        int(tx - (cell_size / 2) -
                                            cell_dimention / 2),
                                        ty + self.border_size / 2,
                                        cell_dimention * 2,
                                        cell_dimention - self.border_size,
                                        col3)
        if self.solved is True:
            self.solved = False
        else:
            self.solved = True
        Mlx.mlx_put_image_to_window(self.mlx, self.initScreen, self.screen,
                                    self.maze_image, self.offsetx,
                                    self.offsety)

    def restart(self) -> None:
        self.func = self.mlx.mlx_loop_hook(self.initScreen, self.render, self)
        print("Re-generating...")
        for y in range(self.maze.y):
            self.maze_hex.append("")
            for x in range(self.maze.x):
                self.maze_hex[y] += "0"
        self.pixel_character(self.offsetx,
                             self.y + self.offsety + 50, self,
                             MlxCharacters.none,
                             self.x, self.offsetx)
        self.maze.verif()
        self.count = -1
        self.load = -1
        self.solved = False
        self.refresh(redo=True)
        self.finished = False
        self.paused = False

    def update_loading(self, reset: bool = False) -> None:
        maze = self.maze
        cells = maze.objects
        count = 0
        for y in range(maze.y):
            for x in range(maze.x):
                cell = cells[y][x]
                if cell.checked is True or cell.Status == 42:
                    count += 1
        if reset is True:
            size = (self.x / self.total_count) * (self.count + 1)
            xpos: int | float = self.offsetx
            ypos = maze.y * self.mult + self.offsety + 50
            self.pixel_character(int(xpos), int(ypos), self,
                                 MlxCharacters.full,
                                 int(size), self.offsetx)
            return
        if self.count == count:
            return
        while self.count <= count:
            size = self.x / self.total_count
            xpos = ((self.offsetx + (size * self.count)) +
                    (size / 2 if self.count != self.total_count
                     else -(size / 2)))
            if xpos != int(xpos):
                xpos += 1
                size += 1
            ypos = maze.y * self.mult + self.offsety + 50
            self.pixel_character(int(xpos), int(ypos), self,
                                 MlxCharacters.full,
                                 int(size), self.offsetx)
            self.count += 1

    def draw_line(self, x1: int | float, y1: int | float, x2: int | float,
                  y2: int | float, size: int = 5,
                  col: int = 0xFFFFFFFF) -> None:
        x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
        if (abs(x2 - x1) >= abs(y2 - y1)):
            self.draw_line_w(x1, y1, x2, y2, size, col)
        else:
            self.draw_line_h(x1, y1, x2, y2, size, col)

    def draw_line_w(self, x1: int, y1: int, x2: int,
                    y2: int, size: int, col: int) -> None:
        if (x1 > x2):
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dx = x2 - x1
        dy = y2 - y1
        y = y1
        direction = -1 if dy < 0 else 1
        dy *= direction
        des = 2*dy - dx
        if dx == 0:
            return
        for x in range(x1, x2 + 1):
            for py in range(size):
                self.mlx.mlx_pixel_put(self.initScreen, self.screen, x,
                                       int(y - (size/2) + py), col)
            if des >= 0:
                y += direction
                des -= 2*dx
            des += 2*dy

    def draw_line_h(self, x1: int, y1: int, x2: int,
                    y2: int, size: int, col: int) -> None:
        if (y1 > y2):
            y1, y2 = y2, y1
            x1, x2 = x2, x1

        dx = x2 - x1
        dy = y2 - y1
        x = x1
        direction = -1 if dx < 0 else 1
        dx *= direction
        des = 2*dx - dy

        if dy == 0:
            return
        for y in range(y1, y2 + 1):
            for px in range(size):
                self.mlx.mlx_pixel_put(self.initScreen, self.screen,
                                       int(x - (size/2) + px), y, col)
            if des >= 0:
                x += direction
                des -= 2*dy
            des += 2*dx

    def refresh(self, redo: int = False) -> None:
        col1 = self.primaryCol
        col2 = self.secondaryCol
        col3 = self.tertiaryCol
        maze: MazeGrid = self.maze
        posx, posy = self.x, self.y
        if self.maze_image is None:
            self.maze_image = Mlx.mlx_new_image(self.mlx, self.initScreen,
                                                posx, posy)
            self.pixelbuff = list(Mlx.mlx_get_data_addr(self.mlx,
                                                        self.maze_image))

        cell_size = self.mult
        cell_dimention = cell_size - self.border_size

        if redo is True:
            self.fill_image(self.pixelbuff, 0, 0,
                            self.x, self.y, col1)
            for y in range(maze.y):
                for x in range(maze.x):
                    ty = int(((cell_size) * y) + self.border_size / 2)
                    tx = int(((cell_size) * x) + self.border_size / 2)
                    self.fill_image(self.pixelbuff, tx, ty,
                                    cell_dimention, cell_dimention, col2)

        hexa_cell = self.maze.hexa_grid()
        for y in range(maze.y):
            for x in range(maze.x):
                cell = maze.objects[y][x]
                ty = int(((cell_size) * y) + self.border_size / 2)
                tx = int(((cell_size) * x) + self.border_size / 2)
                if hexa_cell[y][x] != self.maze_hex[y][x] or redo is True:
                    if cell.S == 0:
                        self.fill_image(self.pixelbuff, tx,
                                        (ty + (cell_size / 2) -
                                         cell_dimention / 2),
                                        cell_dimention, cell_dimention * 2,
                                        col2)
                    if cell.N == 0:
                        self.fill_image(self.pixelbuff, tx,
                                        (ty - (cell_size / 2) -
                                         cell_dimention / 2),
                                        cell_dimention, cell_dimention * 2,
                                        col2)
                    if cell.E == 0:
                        self.fill_image(self.pixelbuff,
                                        (tx + (cell_size / 2) -
                                         cell_dimention / 2),
                                        ty, cell_dimention * 2, cell_dimention,
                                        col2)
                    if cell.W == 0:
                        self.fill_image(self.pixelbuff,
                                        (tx - (cell_size / 2) -
                                         cell_dimention / 2),
                                        ty, cell_dimention * 2, cell_dimention,
                                        col2)
        for y in range(maze.y):
            for x in range(maze.x):
                cell = maze.objects[y][x]
                ty = int(((cell_size) * y) + self.border_size / 2)
                tx = int(((cell_size) * x) + self.border_size / 2)
                if hexa_cell[y][x] != self.maze_hex[y][x] or redo is True:
                    if cell.N == 0 and maze.objects[y - 1][x].Status == 42:
                        self.fill_image(self.pixelbuff,
                                        tx + self.border_size / 2,
                                        int(ty - (cell_size / 2) -
                                            cell_dimention / 2),
                                        cell_dimention - self.border_size,
                                        cell_dimention * 2,
                                        col3)
                    if cell.S == 0 and maze.objects[y + 1][x].Status == 42:
                        self.fill_image(self.pixelbuff,
                                        tx + self.border_size / 2,
                                        int(ty + (cell_size / 2) -
                                            cell_dimention / 2),
                                        cell_dimention - self.border_size,
                                        cell_dimention * 2,
                                        col3)
                    if cell.E == 0 and maze.objects[y][x + 1].Status == 42:
                        self.fill_image(self.pixelbuff,
                                        int(tx + (cell_size / 2) -
                                            cell_dimention / 2),
                                        ty + self.border_size / 2,
                                        cell_dimention * 2,
                                        cell_dimention - self.border_size,
                                        col3)
                    if cell.W == 0 and maze.objects[y][x - 1].Status == 42:
                        self.fill_image(self.pixelbuff,
                                        int(tx - (cell_size / 2) -
                                            cell_dimention / 2),
                                        ty + self.border_size / 2,
                                        cell_dimention * 2,
                                        cell_dimention - self.border_size,
                                        col3)

        for y in range(maze.y):
            if self.solved is not True:
                break
            for x in range(maze.x):
                cell = maze.objects[y][x]
                ty = int(((cell_size) * y) + self.border_size / 2)
                tx = int(((cell_size) * x) + self.border_size / 2)
                if cell.Status == "path" and self.finished is True:
                    if cell.N == 0 and maze.objects[y - 1][x].Status == "path":
                        self.fill_image(self.pixelbuff,
                                        tx + self.border_size / 2,
                                        int(ty - (cell_size / 2) -
                                            cell_dimention / 2),
                                        cell_dimention - self.border_size,
                                        cell_dimention * 2,
                                        col3)
                    if cell.E == 0 and maze.objects[y][x + 1].Status == "path":
                        self.fill_image(self.pixelbuff,
                                        int(tx + (cell_size / 2) -
                                            cell_dimention / 2),
                                        ty + self.border_size / 2,
                                        cell_dimention * 2,
                                        cell_dimention - self.border_size,
                                        col3)
                    if cell.W == 0 and maze.objects[y][x - 1].Status == "path":
                        self.fill_image(self.pixelbuff,
                                        int(tx - (cell_size / 2) -
                                            cell_dimention / 2),
                                        ty + self.border_size / 2,
                                        cell_dimention * 2,
                                        cell_dimention - self.border_size,
                                        col3)
        self.maze_hex = hexa_cell
        Mlx.mlx_put_image_to_window(self.mlx, self.initScreen, self.screen,
                                    self.maze_image, self.offsetx,
                                    self.offsety)

    def fill_image(self, pixelbuff: list[Any], px: Any,
                   py: Any, sx: Any, sy: Any, col: int) -> None:
        r, g, b = (col >> 16) & 0xFF, (col >> 8) & 0xFF, (col >> 00) & 0xFF
        lightrange = 400
        px = int(px)
        py = int(py)
        sx = int(sx)
        sy = int(sy)
        for y in range(sy):
            for x in range(sx):
                pixel_color = 0xFF000000 if self.lights_on is True else col
                for point in range(len(self.lights)):
                    if self.lights_on is False:
                        break
                    light = self.lights[point]
                    lx = light.x
                    ly = light.y
                    magn = magnitude((x + px),
                                     (y + py), lx, ly)
                    if magn > lightrange:
                        continue
                    multiplyer = 1 - magn / lightrange
                    pixel_color += to_colhex(r * multiplyer,
                                             g * multiplyer,
                                             b * multiplyer) - 0xFFFFFFFF
                pixel = ((y + py) * pixelbuff[2]) + ((x + px) * 4)
                pixelbuff[0][pixel] = (pixel_color) & 0xFF
                pixelbuff[0][pixel + 1] = (pixel_color >> 8) & 0xFF
                pixelbuff[0][pixel + 2] = (pixel_color >> 16) & 0xFF
                pixelbuff[0][pixel + 3] = (pixel_color >> 24) & 0xFF

    @staticmethod
    def keybind_manager(key: int, self: Any) -> Any:
        if key == 65307:
            self.mlx.mlx_loop_exit(self.initScreen)
        elif key == 112:
            if self.paused is False:
                self.paused = True
                print("self.paused")
            else:
                self.paused = False
                print("Unself.paused")
        elif key == 65363:
            self.render(self, True)
        elif key == 114:
            self.paused = True
            self.restart()
        elif key == 99:
            self.change_color()
            self.Decorate()
            self.refresh(True)
            self.update_loading(True)
        elif key == 115:
            self.solve_maze()

    def change_color(self) -> None:
        colorPalets = {
            "Ducky Duck": [0xFFFFFF00, 0xFF999900, 0xFF777700],
            "Bubble Blue": [0xFF0000FF, 0xFF000099, 0xFF000077],
            "Red Hot": [0xFFFF0000, 0xFF990000, 0xFF770000],
            "Foliage Green": [0xFF00FF00, 0xFF009900, 0xFF007700],
            "Bakus Mogus": [0xFF009999, 0xFF00FFFF, 0xFF007777],
            "Vintage Static": [0xFF000000, 0xFFFFFFFF, 0xFF000000],
            "Rainbow eyesore": [0xFFFF0000, 0xFF00FF00, 0xFF0000FF],
        }
        listing = list(colorPalets.values())
        try:
            self.primaryCol = listing[self.colorIndex + 1][0]
            self.secondaryCol = listing[self.colorIndex + 1][1]
            self.tertiaryCol = listing[self.colorIndex + 1][2]
            self.colorIndex += 1
        except IndexError:
            self.primaryCol = listing[0][0]
            self.secondaryCol = listing[0][1]
            self.tertiaryCol = listing[0][2]
            self.colorIndex = 0

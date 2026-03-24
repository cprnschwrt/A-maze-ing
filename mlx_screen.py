from mlx import Mlx
from math import floor
from Utils.classes import MazeGrid, Vector2
import inspect
from random import randint, seed
from Utils.characters import Characters
from Utils.func import to_colhex, magnitude
import Utils.hexa as hexa
from algo_get_path import get_shortest_path


def is_mouse_on_button(self, mouse_x, mouse_y, button_x,
                       button_y, button_width, button_height):
    if button_x <= mouse_x <= button_x + button_width and \
            button_y <= mouse_y <= button_y + button_height:
        return True
    return False


def draw_button(self, label: str, x: int, y: int,
                width: int, height: int, button_id: int):
    label_text = str(label)
    self.mlx.mlx_string_put(self.initScreen, self.screen,
                            x + 10, y + 10, 0xFFFFFF, label_text)

    button_color = 0x00FF00
    if is_mouse_on_button(self, self.mouse_x, self.mouse_y,
                          x, y, width, height):
        button_color = 0x0000FF

    for i in range(width):
        for j in range(height):
            self.mlx.mlx_pixel_put(self.initScreen, self.screen,
                                   x + i, y + j, button_color)

    if is_mouse_on_button(self, self.mouse_x, self.mouse_y,
                          x, y, width, height):
        self.hover_button(button_id)


def pixel_character(nx, ny, self, charList: list[str], sx, sy) -> None:
    charList = charList.value
    posx, posy = sx, sy
    image = Mlx.mlx_new_image(self.mlx, self.initScreen,
                              posx, posy)
    pixelbuff = Mlx.mlx_get_data_addr(self.mlx, image)
    pixelbuff = list(pixelbuff)
    ymult = 0
    for y in range(posy):
        xmult = 0
        if y >= (posy / len(charList)) * ymult:
            ymult += 1
        for x in range(posx):
            if x >= (posx / len(charList[ymult - 1])) * xmult:
                xmult += 1
            if charList[ymult - 1][xmult - 1] == "X":
                pixel = (y * pixelbuff[2]) + (x * 4)
                pixelbuff[0][pixel] = (self.primaryCol) & 0xFF
                pixelbuff[0][pixel + 1] = (self.primaryCol >> 8) & 0xFF
                pixelbuff[0][pixel + 2] = (self.primaryCol >> 16) & 0xFF
                pixelbuff[0][pixel + 3] = (self.primaryCol >> 24)
            else:
                pixel = (y * pixelbuff[2]) + (x * 4)
                pixelbuff[0][pixel] = (self.secondaryCol) & 0xFF
                pixelbuff[0][pixel + 1] = (self.secondaryCol >> 8) & 0xFF
                pixelbuff[0][pixel + 2] = (self.secondaryCol >> 16) & 0xFF
                pixelbuff[0][pixel + 3] = (self.secondaryCol >> 24)

    Mlx.mlx_put_image_to_window(self.mlx, self.initScreen, self.screen,
                                image, nx, ny)


def render(self, force: bool = False, Kill: bool = False) -> None:
    self.steps += 1
    if self.paused is True and force is not True and Kill is False:
        return
    if self.finished is True or self.generation_started is False \
            and Kill is False:
        return
    if Kill is True or (self.step is not None
       and inspect.getgeneratorstate(self.step) != "GEN_CLOSED"):
        status = inspect.getgeneratorstate(self.step)
        if Kill is True and status == "GEN_CLOSED":
            self.step.close()
            self.step = None
        elif status != "GEN_CLOSED" and self.step is not None:
            self.step = next(self.step)
            self.refresh(self)

    elif self.step is None:
        print(f"Maze finished in {self.steps} steps, Calculating Path...")
        self.finished = True
        vals = get_shortest_path(self.maze, self.entry, self.exit)
        cells = vals[0]
        path = vals[1]
        for pos in cells:
            self.maze.objects[pos[1]][pos[0]].Status = "path"
        print("Done !")
        hex = hexa.hexa_grid(self.maze)
        with open(self.output, "w") as file:
            for line in hex:
                file.write(line + "\n")
            file.write("\n")
            file.write(f"{self.entry[0]}, {self.entry[1]}\n")
            file.write(f"{self.exit[0]}, {self.exit[1]}\n")
            file.write(f"{path}\n")


def Decorate(self) -> None:
    maze = self.maze
    size1x = maze.x * self.mult + (self.offsetx * 2) - self.offsetx
    posend = maze.y * self.mult + self.offsety + 400 - self.offsetx

    pixel_character(0, 0, self, Characters.up, self.offsetx,
                    maze.y * self.mult + self.offsety + 400)
    pixel_character(size1x,
                    0, self, Characters.up, self.offsetx,
                    maze.y * self.mult + self.offsety + 400)
    pixel_character(self.offsetx,
                    self.offsety - 50, self, Characters.side,
                    maze.x * self.mult,
                    self.offsetx)
    pixel_character(self.offsetx,
                    self.offsety - 50, self, Characters.side,
                    maze.x * self.mult,
                    self.offsetx)
    pixel_character(self.offsetx,
                    maze.y * self.mult + self.offsety, self, Characters.side,
                    maze.x * self.mult, self.offsetx)

    pixel_character(0,
                    self.offsety - self.offsetx, self, Characters.tcorner1,
                    self.offsetx, self.offsetx)
    pixel_character(0,
                    maze.y * self.mult + self.offsety, self,
                    Characters.tcorner1,
                    self.offsetx, self.offsetx)

    pixel_character(size1x,
                    self.offsety - self.offsetx, self, Characters.tcorner3,
                    self.offsetx, self.offsetx)
    pixel_character(size1x,
                    maze.y * self.mult + self.offsety, self,
                    Characters.tcorner3,
                    self.offsetx, self.offsetx)

    pixel_character(0, posend, self, Characters.side,
                    maze.x * self.mult + self.offsetx, self.offsetx)
    pixel_character(0, posend, self, Characters.corner2,
                    self.offsetx, self.offsetx)
    pixel_character(size1x, posend, self, Characters.corner3,
                    self.offsetx, self.offsetx)

    pixel_character(0, 0, self, Characters.side,
                    maze.x * self.mult + self.offsetx, self.offsetx)
    pixel_character(0, 0, self, Characters.corner1,
                    self.offsetx, self.offsetx)
    pixel_character(size1x, 0, self, Characters.corner4,
                    self.offsetx, self.offsetx)


class Screen:
    def __init__(self, maze: MazeGrid, settings: dict) -> None:
        from algo_backtrack_recursive import backtracking_recursive
        self.mlx = Mlx()
        self.initScreen = self.mlx.mlx_init()
        self.maze = maze
        self.settings = settings
        self.mult = 100
        self.max_size = 1250
        self.pixelbuff = None
        self.solved = False
        self.maze_image = None
        self.offsety = 250
        self.primaryCol = None
        self.secondaryCol = None
        self.tertiaryCol = None
        self.colorIndex = 0
        self.steps = 0
        self.paused = False
        self.finished = False
        self.border_size = 10 * 2
        self.offsetx = 50
        self.maze_hex = []
        self.change_color()
        try:
            seed(settings["seed"])
            self.seed = settings["seed"]
        except KeyError:
            self.seed = randint(0, randint(0, 100000000))
            seed(self.seed)
        try:
            self.output = settings["maze.txt"]
        except KeyError:
            self.output = "maze.txt"

        try:
            self.entry = settings["entry"]
        except KeyError:
            self.entry = [0, 0]

        try:
            self.exit = settings["exit"]
        except KeyError:
            self.exit = [maze.x - 1, maze.y - 1]

        try:
            self.lights_on = settings["lights"]
        except KeyError:
            self.lights_on = False

        try:
            self.perfect = settings["perfect"]
        except KeyError:
            self.perfect = True

        try:
            self.skip = settings["skip"]
        except KeyError:
            self.skip = False

        if maze.x * self.mult > self.max_size or\
                maze.y * self.mult > self.max_size:
            val = maze.x * self.mult if maze.y * self.mult <= self.max_size \
                    else maze.y * self.mult
            self.mult = int(floor(self.mult * (((self.max_size / val))) + 1))
        self.screen = (
            self.mlx.mlx_new_window(
                self.initScreen,
                maze.x * self.mult + (self.offsetx * 2),
                maze.y * self.mult + 400 + self.offsety,
                "cschwart | A-MAZE-ING | bgix    "))
        for y in range(self.maze.y):
            self.maze_hex.append([])
            self.maze_hex[y] = ""
            for x in range(self.maze.x):
                self.maze_hex[y] += "0"
        m: Mlx = self.mlx
        self.mouse_x = 0
        self.x = maze.x * self.mult
        self.y = maze.y * self.mult
        self.mouse_y = 0
        self.generation_started = True

        self.lights = [Vector2(x=self.x/2, y=self.y/2),
                       Vector2(x=0, y=0), Vector2(x=self.x, y=0),
                       Vector2(x=self.x, y=self.y), Vector2(x=0, y=self.y)]

        self.wall_color = 0xFF0000FF
        self.cell_color = 0xFF000099
        m: Mlx = self.mlx
        m.mlx_key_hook(self.screen, self.close_screen, self)
        m.mlx_mouse_hook(self.screen, self.mouse_hook, self)
        startpos = None

        try:
            startpos = Vector2(x=(self.entry[0]),
                               y=(self.entry[1]))
        except IndexError:
            while True:
                randX = randint(0, maze.x - 1)
                randY = randint(0, maze.y - 1)
                if maze.objects[randY][randX].Status != 42:
                    startpos = Vector2(x=randX, y=randY)
                    break
        self.step = backtracking_recursive(self, maze, startpos,
                                           None, None, perfect=self.perfect)

        self.startpos = startpos
        self.func = m.mlx_loop_hook(self.initScreen, render, self)
        m.mlx_key_hook(self.screen, self.close_screen, self)
        print(f"\nSeed: {self.seed}")
        Decorate(self)
        self.refresh(redo=True)
        m.mlx_loop(self.initScreen)

    def mouse_hook(self, x, y, button, state):
        self.mouse_x = x
        self.mouse_y = y

        if button == 1:
            if is_mouse_on_button(self, x, y, 10, 10, 200, 50):
                self.start_generation()
            elif is_mouse_on_button(self, x, y, 200, 10, 200, 50):
                self.solve_maze()
            elif is_mouse_on_button(self, x, y, 300, 10, 200, 50):
                self.change_colours()
            elif is_mouse_on_button(self, x, y, 500, 10, 200, 50):
                self.change_pattern()

    def start_generation(self):
        self.generation_started = False
        self.func = self.mlx.mlx_loop_hook(self.initScreen, render, self)

    def solve_maze(self):
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
        self.func = self.mlx.mlx_loop_hook(self.initScreen, render, self)
        self.maze = MazeGrid(x=self.maze.x, y=self.maze.y)
        from algo_backtrack_recursive import backtracking_recursive
        self.step = backtracking_recursive(self, self.maze, self.startpos,
                                           None, None, perfect=self.perfect)
        for y in range(self.maze.y):
            self.maze_hex.append([])
            self.maze_hex[y] = ""
            for x in range(self.maze.x):
                self.maze_hex[y] += "0"
        self.steps = 0
        self.solved = False
        self.refresh(redo=True)
        self.finished = False
        self.paused = False

    def change_colours(self):
        self.wall_color = 0x00FF00
        self.cell_color = 0x0000FF

    def change_pattern(self):
        pass

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
        a: memoryview = self.pixelbuff[0]
        a = a.cast('I')

        cell_size = self.mult
        cell_dimention = cell_size - self.border_size

        if redo is True:
            self.fill_image(self.pixelbuff, 0, 0,
                            self.x, self.y, col1)
            for y in range(maze.y):
                for x in range(maze.x):
                    ty = int(((cell_size) * y) + self.border_size / 2)
                    tx = int(((cell_size) * x) + self.border_size / 2)
                    self.fill_image(self.pixelbuff, ty, tx,
                                    cell_dimention, cell_dimention, col2)

        hexa_cell = hexa.hexa_grid(self.maze)
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
                    if cell.Status == 42:
                        for celly in range(int(cell_dimention -
                                               self.border_size)):
                            for cellx in range(int(cell_dimention -
                                                   self.border_size)):
                                self.fill_image(self.pixelbuff,
                                                tx + self.border_size / 2,
                                                (ty + (cell_size / 2) -
                                                 cell_dimention / 2),
                                                (cell_dimention -
                                                 self.border_size),
                                                (cell_dimention -
                                                 self.border_size),
                                                col3)
                        if cell.S == 0 and maze.objects[y + 1][x].Status == 42:
                            self.fill_image(self.pixelbuff,
                                            tx + self.border_size / 2,
                                            (ty + (cell_size / 2) -
                                             cell_dimention / 2),
                                            cell_dimention - self.border_size,
                                            (cell_dimention * 2 -
                                             self.border_size),
                                            col3)
                        if cell.N == 0 and maze.objects[y - 1][x].Status == 42:
                            self.fill_image(self.pixelbuff,
                                            tx + self.border_size / 2,
                                            (ty - (cell_size / 2) -
                                             cell_dimention / 2),
                                            cell_dimention - self.border_size,
                                            (cell_dimention * 2 -
                                             self.border_size),
                                            col3)
                        if cell.E == 0 and maze.objects[y][x + 1].Status == 42:
                            self.fill_image(self.pixelbuff,
                                            ((tx + (cell_size / 2) -
                                              cell_dimention / 2) +
                                             self.border_size / 2),
                                            ty + self.border_size / 2,
                                            cell_dimention * 2 -
                                            self.border_size,
                                            cell_dimention - self.border_size,
                                            col3)
                        if cell.W == 0 and maze.objects[y][x - 1].Status == 42:
                            self.fill_image(self.pixelbuff,
                                            ((tx - (cell_size / 2) -
                                              cell_dimention / 2) +
                                             self.border_size / 2),
                                            ty + self.border_size / 2,
                                            (cell_dimention * 2 -
                                             self.border_size),
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
        self.maze_hex = hexa_cell
        Mlx.mlx_put_image_to_window(self.mlx, self.initScreen, self.screen,
                                    self.maze_image, self.offsetx,
                                    self.offsety)

    def fill_image(self, pixelbuff: int, px, py, sx, sy, col: int) -> None:
        r, g, b = (col >> 16) & 0xFF, (col >> 8) & 0xFF, (col >> 00) & 0xFF
        lightrange = 600
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
    def close_screen(key: int, self) -> any:
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
            render(self, True)
        elif key == 114:
            from Utils.classes import MazeGrid
            self.paused = True
            self.maze = MazeGrid(x=self.maze.x, y=self.maze.y)
            self.restart()
        elif key == 99:
            self.change_color()
            self.refresh(True)
            Decorate(self)
        elif key == 115:
            self.solve_maze()
        else:
            print(key)

    def change_color(self) -> None:
        colorPalets = {
            "Ducky Duck": [0xFFFFFF00, 0xFF999900, 0xFF777700],
            "Bubble Blue": [0xFF0000FF, 0xFF000099, 0xFF000077],
            "Red Hot": [0xFFFF0000, 0xFF990000, 0xFF770000],
            "Foliage Green": [0xFF00FF00, 0xFF009900, 0xFF007700],
            "Bakus Mogus": [0xFF009999, 0xFF00FFFF, 0xFF007777],
            "Vintage Static": [0xFF000000, 0xFFFFFFFF, 0xFF000000],
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

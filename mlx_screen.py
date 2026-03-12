from mlx import Mlx
import time

mult = 100


def close_screen(key, self) -> None:
    if key == 65307:
        self.mlx.mlx_loop_exit(self.initScreen)
    elif key == 101:
        t = time.time()
        for x in range(mult):
            for y in range(mult):
                self.mlx.mlx_pixel_put(self.initScreen, self.screen, x, y, 0XFFFFFFFF)
        print(time.time() - t)


class Screen:
    def __init__(self) -> None:
        self.mlx = Mlx()
        X = 10
        Y = 10
        self.initScreen = self.mlx.mlx_init()
        self.screen = (
            self.mlx.mlx_new_window(
                self.initScreen,
                X * mult,
                Y * mult,
                "A-MAZE-ING"))
        m: Mlx = self.mlx
        Mlx.mlx_pixel_put
        m.mlx_key_hook(self.screen, close_screen, self)
        m.mlx_loop(self.initScreen)

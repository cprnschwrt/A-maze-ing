__author__ = ["bgix", "cschwart"]
__version__ = "0.0.1"

from .mazeclass import MazeGrid, MazePart, Vector2
from .utility_func import parse_configs, wait, magnitude, to_colhex
from .mlxcharacters import MlxCharacters
from .algo_backtrack_recursive import backtracking_recursive

__all__ = ["MazeGrid", "MazePart", "Vector2", "parse_configs",
           "wait", "magnitude", "to_colhex", "MlxCharacters",
           "backtracking_recursive"]

try:
    from .mlx_screen import Screen
    __all__.append(str(Screen.__name__))
except ModuleNotFoundError:
    print("MLX visualizer could not be downloaded")

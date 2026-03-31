from enum import Enum

# ▄█████ ▄▄     ▄▄▄   ▄▄▄▄  ▄▄▄▄ ▄▄▄▄▄  ▄▄▄▄
# ██     ██    ██▀██ ███▄▄ ███▄▄ ██▄▄  ███▄▄
# ▀█████ ██▄▄▄ ██▀██ ▄▄██▀ ▄▄██▀ ██▄▄▄ ▄▄██▀


class MlxCharacters(Enum):
    """A class storing special character for MLX"""
    up = ("X0X",
          "X0X",
          "X0X")

    side = ("XXX",
            "000",
            "XXX")

    corner1 = ("XXX",
               "X00",
               "X0X")

    tcorner1 = ("X0X",
                "X00",
                "X0X")

    corner2 = ("X0X",
               "X00",
               "XXX")

    corner3 = ("X0X",
               "00X",
               "XXX")

    tcorner3 = ("X0X",
                "00X",
                "X0X")

    corner4 = ("XXX",
               "00X",
               "X0X")

    full = ("0")

    none = None

    start = ("00X00",
             "0XXX0",
             "XXXXX",
             "0XXX0",
             "00X00")

    end = ("X000X",
           "0X0X0",
           "00X00",
           "0X0X0",
           "X000X")

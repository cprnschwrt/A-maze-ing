#!/usr/bin/env python3
import daedalus

config = {}

try:
    with open("triwizard3.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if value.isdigit():
                    value = int(value)
                config[key] = value
            else:
                config[line] = True
except FileNotFoundError:
    print("Error trying to read configuration file \"triwizard3.txt\".")
    exit(1)

if "ENTRY" in config:
    x, y = config["ENTRY"].split(",")
    config["ENTRY"] = (int(x), int(y))
if "EXIT" in config:
    x, y = config["EXIT"].split(",")
    config["EXIT"] = (int(x), int(y))

width = config["WIDTH"]
height = config["HEIGHT"]

grid = daedalus.create_empty_grid(width, height)

# test
print("Created grid: ", len(grid), "rows ×", len(grid[0]), "columns")
print("Cell (4,2):", grid[2][4])  # Caution: cell (x,y) but grid[y][x]... 🙄
# print("Cell (15,20):", grid[20][15]) # Correct error: leap in the dark.

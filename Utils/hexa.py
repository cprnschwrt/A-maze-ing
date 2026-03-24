from .classes import MazeGrid, MazePart


def hexa_cell(cell: MazePart) -> str:
    val = 0
    if cell.W:
        val |= 8
    if cell.S:
        val |= 4
    if cell.E:
        val |= 2
    if cell.N:
        val |= 1
    return hex(val)[2:].upper()


def binar_cell(grid: MazeGrid, x: int, y: int, hex_val: str) -> None:
    if x < 0 or x >= len(grid.objects) or y < 0 or y >= len(grid.objects[0]):
        raise IndexError(f"Les indices (x={x}, y={y}) sont hors de la grille.")

    val = int(hex_val, 16)
    cell = grid.objects[x][y]

    cell.N = 1 if val & 1 else 0
    cell.E = 1 if val & 2 else 0
    cell.S = 1 if val & 4 else 0
    cell.W = 1 if val & 8 else 0


def hexa_grid(grid: MazeGrid) -> list[str]:
    result = []
    for y in range(grid.y):
        row = []
        for x in range(grid.x):
            row.append(hexa_cell(grid.objects[y][x]))
        result.append("".join(row))
    return result

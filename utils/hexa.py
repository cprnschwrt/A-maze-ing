def hexa_cell(cell) -> str:
    val = 0
    if cell.W:
        val |= 8  # 1000
    if cell.S:
        val |= 4  # 0100
    if cell.E:
        val |= 2  # 0010
    if cell.N:
        val |= 1  # 0001
    return hex(val)[2:].upper()


def binar_cell(grid, x: int, y: int, hex_val: str):
    val = int(hex_val, 16)
    cell = grid.objects[x][y]

    cell.N = 1 if val & 1 else 0
    cell.E = 1 if val & 2 else 0
    cell.S = 1 if val & 4 else 0
    cell.W = 1 if val & 8 else 0


def hexa_grid(grid):
    result = []
    for x in range(grid.x):
        row = []
        for y in range(grid.y):
            row.append(hexa_cell(grid.objects[x][y]))
        result.append("".join(row))
    return result

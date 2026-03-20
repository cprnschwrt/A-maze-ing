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
    if x < 0 or x >= len(grid.objects) or y < 0 or y >= len(grid.objects[0]):
        raise IndexError(f"(x={x}, y={y}) should be inside the maze.")

    val = int(hex_val, 16)
    cell = grid.objects[y][x]

    cell.N = 1 if val & 1 else 0
    cell.E = 1 if val & 2 else 0
    cell.S = 1 if val & 4 else 0
    cell.W = 1 if val & 8 else 0


def hexa_grid(grid):
    result = []
    for x in range(grid.y):
        row = []
        for y in range(grid.x):
            row.append(hexa_cell(grid.objects[y][x]))
        result.append("".join(row))
    return result

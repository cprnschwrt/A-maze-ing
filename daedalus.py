cell_template = {"N": True, "E": True, "S": True, "W": True}


def create_empty_grid(width, height):
    return [
        [cell_template.copy() for x in range(width)] for y in range(height)]


def iterate_grid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            cell = grid[y][x]

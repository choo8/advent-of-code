import copy


dir = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1)
}


def parse(filename: str) -> tuple[list[list[str]], str]:
    with open(filename, "r") as f:
        lines = f.readlines()

        split_idx = lines.index("\n")

        grid = [list(row.strip()) for row in lines[:split_idx]]
        moves = "".join([row.strip() for row in lines[split_idx + 1:]])
        return grid, moves


def get_robot_pos(grid: list[list[str]]) -> tuple[int, int]:
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "@":
                return r, c


def get_boxes(grid: list[list[str]], move: str) -> tuple[bool, set[tuple[int, int]]]:
    r, c = get_robot_pos(grid)
    dr, dc = dir[move]

    r, c = r + dr, c + dc
    boxes = set()

    if grid[r][c] == "#":
        return False, boxes
    elif grid[r][c] == ".":
        return True, boxes
    
    stack, visited = [(r, c)], set()
    while len(stack):
        _r, _c = stack.pop()

        if (_r, _c) in visited:
            continue
        visited.add((_r, _c))

        # Hits a wall
        if grid[_r][_c] == "#":
            return False, boxes

        if move in ["<", ">"]:
            if grid[_r][_c] in ["O", "[", "]"]:
                stack.append((_r + dr, _c + dc))
                boxes.add((_r, _c))
        else:
            if grid[_r][_c] == "O":
                stack.append((_r + dr, _c + dc))
                boxes.add((_r, _c))
            elif grid[_r][_c] == "[":
                stack.append((_r + dr, _c + dc))
                stack.append((_r, _c + 1))
                boxes.add((_r, _c))
            elif grid[_r][_c] == "]":
                stack.append((_r + dr, _c + dc))
                stack.append((_r, _c - 1))
                boxes.add((_r, _c))

    return True, boxes


def move_robot(grid: list[list[str]], move: str) -> list[list[str]]:
    can_move, boxes = get_boxes(grid, move)

    if can_move:
        old_grid = copy.deepcopy(grid)
        dr, dc = dir[move]

        for r, c in boxes:
            grid[r][c] = "."
        for r, c in boxes:
            grid[r + dr][c + dc] = old_grid[r][c]

        robot_r, robot_c = get_robot_pos(grid)
        grid[robot_r][robot_c] = "."
        grid[robot_r + dr][robot_c + dc] = "@"

    return grid


def get_coordinates_sum(grid: list[list[str]], box: str) -> int:
    total_sum = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == box:
                total_sum += 100 * r + c
    return total_sum


def print_grid(grid: list[list[str]]):
    for row in grid:
        print("".join(row))


def part_1():
    for filename in ["example.txt", "input.txt"]:
        grid, moves = parse(filename)

        for m in moves:
            grid = move_robot(grid, m)

        total_coordinates = get_coordinates_sum(grid, "O")
        print(f"[Part 1] Sum of boxes' GPS coordinates in {filename}: {total_coordinates}")


def scale_warehouse(grid: list[list[str]]) -> list[list[str]]:
    scaled_grid = []
    for row in grid:
        scaled_row = []
        for cell in row:
            if cell == "O":
                scaled_row.append("[")
                scaled_row.append("]")
            elif cell == "@":
                scaled_row.append("@")
                scaled_row.append(".")
            else:
                scaled_row.append(cell)
                scaled_row.append(cell)
        scaled_grid.append(scaled_row)
    return scaled_grid


def part_2():
    for filename in ["example.txt", "input.txt"]:
        grid, moves = parse(filename)
        grid = scale_warehouse(grid)

        for m in moves:
            grid = move_robot(grid, m)

        total_coordinates = get_coordinates_sum(grid, "[")
        print(f"[Part 2] Sum of boxes' GPS coordinates in {filename}: {total_coordinates}")


if __name__ == "__main__":
    part_1()
    part_2()

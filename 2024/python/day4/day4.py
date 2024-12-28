from functools import partial
from itertools import product


def parse(filename: str) -> list[list[str]]:
    with open(filename, "r") as f:
        rows = f.readlines()

    return [list(row.strip()) for row in rows]


def is_in_grid(r: int, c: int, m: int, n: int) -> bool:
    return r >= 0 and r < m and c >= 0 and c < n


def count_xmas(grid: list[list[str]], coords: tuple[int, int]) -> int:
    r, c = coords
    m, n = len(grid), len(grid[0])
    num_xmas = 0

    if grid[r][c] != "X":
        return num_xmas

    letters = ["M", "A", "S"]

    # Up, Up-Right, Right, Down-Right, Down, Down-Left, Left, Up-Left
    for dr, dc in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]:
        _r, _c = r, c

        for i in range(3):
            _r, _c = _r + dr, _c + dc
           
            if not is_in_grid(_r, _c, m, n) or grid[_r][_c] != letters[i]:
                break

            if i == 2:
                num_xmas += 1

    return num_xmas


def part_1():
    for filename in ["example.txt", "input.txt"]:
        grid = parse(filename)

        m, n = len(grid), len(grid[0])
        coords = list(product([r for r in range(m)], [c for c in range(n)]))

        num_xmas = sum(map(partial(count_xmas, grid), coords))
                
        print(f"[Part 1] Number of 'XMAS' in {filename}: {num_xmas}")


def rotate(letters: list[str]) -> list[list[str]]:
    return [letters[idx:] + letters[:idx] for idx in range(len(letters))]


def count_x_mas(grid: list[list[str]], coords: tuple[int, int]) -> int:
    r, c = coords
    m, n = len(grid), len(grid[0])
    num_x_mas = 0

    if grid[r][c] != "A" or r - 1 < 0 or r + 1 >= m or c - 1 < 0 or c + 1 >= n:
        return num_x_mas
    
    for letters in rotate(["M", "M", "S", "S"]):
        corners = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        corner_coords = [(r + dr, c + dc) for dr, dc in corners]
        corner_letters = [grid[_r][_c] for _r, _c in corner_coords]

        if all([l == cur_l for l, cur_l in zip(letters, corner_letters)]):
            num_x_mas += 1

    return num_x_mas


def part_2():
    for filename in ["example.txt", "input.txt"]:
        grid = parse(filename)

        m, n = len(grid), len(grid[0])
        coords = list(product([r for r in range(m)], [c for c in range(n)]))

        num_x_mas = sum(map(partial(count_x_mas, grid), coords))

        print(f"[Part 2] Number of 'X-MAS' in {filename}: {num_x_mas}")


if __name__ == "__main__":
    part_1()
    part_2()

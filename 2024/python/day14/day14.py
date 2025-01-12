from collections import defaultdict
from collections.abc import Iterable
from functools import reduce
from operator import mul
import re


config = {
            "example.txt": {
                "width": 11,
                "height": 7
            },
            "input.txt": {
                "width": 101,
                "height": 103
            }
        }


def parse(filename: str) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    with open(filename, "r") as f:
        content = f.read()
        pos = [(int(x), int(y)) for (x, y) in re.findall(r"p=(\d+),(\d+)", content)]
        vs = [(int(vx), int(vy)) for (vx, vy) in re.findall(r"v=(-?\d+),(-?\d+)", content)]
        return list(zip(pos, vs))


def get_pos_after_seconds(x: int, y: int, vx: int, vy: int, width: int, height: int, num_seconds: int) -> tuple[int, int]:
    return (x + vx * num_seconds) % width, (y + vy * num_seconds) % height


def get_quadrant(x: int, y: int, width: int, height: int) -> int:
    mid_x, mid_y = (width - 1) / 2, (height - 1) / 2
    # Not in any quadrants
    if x == mid_x or y == mid_y:
        return 0
    # Top left
    elif x < mid_x and y < mid_y:
        return 1
    # Top right
    elif x > mid_x and y < mid_y:
        return 2
    # Bottom right
    elif x > mid_x and y > mid_y:
        return 3
    # Bottom left
    else:
        return 4


def part_1():
    for filename in ["example.txt", "input.txt"]:
        robots = parse(filename)

        width, height = config[filename]["width"], config[filename]["height"]
        quadrants = defaultdict(int)
        for (x, y), (vx, vy) in robots:
            _x, _y = get_pos_after_seconds(x, y, vx, vy, width, height, 100)
            q = get_quadrant(_x, _y, width, height)
            quadrants[q] += 1
        
        safety_factor = reduce(mul, [quadrants[i] for i in range(1, 5)])

        print(f"[Part 1] Safety factor in {filename}: {safety_factor}")


def get_grid_after_seconds(robots: Iterable[tuple[tuple[int, int], tuple[int, int]]], width: int, height: int, num_seconds: int) -> tuple[list[list[int]], bool]:
    visited, grid = set(), [[0 for _ in range(width)] for _ in range(height)]

    for (x, y), (vx, vy) in robots:
        _x, _y = get_pos_after_seconds(x, y, vx, vy, width, height, num_seconds)
        grid[_y][_x] = 1
        visited.add((_y, _x))

    return grid, len(visited) == len(robots)


def print_grid(grid: list[list[int]]):
    for row in grid:
        print("".join([str(x) for x in row]))


def part_2():
    for filename in ["input.txt"]:
        robots = parse(filename)

        width, height = config[filename]["width"], config[filename]["height"]
        for i in range(30000):
            grid, no_overlaps = get_grid_after_seconds(robots, width, height, i)
            if no_overlaps:
                print(f"After {i} seconds")
                print_grid(grid)


if __name__ == "__main__":
    part_1()
    part_2()

from collections import defaultdict
from itertools import combinations
from math import gcd


def parse(filename: str) -> list[list[str]]:
    with open(filename, "r") as f:
        rows = f.readlines()
        return [list(r.strip()) for r in rows]


def get_antennas(grid: list[list[str]]) -> dict[str, list[tuple[int, int]]]:
    antennas = defaultdict(list)

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell != ".":
                antennas[cell].append((r, c))

    return antennas


def is_in_grid(grid: list[list[str]], r: int, c: int) -> bool:
    return r >= 0 and r < len(grid) and c >= 0 and c < len(grid[0])


def get_antinodes(grid: list[list[str]], locations: list[tuple[int, int]]) -> set[tuple[int, int]]:
    antinodes = set()
    for idx1, idx2 in combinations(range(len(locations)), 2):
        a1, a2 = locations[idx1], locations[idx2]

        dr, dc = a1[0] - a2[0], a1[1] - a2[1]
        if is_in_grid(grid, a1[0] + dr, a1[1] + dc):
            antinodes.add((a1[0] + dr, a1[1] + dc))
        
        dr, dc = a2[0] - a1[0], a2[1] - a1[1]
        if is_in_grid(grid, a2[0] + dr, a2[1] + dc):
            antinodes.add((a2[0] + dr, a2[1] + dc))

    return antinodes


def part_1():
    for filename in ["example.txt", "input.txt"]:
        grid = parse(filename)
        antennas = get_antennas(grid)

        antinodes = set()
        for locations in antennas.values():
            if len(locations) >= 2:
                antinodes = antinodes | get_antinodes(grid, locations)

        print(f"[Part 1] Number of unique antinodes in {filename}: {len(antinodes)}")


def get_new_antinodes(grid: list[list[str]], locations: list[tuple[int, int]]) -> set[tuple[int, int]]:
    antinodes = set()
    for idx1, idx2 in combinations(range(len(locations)), 2):
        a1, a2 = locations[idx1], locations[idx2]

        antinodes.add(a1)
        antinodes.add(a2)

        factor = 1
        dr, dc = a1[0] - a2[0], a1[1] - a2[1]
        _gcd = gcd(dr, dc)
        dr, dc = dr / _gcd, dc / _gcd
        while is_in_grid(grid, a1[0] + (dr * factor), a1[1] + (dc * factor)):
            antinodes.add((a1[0] + (dr * factor), a1[1] + (dc * factor)))
            factor += 1

        factor = 1
        dr, dc = a2[0] - a1[0], a2[1] - a1[1]
        _gcd = gcd(dr, dc)
        dr, dc = dr / _gcd, dc / _gcd
        while is_in_grid(grid, a2[0] + (dr * factor), a2[1] + (dc * factor)):
            antinodes.add((a2[0] + (dr * factor), a2[1] + (dc * factor)))
            factor += 1

    return antinodes


def part_2():
    for filename in ["example.txt", "input.txt"]:
        grid = parse(filename)
        anetennas = get_antennas(grid)

        antinodes = set()
        for locations in anetennas.values():
            if len(locations) >= 2:
                antinodes = antinodes | get_new_antinodes(grid, locations)

        print(f"[Part 2] Number of unique antinodes after model update in {filename}: {len(antinodes)}")


if __name__ == "__main__":
    part_1()
    part_2()

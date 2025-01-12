from collections import defaultdict
from collections.abc import Callable


def parse(filename: str) -> list[list[str]]:
    with open(filename, "r") as f:
        rows = f.readlines()
        return [list(row.strip()) for row in rows]


def is_in_grid(grid: list[list[str]], r: int, c: int) -> bool:
    return r >= 0 and r < len(grid) and c >= 0 and c < len(grid[0])


def get_fences(visited: set[tuple[int, int]]) -> dict[tuple[int, int], int]:
    fences, fence_deltas = {}, [(-0.5, 0), (0.5, 0), (0, -0.5), (0, 0.5)]
    for r, c in visited:
        for idx, (dr, dc) in enumerate(fence_deltas):
            fence_r, fence_c = r + dr, c + dc

            if (fence_r, fence_c) in fences:
                del fences[(fence_r, fence_c)]
            else:
                fences[(fence_r, fence_c)] = idx

    return fences


def get_num_fences(visited: set[tuple[int, int]]) -> int:
    return len(get_fences(visited).keys())


def get_region_cost(grid: list[list[int]], r: int, c: int, fence_cost_func: Callable[[set[tuple[int, int]]], int]) -> tuple[set[tuple[int, int]], int]:
    visited = set()
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    stack = [(r, c)]
    while len(stack) > 0:
        _r, _c = stack.pop()

        if (_r, _c) in visited:
            continue
        visited.add((_r, _c))

        for dr, dc in dir:
            new_r, new_c = _r + dr, _c + dc
            if is_in_grid(grid, new_r, new_c) and grid[_r][_c] == grid[new_r][new_c]:
                stack.append((new_r, new_c))

    fence_cost = fence_cost_func(visited)
    region_cost = len(visited) * fence_cost

    return visited, region_cost


def get_fence_cost(grid: list[list[str]], fence_cost_func: Callable[[set[tuple[int, int]]], int]) -> int:
    total_visited, total_cost = set(), 0

    for r, row in enumerate(grid):
        for c, _ in enumerate(row):
            if (r, c) in total_visited:
                continue

            region_visited, region_cost = get_region_cost(grid, r, c, fence_cost_func)
            total_visited = total_visited.union(region_visited)
            total_cost += region_cost

    return total_cost


def part_1():
    for filename in ["example.txt", "input.txt"]:
        grid = parse(filename)
        total_cost = get_fence_cost(grid, get_num_fences)
        print(f"[Part 1] Cost of fencing all regions on map in {filename}: {total_cost}")


def get_num_contiguous(sides: list[int]) -> int:
    num_contiguous = 1

    prev = sides[0]
    for s in sides[1:]:
        if s != prev + 1:
            num_contiguous += 1
        prev = s

    return num_contiguous


def get_num_sides(visited: set[tuple[int, int]]) -> int:
    num_horizontals, num_verticals = defaultdict(lambda: defaultdict(list)), defaultdict(lambda: defaultdict(list))

    fences = get_fences(visited)
    for (r, c), idx in fences.items():
        if int(r) != r:
            num_horizontals[r][idx].append(c)
        if int(c) != c:
            num_verticals[c][idx].append(r)

    num_sides = 0
    for r, sides in num_horizontals.items():
        for _, _sides in sides.items():
            num_sides += get_num_contiguous(list(sorted(_sides)))
    for c, sides in num_verticals.items():
        for _, _sides in sides.items():
            num_sides += get_num_contiguous(list(sorted(_sides)))

    return num_sides


def part_2():
    for filename in ["example.txt", "input.txt"]:
        grid = parse(filename)
        total_cost = get_fence_cost(grid, get_num_sides)
        print(f"[Part 2] Cost of discounted fencing in {filename}: {total_cost}")


if __name__ == "__main__":
    part_1()
    part_2()

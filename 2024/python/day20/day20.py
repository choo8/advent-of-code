import networkx as nx


def parse(filename: str) -> list[list[str]]:
    with open(filename, "r") as f:
        rows = f.readlines()
        return [list(r.strip()) for r in rows]


def is_in_grid(r: int, c: int, grid: list[list[str]]) -> bool:
    return r >= 0 and r < len(grid) and c >= 0 and c < len(grid[0])


def get_coords_within_dist(grid:list[list[str]], r: int, c: int, cheat_dist: int) -> list[tuple[int, int]]:
    coords = []
    for _r in range(r - cheat_dist, r + cheat_dist + 1):
        for _c in range(c - cheat_dist, c + cheat_dist + 1):
            if (r, c) != (_r, _c) and is_in_grid(_r, _c, grid) and grid[_r][_c] != "#":
                if abs(r - _r) + abs(c - _c) <= cheat_dist:
                    coords.append((_r, _c))
    return coords


def create_graph(grid: list[list[str]]) -> nx.Graph:
    graph = nx.Graph()

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "#":
                continue
            graph.add_node((r, c))

    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "#":
                continue
            for dr, dc in dir:
                _r, _c = r + dr, c + dc
                if grid[_r][_c] == ".":
                    graph.add_edge((r, c), (_r, _c), weight=1)

    return graph


def get_cell_coord(grid: list[list[str]], cell: str) -> tuple[int, int]:
    for r, row in enumerate(grid):
        for c, _cell in enumerate(row):
            if cell == _cell:
                return (r, c)


def num_cheats(grid: list[list[str]], cheat_dist:int, threshold: int) -> int:
    graph = create_graph(grid)
    start_r, start_c = get_cell_coord(grid, "S")
    end_r, end_c = get_cell_coord(grid, "E")
    shortest_path = nx.shortest_path(graph, (start_r, start_c), (end_r, end_c))

    num_cheats = 0
    for i, (r, c) in enumerate(shortest_path):
        coords = get_coords_within_dist(grid, r, c, cheat_dist)
        for _r, _c in coords:
            d = abs(r - _r) + abs(c - _c)
            if (_r, _c) in shortest_path[i + 1:] and (shortest_path.index((_r, _c)) - i) - d >= threshold:
                num_cheats += 1

    return num_cheats


def part_1():
    for filename in ["example.txt", "input.txt"]:
        grid = parse(filename)
        print(f"[Part 1] Number of cheats that save 100 picoseconds in {filename}: {num_cheats(grid, 2, 100)}")


def part_2():
    for filename in ["example.txt", "input.txt"]:
        grid = parse(filename)
        print(f"[Part 2] Number of cheats that save 100 picoseconds in {filename}: {num_cheats(grid, 20, 100)}")


if __name__ == "__main__":
    part_1()
    part_2()

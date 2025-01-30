import networkx as nx


dir_dict = {
    0: (0, 1), # east
    1: (1, 0), # south
    2: (0, -1), # west
    3: (-1, 0) # north
}


def parse(filename: str) -> list[list[str]]:
    with open(filename, "r") as f:
        rows = f.readlines()
        return [list(row.strip()) for row in rows]


def get_cell(grid: list[list[str]], cell: str) -> tuple[int, int]:
    for r, row in enumerate(grid):
        for c, _cell in enumerate(row):
            if _cell == cell:
                return (r, c)


def create_graph(grid: list[list[str]]) -> nx.DiGraph:
    graph = nx.DiGraph()

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "#":
                continue

            for dir in range(4):
                graph.add_node((r, c, dir))

            for dir in range(4):
                graph.add_edge((r, c, dir), (r, c, (dir + 1) % 4), weight=1000)
                graph.add_edge((r, c, dir), (r, c, (dir - 1) % 4), weight=1000)

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "#":
                continue

            for dir in range(4):
                dr, dc = dir_dict[dir]
                if grid[r + dr][c + dc] != "#":
                    graph.add_edge((r, c, dir), (r + dr, c + dc, dir), weight=1)

    return graph


def get_score(grid: list[list[str]]) -> int:
    graph = create_graph(grid)
    deer_r, deer_c = get_cell(grid, "S")
    end_r, end_c = get_cell(grid, "E")

    score = min([nx.shortest_path_length(graph, (deer_r, deer_c, 0), (end_r, end_c, dir), weight="weight") for dir in range(4)])

    return score


def part_1():
    for filename in ["example.txt", "input.txt"]:
        grid = parse(filename)
        score = get_score(grid)
        print(f"[Part 1] Lowest score possible in {filename}: {score}")


def get_num_tiles(grid: list[list[str]]) -> int:
    graph = create_graph(grid)
    deer_r, deer_c = get_cell(grid, "S")
    end_r, end_c = get_cell(grid, "E")

    min_score = get_score(grid)
    tiles = set()
    for dir in range(4):
        if nx.shortest_path_length(graph, (deer_r, deer_c, 0), (end_r, end_c, dir), weight="weight") == min_score:
            for path in nx.all_shortest_paths(graph, (deer_r, deer_c, 0), (end_r, end_c, dir), weight="weight"):
                for _r, _c, _ in path:
                    tiles.add((_r, _c))

    return len(tiles)


def part_2():
    for filename in ["example.txt", "input.txt"]:
        grid = parse(filename)
        num_tiles = get_num_tiles(grid)
        print(f"[Part 2] NUmber of tiles in {filename}: {num_tiles}")


if __name__ == "__main__":
    part_1()
    part_2()

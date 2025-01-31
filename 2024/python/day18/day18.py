import networkx as nx


grid_size = {
    "example.txt": (7, 7),
    "input.txt": (71, 71)
}
num_bytes = {
    "example.txt": 12,
    "input.txt": 1024
}


def parse(filename: str) -> list[tuple[int, int]]:
    with open(filename, "r") as f:
        lines = f.readlines()
        coords = [line.split(",") for line in lines]
        return [(int(coord[1]), int(coord[0])) for coord in coords]


def is_in_grid(r: int, c: int, width: int, height: int) -> bool:
    return r >= 0 and r < width and c >= 0 and c < height


def create_grid(coords: list[tuple[int, int]], width: int, height: int, bytes: int) -> list[list[str]]:
    grid = [["." for _ in range(width)] for _ in range(height)]

    for r, c in coords[:bytes]:
        if is_in_grid(r, c, width, height):
            grid[r][c] = "#"

    return grid


def create_graph(grid: list[list[str]]) -> nx.Graph:
    graph = nx.Graph()

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell != ".":
                continue
            graph.add_node((r, c))

    width, height = len(grid[0]), len(grid)
    dir = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell != ".":
                continue
            for dr, dc in dir:
                _r, _c = r + dr, c + dc
                if is_in_grid(_r, _c, width, height) and grid[_r][_c] == "." and not graph.has_edge((r, c), (_r, _c)):
                    graph.add_edge((r, c), (_r, _c), weight=1)
    
    return graph


def part_1():
    for filename in ["example.txt", "input.txt"]:
        width, height = grid_size[filename]
        bytes = num_bytes[filename]
        coords = parse(filename)
        grid = create_grid(coords, width, height, bytes)
        graph = create_graph(grid)
        num_steps = nx.shortest_path_length(graph, (0, 0), (width - 1, height - 1))
        print(f"[Part 1] Minimum number of steps in {filename}: {num_steps}")


def part_2():
    for filename in ["example.txt", "input.txt"]:
        width, height = grid_size[filename]
        bytes = num_bytes[filename]
        coords = parse(filename)
        
        for i in range(bytes, len(coords)):
            grid = create_grid(coords, width, height, i)
            graph = create_graph(grid)
            if not nx.has_path(graph, (0, 0), (width - 1, height - 1)):
                print(f"[Part 2] Coordinates of first byte that blocks exit in {filename}: {(coords[i - 1][1], coords[i - 1][0])}")
                break


if __name__ == "__main__":
    part_1()
    part_2()

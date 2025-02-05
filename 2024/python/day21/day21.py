from functools import cache
import networkx as nx


keypad = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["", "0", "A"]
]
dir_pad = [
    ["", "^", "A"],
    ["<", "v", ">"]
]
dir_dict = {
    (-1, 0): "^",
    (1, 0): "v",
    (0, -1): "<",
    (0, 1): ">"
}


def parse(filename: str) -> list[str]:
    with open(filename, "r") as f:
        codes = f.readlines()
        return [code.strip() for code in codes]


def is_in_pad(pad: list[list[str]], r: int, c: int) -> bool:
    return r >= 0 and r < len(pad) and c >= 0 and c < len(pad[0])


def create_cached_paths(pad: list[list[str]]) -> dict[tuple[int, int], list[str]]:
    graph = nx.DiGraph()

    for row in pad:
        for n in row:
            if n == "":
                continue
            graph.add_node(n)
    
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r, row in enumerate(pad):
        for c, n in enumerate(row):
            if n == "":
                continue
            for dr, dc in dir:
                _r, _c = r + dr, c + dc
                if is_in_pad(pad, _r, _c) and pad[_r][_c] != "":
                    graph.add_edge(n, pad[_r][_c], direction=dir_dict[(dr, dc)])

    cached_paths = {}
    for n in graph.nodes:
        for m in graph.nodes:
            cached_paths[(n, m)] = ["".join([graph.edges[src, dst]["direction"] for src, dst in zip(path, path[1:])]) for path in nx.all_shortest_paths(graph, n, m)]
    
    return cached_paths


def get_coords(cell: int, pad: list[list[str]]) -> tuple[int, int]:
    for r, row in enumerate(pad):
        for c, _cell in enumerate(row):
            if cell == _cell:
                return (r, c)


@cache
def get_shortest_sequence(code: str, cur_bot: int, num_bots: int) -> int:
    if cur_bot > num_bots:
        return len(code)
    seq_len = 0
    if cur_bot == 0:
        cached_paths = create_cached_paths(keypad)
    else:
        cached_paths = create_cached_paths(dir_pad)
    for src, dst in zip("A" + code, code): # Arm initially on 'A'
            seq_len += min([get_shortest_sequence(path + "A", cur_bot + 1, num_bots) for path in cached_paths[(src, dst)]])
    return seq_len


def part_1():
    for filename in ["example.txt", "input.txt"]:
        codes = parse(filename)
        sum_complexity = 0
        for code in codes:
            sum_complexity += int(code[:3]) * get_shortest_sequence(code, 0, 2)
        print(f"[Part 1] Sum of complexities in {filename}: {sum_complexity}")


def part_2():
    for filename in ["example.txt", "input.txt"]:
        codes = parse(filename)
        sum_complexity = 0
        for code in codes:
            sum_complexity += int(code[:3]) * get_shortest_sequence(code, 0, 25)
        print(f"[Part 2] Sum of complexities in {filename}: {sum_complexity}")


if __name__ == "__main__":
    part_1()
    part_2()

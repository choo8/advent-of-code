import networkx as nx


def parse(filename: str) -> list[list[str]]:
    with open(filename, "r") as f:
        lines = f.readlines()
        return [line.strip().split("-") for line in lines]


def create_graph(connections: list[list[str]]) -> nx.Graph:
    graph = nx.Graph()

    for src, dst in connections:
        graph.add_edge(src, dst)

    return graph


def get_triplets(connections: list[list[str]]) -> list[list[str]]:
    graph = nx.Graph()

    for src, dst in connections:
        graph.add_node(src)
        graph.add_node(dst)
        graph.add_edge(src, dst)

    triplets = []
    for n in graph.nodes:
        if not n.startswith("t"):
            continue
        for m in graph.neighbors(n):
            for o in set(graph.neighbors(n)) & set(graph.neighbors(m)):
                if {n, m, o} not in triplets:
                    triplets.append({n, m, o})
    
    return [list(triplet) for triplet in triplets]


def part_1():
    for filename in ["example.txt", "input.txt"]:
        connections = parse(filename)
        triplets = get_triplets(connections)
        print(f"[Part 1] Number of triplets that contain at least one computer with name that starts with 't' in {filename}: {len(triplets)}")


def part_2():
    for filename in ["example.txt", "input.txt"]:
        connections = parse(filename)
        graph = create_graph(connections)
        largest_clique = []
        for c in nx.find_cliques(graph):
            if len(c) > len(largest_clique):
                largest_clique = c
        password = ",".join(sorted(largest_clique))
        print(f"[Part 2] Password to LAN party in {filename}: {password}")


if __name__ == "__main__":
    part_1()
    part_2()

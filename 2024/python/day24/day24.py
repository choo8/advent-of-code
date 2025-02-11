import networkx as nx


def parse(filename: str) -> tuple[dict[str, int], dict[str, list[str]]]:
    with open(filename, "r") as f:
        wire_vals, val_deps = {}, {}
        for line in f.readlines():
            line = line.strip()
            if ":" in line:
                wire, val = line.split(": ")
                wire_vals[wire] = int(val)
            elif "->" in line:
                i, o = line.split(" -> ")
                deps = i.split(" ")
                val_deps[o] = deps

        return wire_vals, val_deps


def create_graph(wire_vals: dict[str, int], val_deps: dict[str, list[str]]) -> nx.DiGraph:
    graph = nx.DiGraph()

    for wire in wire_vals.keys():
        graph.add_node(wire)
    for o, dep in val_deps.items():
        graph.add_node(dep[0])
        graph.add_node(dep[-1])
        graph.add_node(o)

        graph.add_edge(dep[0], o)
        graph.add_edge(dep[-1], o)

    return graph


def calculate_output(wire_vals: dict[str, int], val_deps: dict[str, list[str]]) -> int:
    graph = create_graph(wire_vals, val_deps)

    for n in nx.topological_sort(graph):
        if n not in wire_vals:
            i1, op, i2 = val_deps[n]
            if op == "AND":
                wire_vals[n] = wire_vals[i1] & wire_vals[i2]
            elif op == "OR":
                wire_vals[n] = wire_vals[i1] | wire_vals[i2]
            elif op == "XOR":
                wire_vals[n] = wire_vals[i1] ^ wire_vals[i2]

    output = 0
    for idx, wire in enumerate(sorted(filter(lambda x: x.startswith("z"), wire_vals.keys()))):
        if wire_vals[wire] == 1:
            output += 2 ** idx

    return output


def part_1():
    for filename in ["example.txt", "input.txt"]:
        wire_vals, val_deps = parse(filename)
        output = calculate_output(wire_vals, val_deps)
        print(f"[Part 1] Output from {filename}: {output}")


def validate_adder(val_deps: dict[str, list[str]]) -> str:
    zs = list(filter(lambda x: x.startswith("z"), val_deps.keys()))

    wrong_wires = []
    for o, deps in val_deps.items():
        # If output is z, has to be XOR unless is last bit
        if o.startswith("z") and deps[1] != "XOR" and o != f"z{len(zs) - 1}":
            wrong_wires.append(o)
            continue
        # If output is not z and inputs are not x, y, then has to be AND / OR
        if not o.startswith("z") and not deps[0].startswith("x") and not deps[2].startswith("y") and not deps[2].startswith("x") and not deps[0].startswith("y") and deps[1] == "XOR":
            wrong_wires.append(o)
            continue
        # If input is x, y with XOR gate, should have another XOR gate with this output as input
        if deps[1] == "XOR" and ((deps[0].startswith("x") and deps[2].startswith("y")) or (deps[2].startswith("x") and deps[0].startswith("y"))) and deps[0] not in ["x00", "y00"] and deps[2] not in ["x00", "y00"]:
            valid = False
            for _o, _deps in val_deps.items():
                if _deps[1] == "XOR" and (_deps[0] == o or _deps[2] == o):
                    valid = True
                    break
            if not valid:
                wrong_wires.append(o)
                continue
        if deps[1] == "AND" and ((deps[0].startswith("x") and deps[2].startswith("y")) or (deps[2].startswith("x") and deps[0].startswith("y"))) and deps[0] not in ["x00", "y00"] and deps[2] not in ["x00", "y00"]:
            valid = False
            for _o, _deps in val_deps.items():
                if _deps[1] == "OR" and (_deps[0] == o or _deps[2] == o):
                    valid = True
            if not valid:
                wrong_wires.append(o)
                continue

    return ",".join(sorted(wrong_wires))


def part_2():
    for filename in ["example.txt", "input.txt"]:
        _, val_deps = parse(filename)
        wrong_wires = validate_adder(val_deps)
        print(f"[Part 2] Wrong wires in {filename}: {wrong_wires}")


if __name__ == "__main__":
    part_1()
    part_2()

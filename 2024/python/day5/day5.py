from collections import defaultdict


def parse(filename: str) -> tuple[list[str], list[str]]:
    with open(filename, "r") as f:
        lines = f.readlines()

        split_idx = lines.index("\n")

    return [l.strip() for l in lines[:split_idx]], [l.strip() for l in lines[split_idx + 1:]]


def order_updates(rule_dict: dict[int, set[int]], updates: list[int]) -> list[int]:
    local_rule_dict, visited = {}, {}
    for u in updates:
        local_rule_dict[u] = rule_dict[u] & set(updates)
        visited[u] = False

    sorted_updates = []

    def dfs(node: int):
        if visited[node]:
            return
        visited[node] = True

        for m in local_rule_dict[node]:
            dfs(m)

        sorted_updates.append(node)

    for u in visited:
        if not visited[u]:
            dfs(u)

    return sorted_updates


def part_1():
    for filename in ["example.txt", "input.txt"]:
        rules, updates = parse(filename)

        rule_dict = defaultdict(set)
        for r in rules:
            pre, post = [int(n) for n in r.split("|")]
            rule_dict[post].add(pre)

        midpage_sum = 0
        for u in updates:
            u_list = [int(n) for n in u.split(",")]

            if u_list == order_updates(rule_dict, u_list):
                midpage_sum += u_list[int(len(u_list) / 2)]

        print(f"[Part 1] Sum of middle page number of correctly-order updates in {filename}: {midpage_sum}")


def part_2():
    for filename in ["example.txt", "input.txt"]:
        rules, updates = parse(filename)

        rule_dict = defaultdict(set)
        for r in rules:
            pre, post = [int(n) for n in r.split("|")]
            rule_dict[post].add(pre)

        midpage_sum = 0
        for u in updates:
            u_list = [int(n) for n in u.split(",")]
            sorted_list = order_updates(rule_dict, u_list)

            if u_list != sorted_list:
                midpage_sum += sorted_list[int(len(sorted_list) / 2)]

        print(f"[Part 2] Sum of middle page number of corrected updates in {filename}: {midpage_sum}")


if __name__ == "__main__":
    part_1()
    part_2()

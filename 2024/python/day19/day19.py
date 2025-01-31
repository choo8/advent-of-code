from functools import cache


def parse(filename: str) -> tuple[tuple[str], list[str]]:
    with open(filename, "r") as f:
        lines = f.readlines()
        towels = tuple(lines[0].strip().split(", "))
        designs = [d.strip() for d in lines[2:]]
    return towels, designs


@cache
def exists(design: str, towels: tuple[str]) -> bool:
    if design in towels:
        return True
    for t in towels:
        if design.startswith(t) and exists(design[len(t):], towels):
            return True
    return False


def part_1():
    for filename in ["example.txt", "input.txt"]:
        towels, designs = parse(filename)
        num_possible = sum([exists(d, towels) for d in designs])
        print(f"[Part 1] Number of possible designs in {filename}: {num_possible}")


@cache
def num_possibilities(design: str, towels: tuple[str]) -> int:
    num_pos = 0
    if design in towels:
        num_pos += 1
    for t in towels:
        if design.startswith(t) and design != t:
            num_pos += num_possibilities(design[len(t):], towels)
    return num_pos


def part_2():
    for filename in ["example.txt", "input.txt"]:
        towels, designs = parse(filename)
        num_diff_ways = sum([num_possibilities(d, towels) for d in designs])
        print(f"[Part 2] Number of different ways in {filename}: {num_diff_ways}")


if __name__ == "__main__":
    part_1()
    part_2()

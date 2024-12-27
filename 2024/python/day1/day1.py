from collections import Counter


def parse(filename: str) -> tuple[list[str], list[str]]:
    with open(filename, "r") as f:
        lines = f.readlines()

    l1, l2 = map(list, zip(*[l.split() for l in lines]))
    return l1, l2


def part_1():
    for filename in ["example.txt", "input.txt"]:
        l1, l2 = parse(filename)

        l1.sort()
        l2.sort()

        total_dist = sum(map(lambda x: abs(int(x[0]) - int(x[1])), zip(l1, l2)))

        print(f"[Part 1] Total distance for {filename}: {total_dist}")


def part_2():
    for filename in ["example.txt", "input.txt"]:
        l1, l2 = parse(filename)

        c2 = Counter(l2)
        
        sim_score = sum(map(lambda x: int(x) * c2[x], l1))

        print(f"[Part 2] Similarity score for {filename}: {sim_score}")


if __name__ == "__main__":
    part_1()
    part_2()

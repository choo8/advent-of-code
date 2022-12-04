import argparse

def get_item_priority(item: str) -> int:
    if item >= "a" and item <= "z":
        return ord(item) - ord("a") + 1
    else:
        return ord(item) - ord("A") + 27

parser = argparse.ArgumentParser(prog = "AOC Day 3", description = "AOC Day 3 Solver")
parser.add_argument("-f", "--filename", dest = "filename")

args = parser.parse_args()

with open(args.filename, "r") as f:
    lines = f.readlines()

    # Part 1
    priorities_sum = 0

    for line in lines:
        rucksack = line.strip()
        num_items = len(rucksack)
        first_compartment, second_compartment = rucksack[:(num_items // 2)], rucksack[(num_items // 2):]
        
        for item in set(first_compartment).intersection(set(second_compartment)):
            priorities_sum += get_item_priority(item)

    # Part 2
    group_priorities_sum = 0

    for idx in range(0, len(lines), 3):
        group = lines[idx:idx + 3]
        group_common_item = set()

        for line in group:
            rucksack = line.strip()

            if len(group_common_item) == 0:
                group_common_item = group_common_item.union(set(rucksack))
            else:
                group_common_item = group_common_item.intersection(set(rucksack))

        for item in group_common_item:
            group_priorities_sum += get_item_priority(item)

    print(f"Sum of priorities: {priorities_sum}, Sum of priorities of badges: {group_priorities_sum}")

import argparse

parser = argparse.ArgumentParser(prog = "AOC Day 1", description = "AOC Day 1 Solver")
parser.add_argument("-f", "--filename", dest = "filename")

args = parser.parse_args()

with open(args.filename, "r") as f:
    lines = f.readlines()

    elves, cur_elf = [], 0
    for line in lines:
        if line != "\n":
            cur_elf += int(line.strip())
        else:
            elves.append(cur_elf)
            cur_elf = 0

    print(f"Calories carried by Elf with most calories: {max(elves)}")
    print(f"Total calories carried by elvies with top 3 calories: {sum(sorted(elves, reverse=True)[:3])}")
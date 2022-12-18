import argparse

parser = argparse.ArgumentParser(prog = "AOC Day 4", description = "AOC Day 4 Solver")
parser.add_argument("-f", "--filename", dest = "filename")

args = parser.parse_args()

with open(args.filename, "r") as f:
    lines = f.readlines()

    num_total_overlaps = 0
    num_partial_overlaps = 0
    for line in lines:
        elf1, elf2 = line.split(",")

        elf1_left, elf1_right = elf1.split("-")
        elf2_left, elf2_right = elf2.split("-")

        # Convert from str to int
        elf1_left, elf1_right = int(elf1_left), int(elf1_right)
        elf2_left, elf2_right = int(elf2_left), int(elf2_right)

        # Part 1
        # Check if elf1's range is within elf2's
        if elf1_left >= elf2_left and elf1_right <= elf2_right:
            num_total_overlaps += 1
        # Check if elf2's range is within elf1's
        elif elf2_left >= elf1_left and elf2_right <= elf1_right:
            num_total_overlaps += 1

        # Part 2
        # Check if elf1's range is separate and smaller than elf2's
        if elf1_right < elf2_left:
            continue
        # Check if elf1's range is separate and larger than elf2's
        elif elf1_left > elf2_right:
            continue
        else:
            num_partial_overlaps += 1

    print(f"Number of totally overlapping assignments: {num_total_overlaps}, Number of partially overlapping assignments: {num_partial_overlaps}")
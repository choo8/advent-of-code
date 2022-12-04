import argparse

parser = argparse.ArgumentParser(prog = "AOC Day 2", description = "AOC Day 2 Solver")
parser.add_argument("-f", "--filename", dest = "filename")

args = parser.parse_args()

with open(args.filename, "r") as f:
    lines = f.readlines()

    # Part 1
    score_dict = {"X": 1, "Y": 2, "Z": 3}
    total_score = 0

    # Part 2
    result_dict = {"A": ("Y", "Z"), "B": ("Z", "X"), "C": ("X", "Y")}
    alternate_total_score = 0

    for line in lines:
        opponent, ownself = line.split()
        num_opponent, num_ownself = ord(opponent) - ord("A"), ord(ownself) - ord("X")

        # Draw
        if num_opponent == num_ownself:
            total_score += 3 + score_dict[ownself]
        # Win
        elif (num_ownself - num_opponent) % 3 == 1:
            total_score += 6 + score_dict[ownself]
        # Lose
        else:
            total_score += 0 + score_dict[ownself]

        # Need to lose
        if num_ownself == 0:
            alternate_total_score += 0 + score_dict[result_dict[opponent][1]]
        # Need to draw
        elif num_ownself == 1:
            alternate_total_score += 3 + score_dict[chr(num_opponent + ord("X"))]
        # Need to win
        else:
            alternate_total_score += 6 + score_dict[result_dict[opponent][0]]

    print(f"Total Score: {total_score}, Correct Total Score: {alternate_total_score}")
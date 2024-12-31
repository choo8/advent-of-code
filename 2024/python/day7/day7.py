from itertools import product
import math


def parse(filename: str) -> list[int, list[int]]:
    with open(filename, "r") as f:
        lines = f.readlines()
        calibrations = [l.strip().split(": ") for l in lines]

    return [[int(c[0]), [int(n) for n in c[1].split(" ")]] for c in calibrations]


def is_true(calibration: tuple[int, list[int]], ops: list[str]) -> bool:
    num_ops = len(calibration[1]) - 1
    for ops_perm in product(*[ops for _ in range(num_ops)]):
        acc = calibration[1][0]

        for ops, operand in zip(ops_perm, calibration[1][1:]):
            if ops == "+":
                acc += operand
            elif ops == "*":
                acc *= operand
            elif ops == "||":
                num_digits = int(math.log10(operand)) + 1
                acc = acc * math.pow(10, num_digits) + operand

        if acc == calibration[0]:
            return True

    return False


def part_1():
    for filename in ["example.txt", "input.txt"]:
        calibrations = parse(filename)
        
        total_result = 0
        for c in calibrations:
            if is_true(c, ["+", "*"]):
                total_result += c[0]

        print(f"[Part 1] Total calibration result from {filename}: {total_result}")


def part_2():
    for filename in ["example.txt", "input.txt"]:
        calibrations = parse(filename)

        total_result = 0
        for c in calibrations:
            if is_true(c, ["+", "*", "||"]):
                total_result += c[0]

        print(f"[Part 2] Total calibration result from {filename}: {total_result}")


if __name__ == "__main__":
    part_1()
    part_2()

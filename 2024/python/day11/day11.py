from functools import cache
import math


def parse(filename: str) -> list[int]:
    with open(filename, "r") as f:
        return [int(n) for n in f.read().strip().split()]
    

def transform(s: int) -> list[int]:
    if s == 0:
        return [1]
    elif math.floor(math.log10(s) + 1) % 2 == 0:
        num_digits = math.floor(math.log10(s) + 1)
        smaller = s % math.pow(10, num_digits / 2)
        bigger = (s - smaller) / math.pow(10, num_digits / 2)
        return [int(bigger), int(smaller)]
    else:
        return [int(s * 2024)]


@cache
def num_stones_after_blink(s: int, blinks: int) -> int:
    if blinks == 1:
        return len(transform(s))
    else:
        num_stones = 0
        for _s in transform(s):
            num_stones += num_stones_after_blink(_s, blinks - 1)
        return num_stones


def part_1():
    for filename in ["example.txt", "input.txt"]:
        stones = parse(filename)
    
        num_stones = sum([num_stones_after_blink(s, 25) for s in stones])
    
        print(f"[Part 1] Number of stones in {filename}: {num_stones}")


def part_2():
    for filename in ["example.txt", "input.txt"]:
        stones = parse(filename)
    
        num_stones = sum([num_stones_after_blink(s, 75) for s in stones])
    
        print(f"[Part 2] Number of stones in {filename}: {num_stones}")


if __name__ == "__main__":
    part_1()
    part_2()

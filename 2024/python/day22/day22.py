import sys


def parse(filename: str) -> list[int]:
    with open(filename, "r") as f:
        return [int(line.strip()) for line in f.readlines()]


def generate_next_secret(secret: int) -> int:
    secret = ((secret * 64) ^ secret) % 16777216
    secret = (int(secret / 32) ^ secret) % 16777216
    secret = ((2048 * secret) ^ secret) % 16777216
    return secret


def part_1():
    for filename in ["example.txt", "input.txt"]:
        nums = parse(filename)
        sum_secret = 0
        for n in nums:
            secret = n
            for _ in range(2000):
                secret = generate_next_secret(secret)
            sum_secret += secret
        print(f"[Part 1] Sum of 2000th secret number of each buyer in {filename}: {sum_secret}")


def generate_secret_numbers(secret: int) -> list[int]:
    numbers = [secret % 10]
    for _ in range(2000):
        secret = generate_next_secret(secret)
        numbers.append(secret % 10)
    return numbers


def generate_changes(seq: list[int]) -> tuple[list[int]]:
    changes = []
    for left, right in zip(seq, seq[1:]):
        changes.append(right - left)
    return changes


def generate_patterns(num_seqs: list[list[int]], changes: list[list[int]]) -> tuple[list[list[int]], dict[tuple[int, int, int, int, int], int]]:
    patterns, pattern_cache = set(), {}
    for change_idx, change in enumerate(changes):
        for i in range(len(change) - 4 + 1):
            patterns.add(tuple(change[i:i + 4]))
            if tuple([change_idx] + change[i:i + 4]) not in pattern_cache:
                pattern_cache[tuple([change_idx] + change[i:i + 4])] = num_seqs[change_idx][i + 4]
    return [list(pattern) for pattern in patterns], pattern_cache


def part_2():
    for filename in ["example.txt", "input.txt"]:
        nums = parse(filename)
        num_seqs = [generate_secret_numbers(n) for n in nums]
        changes = [generate_changes(seq) for seq in num_seqs]
        patterns, pattern_cache = generate_patterns(num_seqs, changes)
        num_bananas = 0

        for pattern_idx, pattern in enumerate(patterns):
            pattern_banana = 0
            for change_idx, _ in enumerate(changes):
                if tuple([change_idx] + pattern) in pattern_cache:
                    pattern_banana += pattern_cache[tuple([change_idx] + pattern)]
            num_bananas = max(num_bananas, pattern_banana)

        print(f"[Part 2] Most bananas in {filename}: {num_bananas}")


if __name__ == "__main__":
    part_1()
    part_2()

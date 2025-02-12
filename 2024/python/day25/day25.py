def parse(filename: str) -> tuple[list[list[int]], list[list[int]]]:
    with open(filename, "r") as f:
        lines = f.readlines()
        idx, locks, keys = 0, [], []
        while idx < len(lines):
            if lines[idx].strip() == "#####":
                cur_lock = [0 for _ in range(5)]
                for cur_idx in range(idx + 1, idx + 7):
                    for pin in range(5):
                        if lines[cur_idx][pin] == "#":
                            cur_lock[pin] += 1
                locks.append(cur_lock)
            else:
                cur_key = [0 for _ in range(5)]
                for cur_idx in range(idx + 5, idx - 1, -1):
                    for pin in range(5):
                        if lines[cur_idx][pin] == "#":
                            cur_key[pin] += 1
                keys.append(cur_key)
            idx += 8
        return locks, keys


def get_num_fit(locks: list[list[int]], keys: list[list[int]]) -> int:
    num_fit = 0
    for lock in locks:
        for key in keys:
            if all(n <= 5 for n in [l + k for l, k in zip(lock, key)]):
                num_fit += 1
    return num_fit


def part_1():
    for filename in ["example.txt", "input.txt"]:
        locks, keys = parse(filename)
        num_fit = get_num_fit(locks, keys)
        print(f"[Part 1] Number of unique lock key pairs that fit in {filename}: {num_fit}")


if __name__ == "__main__":
    part_1()

from collections.abc import Iterable
import re
from scipy.optimize import linprog


def parse(filename: str) -> Iterable[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]:
    with open(filename, "r") as f:
        content = f.read()

        a = [(int(ax), int(ay)) for (ax, ay) in re.findall(r"Button A: X\+(\d+), Y\+(\d+)", content)]
        b = [(int(bx), int(by)) for (bx, by) in re.findall(r"Button B: X\+(\d+), Y\+(\d+)", content)]
        prize = [(int(prize_x), int(prize_y)) for (prize_x, prize_y) in re.findall(r"Prize: X=(\d+), Y=(\d+)", content)]
        
        return zip(a, b, prize)


def get_num_tokens(machine: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]) -> int:
    c = [3, 1]
    A = [[machine[0][0], machine[1][0]], [machine[0][1], machine[1][1]]]
    b = list(machine[2])
    a_bounds = (0, None)
    b_bounds = (0, None)
    res = linprog(c, A_eq=A, b_eq=b, bounds=[a_bounds, b_bounds], integrality=3, options={"presolve": False})

    return int(res.fun) if res.success else 0


def part_1():
    for filename in ["example.txt", "input.txt"]:
        machines = parse(filename)
        
        total_tokens = 0
        for m in machines:
            total_tokens += get_num_tokens(m)
        
        print(f"[Part 1] Fewest number of tokens required in {filename}: {total_tokens}")


def fix_error(machines: Iterable[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]) -> list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]:
    return [((ax, ay), (bx, by), (10000000000000 + prize_x, 10000000000000 + prize_y)) for ((ax, ay), (bx, by), (prize_x, prize_y)) in machines]


def part_2():
    for filename in ["example.txt", "input.txt"]:
        machines = parse(filename)

        total_tokens = 0
        for m in fix_error(machines):
            total_tokens += get_num_tokens(m)

        print(f"[Part 2] Fewest number of tokens required in {filename}: {total_tokens}")


if __name__ == "__main__":
    part_1()
    part_2()

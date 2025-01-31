import re


def parse(filename: str) -> tuple[int, int, int, list[int]]:
    with open(filename, "r") as f:
        content = f.read()

        reg_a = re.findall(r"Register A: (.*)", content)[0]
        reg_b = re.findall(r"Register B: (.*)", content)[0]
        reg_c = re.findall(r"Register C: (.*)", content)[0]
        prog = re.findall(r"Program: (.*)", content)[0]

    return int(reg_a), int(reg_b), int(reg_c), [int(x) for x in prog.split(",")]


def perform_inst(prog: list[int], ip: int, reg_a: int, reg_b: int, reg_c: int, outs: list[int]) -> tuple[int, int, int, int, list[int]]:
    operand_dict = {
        0: 0,
        1: 1,
        2: 2,
        3: 3,
        4: reg_a,
        5: reg_b,
        6: reg_c
    }
    inst, operand = prog[ip], prog[ip + 1]
    ip += 2
    if inst == 0:
        reg_a = int(reg_a / pow(2, operand_dict[operand]))
    elif inst == 1:
        reg_b = operand ^ reg_b
    elif inst == 2:
        reg_b = operand_dict[operand] % 8 
    elif inst == 3:
        if reg_a != 0:
            ip = operand
    elif inst == 4:
        reg_b = reg_b ^ reg_c
    elif inst == 5:
        outs.append(operand_dict[operand] % 8)
    elif inst == 6:
        reg_b = int(reg_a / pow(2, operand_dict[operand]))
    elif inst == 7:
        reg_c = int(reg_a / pow(2, operand_dict[operand]))

    return ip, reg_a, reg_b, reg_c, outs


def exec_prog(prog: list[int], reg_a: int, reg_b: int, reg_c: int) -> list[int]:
    outs, ip = [], 0
    while ip < len(prog):
        ip, reg_a, reg_b, reg_c, outs = perform_inst(prog, ip, reg_a, reg_b, reg_c, outs)
    return outs


def part_1():
    for filename in ["example.txt", "input.txt"]:
        reg_a, reg_b, reg_c, prog = parse(filename)
        outs = ",".join([str(x) for x in exec_prog(prog, reg_a, reg_b, reg_c)])
        print(f"[Part 1] Final output of {filename}: {outs}")


def part_2():
    for filename in ["example.txt", "input.txt"]:
        reg_a, reg_b, reg_c, prog = parse(filename)
        reg_a = 1
        while True:
            outs = exec_prog(prog, reg_a, reg_b, reg_c)

            if outs == prog:
                break
            elif len(outs) < len(prog):
                reg_a *= 2
            else:
                for i in range(len(prog) - 1, -1, -1):
                    if outs[i] != prog[i]:
                        reg_a += int(pow(8, i))
                        break

        print(f"[Part 2] Lowest initial value of A for {filename}: {reg_a}")


if __name__ == "__main__":
    part_1()
    part_2()

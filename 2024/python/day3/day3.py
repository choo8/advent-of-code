import re


def parse(filename: str) -> str:
    with open(filename, "r") as f:
        lines = f.readlines()

    return "".join(lines)


def process_mul(instruction: str) -> int:
    x, y = re.findall(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)", instruction)[0]
    return int(x) * int(y)


def part_1():
    for filename in ["example.txt", "input.txt"]:
        memory = parse(filename)

        instructions = re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)", memory)

        result = sum([process_mul(i) for i in instructions])
        
        print(f"[Part 1] Results of multiplications in {filename}: {result}")


def process_instructions(instructions: list[str]) -> list[str]:
    enabled, processed = True, []

    for i in instructions:
        if i == "don't()":
            enabled = False
        elif i == "do()":
            enabled = True
        else:
            if enabled:
                processed.append(i)

    return processed


def part_2():
    for filename in ["example.txt", "input.txt"]:
        memory = parse(filename)

        instructions = re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don't\(\)", memory)

        result = sum([process_mul(i) for i in process_instructions(instructions)])

        print(f"[Part 2] Results of multiplications in {filename}: {result}")


if __name__ == "__main__":
    part_1()
    part_2()

def parse(filename: str) -> list[list[int]]:
    with open(filename, "r") as f:
        reports = [[int(l) for l in line.split()] for line in f.readlines()]

    return reports


def is_safe_increase(report: list[int]) -> bool:
    if len(report) <= 1:
        return True
    else:
        return report[0] + 1 <= report[1] and report[0] + 3 >= report[1] and is_safe_increase(report[1:])


def is_safe_decrease(report: list[int]) -> bool:
    if len(report) <= 1:
        return True
    else:
        return report[0] - 1 >= report[1] and report[0] - 3 <= report[1] and is_safe_decrease(report[1:])


def is_report_safe(report: list[int]) -> bool:
    return is_safe_increase(report) or is_safe_decrease(report)


def part_1():
    for filename in ["example.txt", "input.txt"]:
        reports = parse(filename)

        safe_reports = sum(map(is_report_safe, reports))

        print(f"[Part 1] Number of safe reports in {filename}: {safe_reports}")


def is_dampened_report_safe(report: list[int]) -> bool:
    if not is_report_safe(report):
        return any(map(is_report_safe, [report[:i] + report[i+1:] for i in range(len(report))]))
    else:
        return True


def part_2():
    for filename in ["example.txt", "input.txt"]:
        reports = parse(filename)

        safe_reports = sum(map(is_dampened_report_safe, reports))

        print(f"[Part 2] Number of safe reports after Problem Dampener in {filename}: {safe_reports}")


if __name__ == "__main__":
    part_1()
    part_2()

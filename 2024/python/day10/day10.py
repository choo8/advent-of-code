def parse(filename: str) -> list[list[int]]:
    with open(filename, "r") as f:
        rows = f.readlines()
        return [[int(n) for n in list(r.strip())] for r in rows]


def get_trailheads(grid: list[list[int]]) -> list[tuple[int, int]]:
    trailheads = []
    for r, row in enumerate(grid):
        for c, height in enumerate(row):
            if height == 0:
                trailheads.append((r, c))
    return trailheads


def is_in_grid(grid: list[list[int]], r: int, c: int) -> bool:
    return r >= 0 and r < len(grid) and c >= 0 and c < len(grid[0])


def get_score(grid: list[list[int]], r: int, c: int) -> int:
    end_set, stack, dir = set(), [(r, c)], [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while len(stack):
        r, c = stack.pop()

        if grid[r][c] == 9:
            end_set.add((r, c))

        for dr, dc in dir:
            new_r, new_c = r + dr, c + dc

            if is_in_grid(grid, new_r, new_c) and grid[r][c] + 1 == grid[new_r][new_c]:
                stack.append((new_r, new_c))

    return len(end_set)


def part_1():
    for filename in ["example.txt", "input.txt"]:
        grid = parse(filename)
        trailheads = get_trailheads(grid)

        sum_scores = 0
        for r, c in trailheads:
            sum_scores += get_score(grid, r, c)

        print(f"[Part 1] Sum of scores of all trailheads in {filename}: {sum_scores}")


def get_rating(grid: list[list[int]], r: int, c: int) -> int:
    rating, stack, dir = 0, [(r, c)], [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while len(stack):
        r, c = stack.pop()

        if grid[r][c] == 9:
            rating += 1

        for dr, dc in dir:
            new_r, new_c = r + dr, c + dc

            if is_in_grid(grid, new_r, new_c) and grid[r][c] + 1 == grid[new_r][new_c]:
                stack.append((new_r, new_c))

    return rating


def part_2():
    for filename in ["example.txt", "input.txt"]:
        grid = parse(filename)
        trailheads = get_trailheads(grid)

        sum_ratings = 0
        for r, c in trailheads:
            sum_ratings += get_rating(grid, r, c)

        print(f"[Part 2] Sum of ratings of all trailheads in {filename}: {sum_ratings}")


if __name__ == "__main__":
    part_1()
    part_2()

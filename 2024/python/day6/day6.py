def parse(filename: str) -> list[list[str]]:
    with open(filename, "r") as f:
        return [list(l.strip()) for l in f.readlines()]


def get_cur_pos(map: list[list[str]]) -> tuple[int, int, int]:
    dir = {"^": 0, ">": 1, "v": 2, "<": 3}
    for r_idx, r in enumerate(map):
        for c_idx, cell in enumerate(r):
            if cell not in [".", "#"]:
                return (r_idx, c_idx, dir[cell])


def is_in_map(map: list[list[str]], r: int, c: int) -> bool:
    return r >= 0 and r < len(map) and c >= 0 and c < len(map[0])


def part_1():
    for filename in ["example.txt", "input.txt"]:
        map = parse(filename)
        r, c, dir = get_cur_pos(map)

        num_steps, visited = 1, set([(r, c)])
        delta = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
        while True:
            new_r, new_c = r + delta[dir][0], c + delta[dir][1]

            if not is_in_map(map, new_r, new_c):
                break
        
            if map[new_r][new_c] in [".", "^", ">", "v", "<"]:
                if (new_r, new_c) not in visited:
                    num_steps += 1
                    visited.add((new_r, new_c))
                r, c = new_r, new_c
            elif map[new_r][new_c] == "#":
                dir = (dir + 1) % 4

        print(f"[Part 1] Number of distinct positions visited in {filename}: {num_steps}")


def is_loop(map: list[list[str]], r: int, c: int, dir: int) -> bool:
    visited_corners = []

    delta = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
    while True:
        new_r, new_c = r + delta[dir][0], c + delta[dir][1]

        if not is_in_map(map, new_r, new_c):
            return False

        if map[new_r][new_c] in ["#", "O"]:
            if (r, c) in visited_corners and visited_corners[-1] != (r, c):
                return True
            visited_corners.append((r, c))
            dir = (dir + 1) % 4
        else:
            r, c = new_r, new_c


def part_2():
    for filename in ["example.txt", "input.txt"]:
        map = parse(filename)
        r, c, dir = get_cur_pos(map)

        num_pos = 0
        for obs_r, _r in enumerate(map):
            for obs_c, cell in enumerate(_r):
                if cell in ["#", "^", ">", "v", "<"]:
                    continue

                map[obs_r][obs_c] = "O"
                if is_loop(map, r, c, dir):
                    num_pos += 1
                map[obs_r][obs_c] = cell

        print(f"[Part 2] Number of obstruction positions in {filename}: {num_pos}")


if __name__ == "__main__":
    part_1()
    part_2()

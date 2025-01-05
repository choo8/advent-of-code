from bisect import bisect_left, bisect_right


def parse(filename: str) -> list[int]:
    with open(filename, "r") as f:
        disk_map = f.read()
        return [int(n) for n in list(disk_map.strip())]


def get_segment_checksum(left: int, n: int, file_id: int) -> int:
    return int(file_id * n * (left + left + n - 1) / 2)


def get_checksum(disk_map: list[int]) -> int:
    blocks, spaces = [disk_map[i] for i in range(0, len(disk_map), 2)], [disk_map[i] for i in range(1, len(disk_map), 2)]
    num_blocks = sum(blocks)

    checksum = 0
    left, is_file = 0, True
    left_block_idx, spaces_idx = 0, 0
    right_block_idx, right_blocks_left = len(blocks) - 1, blocks[-1]
    while left < num_blocks:
        if is_file:
            checksum += get_segment_checksum(left, min(blocks[left_block_idx], num_blocks - left), left_block_idx)
            left += min(blocks[left_block_idx], num_blocks - left)
            left_block_idx += 1
        else:
            to_fill = spaces[spaces_idx]
            while left < num_blocks and to_fill > 0:
                if right_blocks_left > to_fill:
                    checksum += get_segment_checksum(left, to_fill, right_block_idx)
                    right_blocks_left -= to_fill
                    left += to_fill
                    to_fill = 0
                else:
                    checksum += get_segment_checksum(left, right_blocks_left, right_block_idx)
                    to_fill -= right_blocks_left
                    left += right_blocks_left
                    right_block_idx -= 1
                    right_blocks_left = blocks[right_block_idx]

            spaces_idx += 1
        
        is_file = not is_file

    return checksum


def part_1():
    for filename in ["example.txt", "input.txt"]:
        disk_map = parse(filename)

        print(f"[Part 1] Filesystem checksum in {filename}: {get_checksum(disk_map)}")


def get_offsets(disk_map: list[int]) -> tuple[list[int], list[int]]:
    prefix_num_block = [0 for _ in range(len(disk_map))]

    for idx in range(1, len(prefix_num_block)):
        prefix_num_block[idx] = prefix_num_block[idx - 1] + disk_map[idx - 1]

    return [prefix_num_block[i] for i in range(0, len(disk_map), 2)], [prefix_num_block[i] for i in range(1, len(disk_map), 2)]


def get_dicts(disk_map: list[int]) -> tuple[dict[int, tuple[int, int]], dict[int, int]]:
    file_offsets, space_offsets = get_offsets(disk_map)
    files, spaces = [disk_map[i] for i in range(0, len(disk_map), 2)], [disk_map[i] for i in range(1, len(disk_map), 2)]

    files_dict = {file_offsets[file_id]: (file_id, num_files) for file_id, num_files in enumerate(files)}
    spaces_dict = {space_offsets[i]: num_spaces for i, num_spaces in enumerate(spaces) if num_spaces > 0}

    return files_dict, spaces_dict


def insert_space(spaces_dict: dict[int, int], file_offset: int, num_files: int) -> dict[int, int]:
    merged_prev, merged_next = False, False

    spaces_offsets = list(sorted(spaces_dict.keys()))
    i = bisect_left(spaces_offsets, file_offset)
    if i:
        prev_offset = spaces_offsets[i - 1]
        # Block of space right before block of files
        if prev_offset + spaces_dict[prev_offset] == file_offset:
            spaces_dict[prev_offset] += num_files
            merged_prev = True

    i = bisect_right(spaces_offsets, file_offset)
    if i != len(spaces_offsets):
        next_offset = spaces_offsets[i]
        # Block of space right after block of files
        if file_offset + num_files == next_offset:
            if merged_prev:
                spaces_dict[prev_offset] += spaces_dict[next_offset]
            else:
                spaces_dict[file_offset] = num_files + spaces_dict[next_offset]
            del spaces_dict[next_offset]
            merged_next = True

    if not merged_next:
        spaces_dict[file_offset] = num_files
    
    return spaces_dict


def get_new_checksum(disk_map: list[int]) -> int:
    files_dict, spaces_dict = get_dicts(disk_map)

    checksum = 0
    for file_offset in sorted(files_dict.keys(), reverse=True):
        file_id, num_files = files_dict[file_offset]
        shifted = False

        for space_offset in sorted(spaces_dict.keys()):
            num_spaces = spaces_dict[space_offset]
            if space_offset < file_offset and num_spaces >= num_files:
                checksum += get_segment_checksum(space_offset, num_files, file_id)
                
                # Modify space that was used
                del spaces_dict[space_offset]
                if num_files < num_spaces:
                    spaces_dict[space_offset + num_files] = num_spaces - num_files

                # Create space in position of file block
                spaces_dict = insert_space(spaces_dict, file_offset, num_files)

                shifted = True
                break

        if not shifted:
            checksum += get_segment_checksum(file_offset, num_files, file_id)

    return checksum
        

def part_2():
    for filename in ["example.txt", "input.txt"]:
        disk_map = parse(filename)

        print(f"[Part 2] New filesystem checksum in {filename}: {get_new_checksum(disk_map)}")


if __name__ == "__main__":
    part_1()
    part_2()

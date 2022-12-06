def group(data: str, group_size: int) -> list[str]:
    return [
        data[start:end]
        for start in range(len(data))
        if (end := start + group_size) <= len(data)
    ]


def part_1(data: str) -> int:
    group_size = 4
    groups = group(data, group_size)
    for i, g in enumerate(groups):
        if len(set(g)) == len(g):
            break
    return i + group_size


def part_2(data: str) -> int:
    group_size = 14
    groups = group(data, group_size)
    for i, g in enumerate(groups):
        if len(set(g)) == len(g):
            break
    return i + group_size


if __name__ == "__main__":
    # data
    with open("data/06.txt") as f:
        data = f.read()
    # part 1
    assert part_1("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert part_1("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert part_1("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
    assert part_1("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11
    print("Part 1:", part_1(data))

    # part 2
    assert part_2("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 19
    assert part_2("bvwbjplbgvbhsrlpgdmjqwftvncz") == 23
    assert part_2("nppdvjthqldpwncqszvftbrmjlhg") == 23
    assert part_2("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 29
    assert part_2("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 26
    print("Part 2:", part_2(data))

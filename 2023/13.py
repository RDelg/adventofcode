EXAMPLE = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


def parse(data: str) -> list[list[str]]:
    return [x.splitlines() for x in data.split("\n\n")]


def rotate(map: list[str]) -> list[str]:
    return ["".join(x) for x in zip(*map[::-1])]


def calculate_diferece(a: list[str], b: list[str]) -> int:
    return sum(
        [sum([1 for xx, yy in zip(x, y) if xx != yy]) for x, y in zip(a, b) if x != y]
    )


def find_reflection_point(map: list[str], smudged: int = 0) -> int:
    for i in range(len(map) - 1):
        if i < (len(map) // 2):
            start = 0
            end = (i + 1) * 2
        else:
            start = 2 * (i - len(map) // 2) + 1
            end = len(map)
        if calculate_diferece(map[start : i + 1], map[i + 1 : end][::-1]) == smudged:
            return i + 1

    return 0


def part_1(data: str) -> int:
    maps = parse(data)
    maps_rotated = [rotate(x) for x in maps]
    points_horizontal = [find_reflection_point(x) for x in maps]
    points_vertical = [find_reflection_point(x) for x in maps_rotated]
    s_hor = sum(points_horizontal) * 100
    s_ver = sum(points_vertical)
    return s_hor + s_ver


def part_2(data: str) -> int:
    maps = parse(data)
    maps_rotated = [rotate(x) for x in maps]
    points_horizontal = [find_reflection_point(x, 1) for x in maps]
    points_vertical = [find_reflection_point(x, 1) for x in maps_rotated]
    s = [x * 100 if x > 0 else y for x, y in zip(points_horizontal, points_vertical)]
    return sum(s)


if __name__ == "__main__":
    with open("data/13.txt") as f:
        data = f.read()

    assert part_1(EXAMPLE) == 405
    print(f"{part_1(data) = }")
    assert part_2(EXAMPLE) == 400
    print(f"{part_2(data) = }")

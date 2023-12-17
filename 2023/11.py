import itertools
from collections import defaultdict
from typing import NamedTuple

EXAMPLE = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


class Point(NamedTuple):
    y: int
    x: int


def parse(data: str) -> tuple[list[Point], list[int], list[int]]:
    grid = [list(line) for line in data.splitlines()]
    galaxies = []
    empty_spaces_y = []
    empty_spaces_x_candidates = []
    for i, line in enumerate(grid):
        empty_spaces_x_candidates.append([j for j, c in enumerate(line) if c == "."])
        if all(c == "." for c in line):
            empty_spaces_y.append(i)
        for j, c in enumerate(line):
            if c == "#":
                galaxies.append(Point(i, j))

    group_dict = defaultdict(lambda: 0)
    for spaces in empty_spaces_x_candidates:
        for x in spaces:
            group_dict[x] += 1

    empty_spaces_x = [k for k, v in group_dict.items() if v == len(grid)]

    return galaxies, empty_spaces_y, empty_spaces_x


def manhattan_distance(p1: Point, p2: Point) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def expand(
    galaxies: list[Point],
    empty_spaces_y: list[int],
    empty_spaces_x: list[int],
    n: int = 1,
) -> list[Point]:
    expanded_galaxies = []
    for g in galaxies:
        yy = sum([n for x in empty_spaces_y if g.y > x])
        xx = sum([n for x in empty_spaces_x if g.x > x])
        expanded_galaxies.append(Point(g.y + yy, g.x + xx))
    return expanded_galaxies


def part_1(data: str) -> int:
    galaxies, empty_spaces_y, empty_spaces_x = parse(data)
    expanded_galaxies = expand(galaxies, empty_spaces_y, empty_spaces_x)
    distances = [
        manhattan_distance(*c) for c in itertools.combinations(expanded_galaxies, 2)
    ]
    return sum(distances)


def part_2(data: str, n: int) -> int:
    galaxies, empty_spaces_y, empty_spaces_x = parse(data)
    expanded_galaxies = expand(galaxies, empty_spaces_y, empty_spaces_x, n)
    distances = [
        manhattan_distance(*c) for c in itertools.combinations(expanded_galaxies, 2)
    ]
    return sum(distances)


if __name__ == "__main__":
    with open("data/11.txt") as f:
        data = f.read()

    assert (part_1(EXAMPLE)) == 374
    print(f"{part_1(data) = }")

    assert (part_2(EXAMPLE, n=10 - 1)) == 1030
    assert (part_2(EXAMPLE, n=100 - 1)) == 8410
    print(f"{part_2(data, 1000000-1) = }")

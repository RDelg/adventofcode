import re

EXAMPLE_1 = """\
.....
.S-7.
.|.|.
.L-J.
....."""

EXAMPLE_2 = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

EXAMPLE_3 = """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

EXAMPLE_4 = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

EXAMPLE_5 = """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

MOVES = {
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
    "|": [(1, 0), (-1, 0)],
    "-": [(0, 1), (0, -1)],
}


def find_start(grid: list[list[str]]) -> tuple[int, int]:
    for i, line in enumerate(grid):
        for j, c in enumerate(line):
            if c == "S":
                return i, j
    return -1, -1


def get_start_type(grid: list[list[str]], start: tuple[int, int]) -> str:
    n, m = len(grid), len(grid[0])
    for k, v in MOVES.items():
        connections = [
            (start[0] + i, start[1] + j)
            for i, j in v
            if 0 <= start[0] + i < n and 0 <= start[1] + j < m
        ]
        connections_type = [grid[i][j] for i, j in connections]
        if any(x == "." for x in connections_type) or len(connections_type) != 2:
            continue
        if (
            len(
                [
                    1
                    for ct, con in zip(connections_type, connections)
                    if grid[con[0] + MOVES[ct][0][0]][con[1] + MOVES[ct][0][1]] == "S"
                    or grid[con[0] + MOVES[ct][1][0]][con[1] + MOVES[ct][1][1]] == "S"
                ]
            )
            == 2
        ):
            return k
    return ""


def generate_path(
    grid: list[list[str]], start: tuple[int, int]
) -> list[tuple[int, int]]:
    start_type = get_start_type(grid, start)
    last_pos = start
    # choose one side
    current_pos = (
        start[0] + MOVES[start_type][0][0],
        start[1] + MOVES[start_type][0][1],
    )

    path = [start, current_pos]
    while grid[current_pos[0]][current_pos[1]] != "S":
        posible_moves = [
            (current_pos[0] + i, current_pos[1] + j)
            for i, j in MOVES[grid[current_pos[0]][current_pos[1]]]
        ]
        posible_moves = [(i, j) for i, j in posible_moves if (i, j) != last_pos]
        last_pos = current_pos
        current_pos = posible_moves[0]
        path.append(current_pos)
    return path


def part_1(data: str) -> int:
    grid = [list(line) for line in data.splitlines()]
    start = find_start(grid)

    path = generate_path(grid, start)
    n = len(path)
    return n // 2


# https://en.wikipedia.org/wiki/Shoelace_formula
def interior_area(points: list[tuple[int, int]]) -> float:
    padded_points = [*points, points[0]]
    return (
        sum(
            row1 * col2 - row2 * col1
            for (row1, col1), (row2, col2) in zip(padded_points, padded_points[1:])
        )
        / 2
    )


def part_2(data: str) -> int:
    grid = [list(line) for line in data.splitlines()]
    start = find_start(grid)
    path = generate_path(grid, start)
    area = interior_area(path)
    # https://en.wikipedia.org/wiki/Pick's_theorem
    num_interior_points = int(abs(area) - 0.5 * len(path) + 1)
    return num_interior_points + 1


if __name__ == "__main__":
    with open("data/10.txt") as f:
        data = f.read()
    assert (part_1(EXAMPLE_1)) == 4
    assert (part_1(EXAMPLE_2)) == 8
    print(f"{part_1(data) = }")

    assert (part_2(EXAMPLE_3)) == 4
    assert (part_2(EXAMPLE_4)) == 8
    assert (part_2(EXAMPLE_5)) == 10
    print(f"{part_2(data) = }")

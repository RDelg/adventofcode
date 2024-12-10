from typing import Generator

EXAMPLE = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""


def parse(data: str) -> list[list[str]]:
    return [list(x) for x in data.splitlines()]


def paths_from_point(x: int, y: int, n: int, m: int, length: int) -> Generator[list[tuple[int, int]], None, None]:
    # to the right
    yield [(x, y + i) for i in range(min(m - y, length))]
    # to the left
    yield [(x, y - i) for i in range(min(y + 1, length))]
    # to the bottom
    yield [(x + i, y) for i in range(min(n - x, length))]
    # to the top
    yield [(x - i, y) for i in range(min(x + 1, length))]
    # to the bottom right
    yield [(x + i, y + i) for i in range(min(n - x, m - y, length))]
    # to the bottom left
    yield [(x + i, y - i) for i in range(min(n - x, y + 1, length))]
    # to the top right
    yield [(x - i, y + i) for i in range(min(x + 1, m - y, length))]
    # to the top left
    yield [(x - i, y - i) for i in range(min(x + 1, y + 1, length))]


def crosses_from_point(x: int, y: int, n: int, m: int) -> list[list[tuple[int, int]]]:
    if x == 0 or x == n - 1 or y == 0 or y == m - 1:
        return []
    return [
        [(x - 1, y - 1), (x, y), (x + 1, y + 1)],
        [(x - 1, y + 1), (x, y), (x + 1, y - 1)],
    ]


def part_1(raw: str) -> int:
    data = parse(raw)
    find_xs = lambda x: [(i, j) for i, row in enumerate(x) for j, col in enumerate(row) if col == "X"]
    xs = find_xs(data)
    n, m = len(data), len(data[0])
    val = 0
    for x, y in xs:
        for path in paths_from_point(x, y, n, m, 4):
            word = "".join(data[i][j] for i, j in path)
            if len(word) == 4:
                if word == "XMAS" or word == "SAMX":
                    val += 1
    return val


def part_2(raw: str) -> int:
    data = parse(raw)
    find_as = lambda x: [(i, j) for i, row in enumerate(x) for j, col in enumerate(row) if col == "A"]
    as_ = find_as(data)
    n, m = len(data), len(data[0])
    val = 0
    for x, y in as_:
        n_mas = 0
        for path in crosses_from_point(x, y, n, m):
            try:
                word = "".join(data[i][j] for i, j in path)
                if word == "MAS" or word == "SAM":
                    n_mas += 1
            except IndexError:
                pass
        if n_mas == 2:
            val += 1

    return val


if __name__ == "__main__":
    # data
    with open("data/04.txt") as f:
        data = f.read()

    # part 1
    assert part_1(EXAMPLE) == 18
    print(f"{part_1(data)= }")

    # part 2
    assert part_2(EXAMPLE) == 9
    print(f"{part_2(data)= }")

from collections import Counter
from typing import Generator

EXAMPLE = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""


def parse(data: str) -> list[list[int]]:
    return [list(map(int, x.split())) for x in data.splitlines()]


def part_1(data: str) -> int:
    parsed = parse(data)
    i = 0
    is_increasing = lambda x: all(x[i] <= x[i + 1] for i in range(len(x) - 1))
    is_decreasing = lambda x: all(x[i] >= x[i + 1] for i in range(len(x) - 1))
    consecutive_diff = lambda x: [abs(x[i] - x[i + 1]) for i in range(len(x) - 1)]
    for row in parsed:
        if is_increasing(row) or is_decreasing(row):
            if 1 <= min(consecutive_diff(row)) and max(consecutive_diff(row)) <= 3:
                i += 1
    return i


def row_generator(row: list[int]) -> Generator[list[int], None, None]:
    yield row
    for i in range(len(row)):
        yield row[:i] + row[i + 1 :]


def part_2(data: str) -> int:
    parsed = parse(data)
    ok_level = lambda x, y, sign: 0 < (x - y) * sign <= 3
    diffs_sign = lambda x: [(-1) ** int(x[i] - x[i + 1] < 0) for i in range(len(x) - 1)]
    n = 0
    for row in parsed:
        sign = Counter(diffs_sign(row)).most_common()[0][0]
        found = False
        for r in row_generator(row):
            if all(ok_level(r[i], r[i + 1], sign) for i in range(len(r) - 1)):
                found = True
                break
        if found:
            n += 1

    return n


if __name__ == "__main__":
    with open("data/02.txt") as f:
        data = f.read()

    # part 1
    assert part_1(EXAMPLE) == 2
    print(f"{part_1(data)=}")

    # part 2
    assert part_2(EXAMPLE) == 4
    print(f"{part_2(data)=}")

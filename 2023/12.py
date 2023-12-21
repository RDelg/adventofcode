import re
from typing import NamedTuple
from functools import lru_cache

EXAMPLE = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


class Row(NamedTuple):
    pattern: str
    arrangement: list[int]


def parse(data: str) -> list[Row]:
    lines = data.splitlines()
    return [
        Row((y := line.split())[0], [int(x) for x in y[1].split(",")]) for line in lines
    ]


def calculate_arragement(pattern: str) -> list[int]:
    return [len(x) for x in re.findall(r"#+", pattern)]


@lru_cache(maxsize=128)
def expand_pattern(pattern: str) -> list[str]:
    if "?" not in pattern:
        return [pattern]
    return expand_pattern(pattern.replace("?", "#", 1)) + expand_pattern(
        pattern.replace("?", ".", 1)
    )


def calculate_variants(row: Row) -> int:
    n = 0
    for pattern in expand_pattern(row.pattern):
        new_arrangement = calculate_arragement(pattern)
        if new_arrangement == row.arrangement:
            n += 1
    return n


def part_1(data: str) -> int:
    rows = parse(data)
    posibilities = [calculate_variants(row) for row in rows]
    return sum(posibilities)


def part_2(data: str) -> int:
    rows = parse(data)
    rows = [Row("?".join([x.pattern] * 5), x.arrangement * 5) for x in rows]
    print(calculate_variants(rows[1]))
    # posibilities = [calculate_variants(row) for row in rows]
    # return sum(posibilities)


if __name__ == "__main__":
    with open("data/12.txt") as file:
        data = file.read()
    assert part_1(EXAMPLE) == 21
    print(f"{part_1(data) = }")

    # assert part_2(EXAMPLE) == 525152
    # print(f"{part_2(EXAMPLE) = }")  #

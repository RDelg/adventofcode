import re
from typing import NamedTuple

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


def expand(row: Row) -> list[Row]:
    patterns = []
    positions_to_change = [i for i, c in enumerate(row.pattern) if c == "?"]
    for i in range(2 ** len(positions_to_change)):
        new_pattern = row.pattern
        for j, position in enumerate(positions_to_change):
            new_pattern = (
                new_pattern[:position]
                + ("#" if i & 2**j else ".")
                + new_pattern[position + 1 :]
            )
        new_arrangement = calculate_arragement(new_pattern)
        if new_arrangement == row.arrangement:
            patterns.append(Row(new_pattern, row.arrangement))
    return patterns


def part_1(data: str) -> int:
    rows = parse(data)
    posibilities = [expand(row) for row in rows]
    return sum(len(x) for x in posibilities)


if __name__ == "__main__":
    with open("data/12.txt") as file:
        data = file.read()
    assert part_1(EXAMPLE) == 21
    print(f"{part_1(data) = }")

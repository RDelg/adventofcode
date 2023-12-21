import re
from typing import NamedTuple
from functools import cache

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
        Row((y := line.split())[0], tuple(int(x) for x in y[1].split(",")))
        for line in lines
    ]


def calculate_arragement(pattern: str) -> list[int]:
    return [len(x) for x in re.findall(r"#+", pattern)]


@cache
def n_solutions(
    pattern: str, arrangement: tuple[int], current_group_size: int = 0
) -> list[str]:
    if not pattern:
        return not arrangement and not current_group_size
    n = 0
    possible = [".", "#"] if pattern[0] == "?" else pattern[0]
    for c in possible:
        if c == "#":
            n += n_solutions(pattern[1:], arrangement, current_group_size + 1)
        else:
            if current_group_size:
                if arrangement and arrangement[0] == current_group_size:
                    n += n_solutions(pattern[1:], arrangement[1:])
            else:
                n += n_solutions(pattern[1:], arrangement)
    return n


def part_1(data: str) -> int:
    rows = parse(data)
    posibilities = [n_solutions(row.pattern + ".", row.arrangement) for row in rows]
    return sum(posibilities)


def part_2(data: str) -> int:
    rows = parse(data)
    rows = [Row("?".join([x.pattern] * 5), x.arrangement * 5) for x in rows]
    posibilities = [n_solutions(row.pattern + ".", row.arrangement) for row in rows]
    return sum(posibilities)


if __name__ == "__main__":
    with open("data/12.txt") as file:
        data = file.read()
    assert part_1(EXAMPLE) == 21
    print(f"{part_1(data) = }")

    assert part_2(EXAMPLE) == 525152
    print(f"{part_2(data) = }")

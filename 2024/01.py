from collections import Counter

EXAMPLE = """\
3   4
4   3
2   5
1   3
3   9
3   3"""


def parse(data: str) -> tuple[list[int], list[int]]:
    parsed: list[list[int]] = [list(map(int, x.split())) for x in data.splitlines()]
    return [x[0] for x in parsed], [x[1] for x in parsed]


def part_1(data: str) -> int:
    parsed = parse(data)
    a = sorted(parsed[0])
    b = sorted(parsed[1])
    return sum([abs(x - y) for x, y in zip(a, b)])


def part_2(data: str) -> int:
    parsed = parse(data)
    count = Counter(parsed[1])
    return sum([x * count[x] for x in parsed[0]])


if __name__ == "__main__":
    with open("data/01.txt") as f:
        data = f.read()

    # part 1
    assert part_1(EXAMPLE) == 11
    print(f"{part_1(data)=}")

    # part 2
    assert part_2(EXAMPLE) == 31
    print(f"{part_2(data)=}")

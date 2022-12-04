from dataclasses import dataclass


EXAMPLE = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


@dataclass
class Range:
    start: int
    end: int

    def __post_init__(self):
        self.start, self.end = sorted((int(self.start), int(self.end)))

    def __contains__(self, other: "Range") -> bool:
        return self.start <= other.start <= other.end <= self.end

    def overlaps(self, other: "Range") -> bool:
        return (
            self.start <= other.start <= self.end
            or other.start <= self.start <= other.end
        )


def parse(data: str) -> list[tuple[Range, Range]]:
    return [
        tuple(map(lambda z: Range(*z), map(lambda y: y.split("-"), x.split(","))))
        for x in data.split("\n")
    ]


def part_1(data: str) -> int:
    range_pairs = parse(data)
    return sum([1 for a, b in range_pairs if a in b or b in a])


def part_2(data: str) -> int:
    range_pairs = parse(data)
    return sum([1 for a, b in range_pairs if a.overlaps(b) or b.overlaps(a)])


if __name__ == "__main__":
    # data
    with open("data/04.txt") as f:
        data = f.read()
    # part 1
    assert part_1(EXAMPLE) == 2
    print("Part 1:", part_1(data))
    # part 2
    assert part_2(EXAMPLE) == 4
    print("Part 2:", part_2(data))

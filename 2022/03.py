from dataclasses import dataclass


EXAMPLE = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


@dataclass
class RuckSack:
    left: set[str]
    right: set[str]

    @classmethod
    def from_string(cls, string: str) -> "RuckSack":
        n = len(string)
        left, right = string[: n // 2], string[n // 2 :]
        return cls(set(left), set(right))

    @property
    def all(self) -> set[str]:
        return self.left | self.right


def get_priority(item: str) -> int:
    if item.isupper():
        return ord(item) - ord("A") + ord("z") - ord("a") + 2
    else:
        return ord(item) - ord("a") + 1


def parse(data: str) -> list[RuckSack]:
    return [RuckSack.from_string(x) for x in data.split("\n")]


def part_1(data: str) -> int:
    rucksacks = parse(data)

    return sum(
        map(
            lambda x: get_priority(x.pop()),
            [rucksack.left.intersection(rucksack.right) for rucksack in rucksacks],
        ),
    )


def part_2(data: str) -> int:
    rucksacks = parse(data)

    return sum(
        map(
            lambda x: get_priority(x.pop()),
            [
                x[0].all.intersection(x[1].all).intersection(x[2].all)
                for x in zip(*(iter(rucksacks),) * 3)
            ],
        )
    )


if __name__ == "__main__":
    # data
    with open("data/03.txt") as f:
        data = f.read()

    # part 1
    assert part_1(EXAMPLE) == 157
    print("Part 1:", part_1(data))
    # part 2
    assert part_2(EXAMPLE) == 70
    print("Part 2:", part_2(data))

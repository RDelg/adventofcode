RAW = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""


class Elf:
    def __init__(self, meals: list[int]):
        self.meals = meals
        self.sum = sum(meals)

    def __repr__(self):
        return f"Elf({self.meals}) total: {self.sum}"


def parse(data: str) -> list[Elf]:
    return [Elf([int(meal) for meal in elf.split("\n")]) for elf in data.split("\n\n")]


if __name__ == "__main__":
    # data
    with open("data/01.txt") as f:
        data = f.read()
    # Part 1
    assert sorted(parse(RAW), key=lambda x: x.sum)[-1].sum == 24000
    print("Part 1:", sorted(parse(data), key=lambda x: x.sum)[-1].sum)
    # Part 2
    assert (sum([x.sum for x in sorted(parse(RAW), key=lambda x: x.sum)[-3:]])) == 45000
    print(
        "Part 2:", sum([x.sum for x in sorted(parse(data), key=lambda x: x.sum)[-3:]])
    )

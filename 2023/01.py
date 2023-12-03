EXAMPLE = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

EXAMPLE_PART_2 = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


NUMBERS_AS_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "zero": 0,
}


def part_1(data: str) -> int:
    return sum(
        map(
            lambda x: (int(x[0] + x[1])),
            [
                ((x := [c for c in line if not c.isalpha()])[0], x[-1])
                for line in data.splitlines()
            ],
        )
    )


def part_2(data: str) -> int:
    for word, number in NUMBERS_AS_WORDS.items():
        data = data.replace(word, word + str(number) + word)

    return sum(
        map(
            lambda x: (int(x[0] + x[1])),
            [
                ((x := [c for c in line if not c.isalpha()])[0], x[-1])
                for line in data.splitlines()
            ],
        )
    )


if __name__ == "__main__":
    with open(file="data/01.txt") as f:
        data = f.read()
    assert (part_1(EXAMPLE)) == 142
    print(f"{part_1(data)=}")

    assert (part_2(EXAMPLE_PART_2)) == 281
    print(f"{part_2(data)=}")

EXAMPLE_1 = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

EXAMPLE_2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""


def part_1(data: str) -> int:
    return 0


if __name__ == "__main__":
    with open("2023/08.txt") as f:
        data = f.read()
    # assert (part_1(EXAMPLE_1)) == 2
    # assert (part_1(EXAMPLE_2)) == 6
    print(f"{part_1(EXAMPLE_1) = }")

    # assert (part_2(EXAMPLE)) == 5905
    # print(f"{part_2(data) = }")

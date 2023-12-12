import math
from typing import NamedTuple

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

EXAMPLE_3 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


class Rule(NamedTuple):
    left: str
    right: str

    def __repr__(self) -> str:
        return f"L: {self.left} R: {self.right}"


def parse(data: str) -> tuple[str, dict[str, Rule]]:
    rules = {}
    lines = data.splitlines()
    for line in lines[2:]:
        x = line.split(" = ")
        rules[x[0]] = Rule(*x[1][1:-1].split(", "))
    return lines[0], rules


def part_1(data: str) -> int:
    seq, rules = parse(data)
    current_pos = "AAA"
    count = 0
    while True:
        if current_pos == "ZZZ":
            break
        for r in seq:
            count += 1
            if r == "R":
                current_pos = rules[current_pos].right
            elif r == "L":
                current_pos = rules[current_pos].left
            else:
                raise ValueError(f"Unknown rule: {r}")
            if current_pos == "ZZZ":
                break
    return count


def part_2(data: str) -> int:
    seq, rules = parse(data)
    current_pos = [x for x in rules.keys() if x.endswith("A")]
    counts = []
    for i in range(len(current_pos)):
        end = False
        count = 0
        while not end:
            for r in seq:
                count += 1
                if r == "R":
                    current_pos[i] = rules[current_pos[i]].right
                elif r == "L":
                    current_pos[i] = rules[current_pos[i]].left
                else:
                    raise ValueError(f"Unknown rule: {r}")
                if current_pos[i].endswith("Z"):
                    end = True
                    break
        counts.append(count)
    return math.lcm(*counts)


if __name__ == "__main__":
    with open("data/08.txt") as f:
        data = f.read()
    assert (part_1(EXAMPLE_1)) == 2
    assert (part_1(EXAMPLE_2)) == 6
    print(f"{part_1(data) = }")

    assert (part_2(EXAMPLE_3)) == 6
    print(f"{part_2(data) = }")

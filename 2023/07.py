from itertools import groupby
from typing import NamedTuple

EXAMPLE = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


CARDS_VALUE = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


class Hand(NamedTuple):
    cards: str
    bet: int

    def __repr__(self) -> str:
        return f"{self.cards} {self.bet}"

    @property
    def group(self) -> dict[str, list[str]]:
        return {
            k: list(g)
            for k, g in groupby(sorted(self.cards, key=lambda x: CARDS_VALUE[x]))
        }


def parse(data: str) -> list[Hand]:
    return [Hand(x[:5], int(x[6:])) for x in data.splitlines()]


def part_1(data: str) -> int:
    hands = parse(data)
    print(hands[0].cards, hands[0].group)
    return 0


if __name__ == "__main__":
    with open(file="data/07.txt") as f:
        data = f.read()
    # assert (part_1(EXAMPLE)) == 220
    print(f"{part_1(EXAMPLE) = }")

    # assert (part_2(EXAMPLE)) == 765
    # print(f"{part_2(data) = }")

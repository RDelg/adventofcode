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

CARDS_VALUE_WITH_JOKER = {**CARDS_VALUE, "J": 1}


class Hand(NamedTuple):
    cards: str
    bet: int
    use_joker: bool = False

    def __repr__(self) -> str:
        return f"{self.cards} {self.bet}"

    @property
    def group(self) -> dict[str, list[str]]:
        g = {k: list(g) for k, g in groupby(sorted(self.cards))}
        if not self.use_joker:
            return g
        if "J" in g and len(g) > 1:
            j_group = g["J"]
            del g["J"]
            max_key = max(g, key=lambda x: len(g[x]))
            g[max_key].extend(j_group)
        return g

    @property
    def cards_as_hex(self) -> str:
        convert = CARDS_VALUE_WITH_JOKER if self.use_joker else CARDS_VALUE
        return "".join([hex(convert[c])[2:] for c in self.cards])

    def is_five_of_a_kind(self) -> bool:
        return len(self.group) == 1

    def is_four_of_a_kind(self) -> bool:
        return any(len(v) == 4 for v in self.group.values())

    def is_full_house(self) -> bool:
        return len(self.group) == 2 and any(len(v) == 3 for v in self.group.values())

    def is_tree_of_a_kind(self) -> bool:
        return any(len(v) == 3 for v in self.group.values())

    def is_two_pairs(self) -> bool:
        return (
            len(self.group) == 3
            and sum([len(v) == 2 for v in self.group.values()]) == 2
        )

    def is_one_pair(self) -> bool:
        return len(self.group) == 4 and any(len(v) == 2 for v in self.group.values())

    def is_high_card(self) -> bool:
        return len(self.group) == 5

    @property
    def value(self) -> int:
        if self.is_five_of_a_kind():
            return 10
        if self.is_four_of_a_kind():
            return 9
        if self.is_full_house():
            return 8
        if self.is_tree_of_a_kind():
            return 7
        if self.is_two_pairs():
            return 6
        if self.is_one_pair():
            return 5
        if self.is_high_card():
            return 4
        raise ValueError("No hand value")


def parse(data: str, use_joker: bool = False) -> list[Hand]:
    return [Hand(x[:5], int(x[6:]), use_joker) for x in data.splitlines()]


def get_gainings(hands: list[Hand]) -> int:
    grouped_hands = groupby(sorted(hands, key=lambda x: x.value), key=lambda x: x.value)
    rank = 1
    total_gainings = 0
    for _, g in grouped_hands:
        l = list(g)
        if len(l) == 1:
            total_gainings += l[0].bet * rank
            rank += 1
        else:
            sort = sorted(l, key=lambda x: x.cards_as_hex)
            for hand in sort:
                total_gainings += hand.bet * rank
                rank += 1
    return total_gainings


def part_1(data: str) -> int:
    hands = parse(data)
    return get_gainings(hands)


def part_2(data: str) -> int:
    hands = parse(data, True)
    return get_gainings(hands)


if __name__ == "__main__":
    with open(file="data/07.txt") as f:
        data = f.read()
    assert (part_1(EXAMPLE)) == 6440
    print(f"{part_1(data) = }")

    assert (part_2(EXAMPLE)) == 5905
    print(f"{part_2(data) = }")

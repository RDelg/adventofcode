from typing import NamedTuple

EXAMPLE = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


class Card(NamedTuple):
    id: int
    winning_numbers: set[int]
    numbers: set[int]

    @classmethod
    def from_str(cls, string: str) -> "Card":
        card_id_str, all_numbers_str = string.split(":")
        card_id = int(card_id_str.split()[1])
        winning_numbers_str, numbers_str = all_numbers_str.split("|")
        winning_numbers = set(int(n) for n in winning_numbers_str.split())
        numbers = set(int(n) for n in numbers_str.split())
        return cls(id=card_id, winning_numbers=winning_numbers, numbers=numbers)

    @property
    def score(self) -> int:
        return len(self.winning_numbers & self.numbers)


def part_1(string: str) -> int:
    cards = [Card.from_str(line) for line in string.splitlines()]
    return sum([2 ** (card.score - 1) for card in cards if card.score > 0])


def part_2(string: str) -> int:
    cards = [Card.from_str(line) for line in string.splitlines()]
    n_cards = [1 for _ in range(len(cards))]
    for i, card in enumerate(cards):
        for j in range(card.score):
            n_cards[i + j + 1] += n_cards[i]

    return sum(n_cards)


if __name__ == "__main__":
    with open(file="data/04.txt") as f:
        data = f.read()

    assert part_1(EXAMPLE) == 13
    print(f"{part_1(data) = }")

    assert part_2(EXAMPLE) == 30
    print(f"{part_2(data) = }")

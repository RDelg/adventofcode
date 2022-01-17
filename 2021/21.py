from collections import defaultdict
from typing import Dict, Iterator, List, Tuple
from functools import lru_cache
from itertools import product


RAW = """\
Player 1 starting position: 4
Player 2 starting position: 8
"""


def deterministic_dice(n: int) -> Iterator[List[int]]:
    sides = 100
    start = iteration = 0
    while 1:
        for i in range(start, ((sides // n) + iteration + 1) * n, n):
            yield [1 + (j + i) % sides for j in range(n)]
        iteration += 1
        start = ((sides // n) + iteration) * n


def parse_input(data: str) -> Tuple[int, int]:
    return tuple([int(x.split(" ")[-1]) for x in data.strip().split("\n")])


def play_1(data: str, iters: int = 500) -> Tuple[int, int, int]:
    LIMIT = 1_000
    p1, p2 = parse_input(data)
    p1s, p2s = 0, 0
    for i, v in zip(range(iters), deterministic_dice(3)):
        if i % 2:
            p2 = ((p2 - 1 + sum(v)) % 10) + 1
            p2s += p2
        else:
            p1 = ((p1 - 1 + sum(v)) % 10) + 1
            p1s += p1
        if p1s >= LIMIT or p2s >= LIMIT:
            break

    return p1s, p2s, i


@lru_cache(maxsize=None)
def roll(max_value: int, dices: int) -> Dict[int, int]:
    sums = defaultdict(lambda: 0)
    for roll in product(range(1, max_value + 1), repeat=dices):
        sums[sum(roll)] += 1
    return sums


@lru_cache(maxsize=None)
def dirac_roll(s1: int, s2: int, p1: int, p2: int, multiplier: int = 1) -> Tuple[int]:
    win_1 = win_2 = 0
    for v1, count in roll(max_value=3, dices=3).items():
        wrap = lambda x, add: ((x - 1 + add) % 10) + 1
        new_s1 = wrap(s1, v1)
        new_p1 = p1 + new_s1
        if new_p1 >= 21:
            win_1 += count * multiplier
        else:
            new_win_2, new_win_1 = dirac_roll(
                s2, new_s1, p2, new_p1, count * multiplier
            )
            win_1 += new_win_1
            win_2 += new_win_2
    return win_1, win_2


if __name__ == "__main__":
    with open("data/21.txt") as f:
        data = f.read()

    # Part 1
    # Demo
    p1s, p2s, its = play_1(RAW)
    assert min(p1s, p2s) * (its + 1) * 3 == 739785
    # Real
    p1s, p2s, its = play_1(data)
    print("Part 1:", min(p1s, p2s) * (its + 1) * 3)

    # Part 2
    assert dirac_roll(4, 8, 0, 0) == (444356092776315, 341960390180808)
    p1, p2 = parse_input(data)
    print("Part 2:", max(dirac_roll(p1, p2, 0, 0)))

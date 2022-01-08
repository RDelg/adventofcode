from typing import Iterator, List, Tuple


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

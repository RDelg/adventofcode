from functools import reduce
from math import ceil, floor
import re

EXAMPLE = """\
Time:      7  15   30
Distance:  9  40  200"""


def parse1(data: str) -> list[tuple[int, int]]:
    x = [re.findall(r"\d+", x) for x in data.splitlines()]
    return [(int(x), int(y)) for x, y in zip(*x)]


# same format as part 1, but different parsing
def parse2(data: str) -> list[tuple[int, int]]:
    x = ["".join(re.findall(r"\d+", x)) for x in data.splitlines()]
    return [(int(x[0]), int(x[1]))]


def find_roots(t: float, disttance: float) -> tuple[float, float]:
    det = t**2 - 4 * disttance
    if det < 0:
        raise ValueError("No roots")
    det = (det**0.5) / 2
    return t / 2 + det, t / 2 - det


def evaluate(t: float, max_time: float) -> float:
    return (max_time - t) * t


def get_value(data: list[tuple[int, int]]) -> float:
    roots = [find_roots(*x) for x in data]
    evals = [
        (x[1], (evaluate(floor(y[0]), x[0]), evaluate(ceil(y[1]), x[0])))
        for x, y in zip(data, roots)
    ]

    b = [1 if x[1][0] > x[0] < x[1][1] else -1 for x in evals]
    distances = [floor(x[0]) - ceil(x[1]) + y for x, y in zip(roots, b)]
    return reduce(lambda x, y: x * y, distances)


def part_1(data: str) -> int:
    parsed = parse1(data)
    return int(get_value(parsed))


def part_2(data: str) -> int:
    parsed = parse2(data)
    return int(get_value(parsed))


if __name__ == "__main__":
    with open(file="data/06.txt") as f:
        data = f.read()
    assert (part_1(EXAMPLE)) == 288
    print(f"{part_1(data) = }")

    assert (part_2(EXAMPLE)) == 71503
    print(f"{part_2(data) = }")

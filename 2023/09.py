EXAMPLE = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def parse(data: str) -> list[list[int]]:
    return [list(map(int, line.split())) for line in data.splitlines()]


def process_sequence(sequence: list[int]) -> list[list[int]]:
    seq = sequence.copy()
    sequences = [seq]
    while not all(y == 0 for y in seq):
        seq = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
        sequences.append(seq)
    return sequences


def part_1(data: str) -> int:
    sequences = parse(data)
    n = 0
    for seq in sequences:
        seqs = process_sequence(seq)
        n += sum([x[-1] for x in seqs])
    return n


def part_2(data: str) -> int:
    sequences = parse(data)
    n = 0
    for seq in sequences:
        seqs = process_sequence(seq)
        m = 0
        for s in reversed(seqs[:-1]):
            m = s[0] - m
        n += m
    return n


if __name__ == "__main__":
    with open("data/09.txt") as f:
        data = f.read()

    assert (part_1(EXAMPLE)) == 114
    print(f"{part_1(data) = }")

    assert (part_2(EXAMPLE)) == 2
    print(f"{part_2(data) = }")

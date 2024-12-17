from collections import defaultdict
from collections.abc import Generator
from typing import NamedTuple

EXAMPLE = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


class Rule(NamedTuple):
    after: int
    before: int


def parse(raw: str) -> tuple[list[Rule], list[list[int]]]:
    raw_rules, raw_seqs = raw.strip().split("\n\n")
    rules = [Rule(*map(int, rule.split("|"))) for rule in raw_rules.split("\n")]
    seqs = [list(map(int, seq.split(","))) for seq in raw_seqs.split("\n")]
    return rules, seqs


def generate_index_pairs(sequent: list[int]) -> Generator[tuple[int, int], None, None]:
    for i in range(len(sequent) - 1):
        for j in range(i + 1, len(sequent)):
            yield i, j


def is_sorted(seq: list[int], rules_grouped: dict[int, list[Rule]]) -> bool:
    ok = True
    for i, j in generate_index_pairs(seq):
        pair = (seq[i], seq[j])
        if any(r.after == pair[1] and r.before == pair[0] for r in rules_grouped[pair[0]]):
            ok = False
            break
    return ok


def part_1(raw: str) -> int:
    rules, seqs = parse(raw)
    rules_by_before = defaultdict(list)
    for r in rules:
        rules_by_before[r.before].append(r)
    v = 0
    for seq in seqs:
        if is_sorted(seq, rules_by_before):
            v += seq[len(seq) // 2]
    return v


def part_2(raw: str) -> int:
    rules, seqs = parse(raw)
    rules_by_before = defaultdict(list)
    for r in rules:
        rules_by_before[r.before].append(r)

    v = 0
    for seq in seqs:
        sorted = True
        while not is_sorted(seq, rules_by_before):
            sorted = False
            for i, j in generate_index_pairs(seq):
                pair = (seq[i], seq[j])
                for r in rules_by_before[pair[0]]:
                    if r.after == pair[1] and r.before == pair[0]:
                        seq[i], seq[j] = seq[j], seq[i]
                        break
        if not sorted:
            v += seq[len(seq) // 2]

    return v


if __name__ == "__main__":
    # data
    with open("data/05.txt") as f:
        data = f.read()

    # part 1
    assert part_1(EXAMPLE) == 143
    print(f"{part_1(data)= }")

    # part 2
    assert part_2(EXAMPLE) == 123
    print(f"{part_2(data)= }")

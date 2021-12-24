from collections import defaultdict
from typing import Dict


RAW_DEMO = """\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""


class Polymer:
    def __init__(self, data: str) -> None:
        sequence, rules = data.strip().split("\n\n")
        self.rules_dict = self.parse_rules(rules)
        self.sequence_str = sequence
        self.steps = 0
        self.sequence_histogram = self.create_sequence_histogram()

    def create_sequence_histogram(self) -> Dict[str, int]:
        histogram = defaultdict(lambda: 0)
        for i in range(len(self.sequence_str) - 1):
            histogram[self.sequence_str[i : i + 2]] += 1
        return histogram

    @staticmethod
    def parse_rules(rules: str) -> Dict[str, str]:
        return {
            rule.split(" -> ")[0]: rule.split(" -> ")[1] for rule in rules.split("\n")
        }

    def step(self, steps: int = 1) -> None:
        for _ in range(steps):
            self.step_once()

    def step_once(self) -> None:
        new_hist = defaultdict(lambda: 0)
        for seq, count in self.sequence_histogram.items():
            seq1, seq2 = seq[0] + self.rules_dict[seq], self.rules_dict[seq] + seq[1]
            new_hist[seq1] += count
            new_hist[seq2] += count
        self.sequence_histogram = new_hist

        self.steps += 1

    def letter_histogram(self) -> Dict[str, int]:
        letter_hist = defaultdict(lambda: 0)
        for k, v in self.sequence_histogram.items():
            letter_hist[k[1]] += v
        return letter_hist

    def generate_solution(self) -> int:
        letter_hist = self.letter_histogram()
        return max(letter_hist.values()) - min(letter_hist.values())

    def __str__(self) -> str:
        return f"{self.sequence_histogram} after {self.steps} steps"

    def __repr__(self) -> str:
        return str(self)


if __name__ == "__main__":
    # Data
    with open("data/14.txt") as f:
        data = f.read()
    # Part 1
    # Demo
    p = Polymer(RAW_DEMO)
    p.step(10)
    assert p.generate_solution() == 1588
    # Real
    p = Polymer(data)
    p.step(10)
    print("Part 1:", p.generate_solution())
    # Part 2
    # Demo
    p = Polymer(RAW_DEMO)
    p.step(40)
    assert p.generate_solution() == 2188189693529
    p = Polymer(data)
    p.step(40)
    print("Part 2:", p.generate_solution())

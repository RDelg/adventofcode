from typing import List
from collections import defaultdict


RAW = "3,4,3,1,2"


class LanternFishSimulator:
    max_days: int = 9
    reset_day: int = 6

    def __init__(self, init_states: List[int]):
        group_dict = defaultdict(lambda: 0)
        for state in init_states:
            group_dict[state] += 1

        self.group = [group_dict.get(i, 0) for i in range(self.max_days)]

    def new_day(self) -> None:
        zeros = self.group[0]
        for i in range(1, self.max_days):

            self.group[i - 1] = self.group[i]
        self.group[self.max_days - 1] = zeros
        self.group[self.reset_day] += zeros

    def simulate(self, n: int) -> None:
        for _ in range(n):
            self.new_day()

    def __repr__(self) -> str:
        return str(self)

    def total(self) -> int:
        return sum(self.group)

    def __str__(self) -> str:
        return str(self.total())


if __name__ == "__main__":
    fishes = LanternFishSimulator([int(i) for i in RAW.split(",")])
    fishes.simulate(18)
    assert (fishes.total()) == 26
    fishes = LanternFishSimulator([int(i) for i in RAW.split(",")])
    fishes.simulate(80)
    assert (fishes.total()) == 5934

    # Part 1
    with open("data/06.txt") as f:
        raw = f.read().strip()
    fishes = LanternFishSimulator([int(i) for i in raw.split(",")])
    fishes.simulate(80)
    print(f"Part 1: {fishes.total()}")

    # Part 2
    fishes = LanternFishSimulator([int(i) for i in RAW.split(",")])
    fishes.simulate(256)
    assert (fishes.total()) == 26984457539
    fishes = LanternFishSimulator([int(i) for i in raw.split(",")])
    fishes.simulate(256)
    print(f"Part 2: {fishes.total()}")

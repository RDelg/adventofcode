from collections import defaultdict
from typing import List


RAW_DEMO_1 = """\
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

RAW_DEMO_2 = """\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""

RAW_DEMO_3 = """\
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""


class Graph:
    def __init__(self, data: str) -> None:
        self.set_adj_dict(data)

    def set_adj_dict(self, data: str) -> None:
        self.adj_dict = defaultdict(list)
        for line in data.strip().split("\n"):
            state, next_state = line.split("-")
            self.adj_dict[state].append(next_state)
            self.adj_dict[next_state].append(state)
        self.all_lower_states = [x for x in self.adj_dict if x.islower()]

    def step(self, paths: List[List[str]], small_q_once: int = 1) -> List[List[str]]:
        not_ending_idx = [i for i, x in enumerate(paths) if x[-1] != "end"]
        if not len(not_ending_idx):
            return paths
        new_paths = [x for i, x in enumerate(paths) if i not in not_ending_idx]
        for i in not_ending_idx:
            current_path = paths[i]
            current_state = current_path[-1]
            counts = defaultdict(lambda: 0)
            for s in current_path:
                counts[s] += 1
            used = [x for x, c in counts.items() if c >= small_q_once and x.islower()]
            if len(used):
                used = [x for x in counts if x.islower()]
            possibilities = (
                set(self.adj_dict[current_state]) - set(used) - set(["start"])
            )
            if not len(possibilities):
                continue
            for state in list(possibilities):
                new_paths.append(current_path + [state])
        return self.step(new_paths, small_q_once=small_q_once)


if __name__ == "__main__":
    # Data
    with open("data/12.txt", "r") as f:
        data = f.read()
    # Part 1
    # Demo 1
    g = Graph(RAW_DEMO_1)
    new_paths = g.step([["start"]])
    assert len(new_paths) == 10
    # Demo 2
    g = Graph(RAW_DEMO_2)
    new_paths = g.step([["start"]])
    assert len(new_paths) == 19
    # Demo 3
    g = Graph(RAW_DEMO_3)
    new_paths = g.step([["start"]])
    assert len(new_paths) == 226
    # Real
    g = Graph(data)
    new_paths = g.step([["start"]])
    print("Part 1:", len(new_paths))

    # Part 2
    # Demo 1
    g = Graph(RAW_DEMO_1)
    new_paths = g.step([["start"]], small_q_once=2)
    assert len(new_paths) == 36
    # Demo 2
    g = Graph(RAW_DEMO_2)
    new_paths = g.step([["start"]], small_q_once=2)
    assert len(new_paths) == 103
    # Demo 3
    g = Graph(RAW_DEMO_3)
    new_paths = g.step([["start"]], small_q_once=2)
    assert len(new_paths) == 3509
    # Real
    print("This part is not optimized!!!")
    g = Graph(data)
    new_paths = g.step([["start"]], small_q_once=2)
    print("Part 2:", len(new_paths))

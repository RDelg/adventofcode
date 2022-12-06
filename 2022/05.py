import re
from collections import deque
from typing import Deque, NamedTuple


EXAMPLE = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


Crate = str
CratesStack = Deque[Crate]


class Move(NamedTuple):
    quantity: int
    from_idx: int
    to_idx: int


def parse(data: str) -> tuple[Deque[CratesStack], list[Move]]:
    move_regexp = re.compile(r"move (\d+) from (\d+) to (\d+)")

    state, moves = data.split("\n\n")
    moves = [
        Move(*map(int, re.match(move_regexp, x).groups())) for x in moves.splitlines()
    ]
    state, n_idxs = (x := state.splitlines())[:-1], len(re.findall("\d+", x[-1]))

    def split_by_length(s: str, n_idxs: int) -> list[str]:
        return [s[i * 4 - 3] for i in range(1, n_idxs + 1)]

    state = [split_by_length(x, n_idxs) for x in state]

    crates_stack = [deque() for _ in range(n_idxs)]
    for state in reversed(state):
        for idx, crate in enumerate(state):
            if crate != " ":
                crates_stack[idx].append(crate)

    return crates_stack, moves


def part_1(data: str) -> str:
    crates_stack, moves = parse(data)
    for move in moves:
        crates_stack[move.to_idx - 1].extend(
            crates_stack[move.from_idx - 1].pop()
            for _ in range(min(move.quantity, len(crates_stack[move.from_idx - 1])))
        )
    return "".join([stack.pop() for stack in crates_stack])


def part_2(data: str) -> str:
    crates_stack, moves = parse(data)
    for move in moves:
        crates_stack[move.to_idx - 1].extend(
            reversed(
                [
                    crates_stack[move.from_idx - 1].pop()
                    for _ in range(
                        min(move.quantity, len(crates_stack[move.from_idx - 1]))
                    )
                ]
            )
        )
    return "".join([stack.pop() for stack in crates_stack])


if __name__ == "__main__":
    # data
    with open("data/05.txt") as f:
        data = f.read()
    # part 1
    assert part_1(EXAMPLE) == "CMZ"
    print("Part 1:", part_1(data))
    # part 2
    assert part_2(EXAMPLE) == "MCD"
    print("Part 2:", part_2(data))

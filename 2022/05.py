
import re
from typing import NamedTuple



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
CratesStack = list[Crate]

class Move(NamedTuple):
    quantity: int
    from_idx: int
    to_idx: int

def parse(data: str) -> tuple[list[CratesStack], list[Move]]:
    move_regexp = re.compile(r"move (\d+) from (\d+) to (\d+)")
    idxs_regexp = re.compile(r"\s+(\d+)\s+(\d+)\s+(\d+)\s+")

    state, moves = data.split("\n\n")
    moves = [Move(*map(int, re.match(move_regexp, x).groups())) for x in moves.splitlines()]
    state, n_idxs = (x:= state.splitlines())[:-1], len(re.match(idxs_regexp, x[-1]).groups())
    state = [re.findall(r"\[(\w)\]", x) for x in state]
    print(state)



def part_1(data: str) -> int:
    parse(data)

if __name__ == "__main__":

    print("Part 1:", part_1(EXAMPLE))
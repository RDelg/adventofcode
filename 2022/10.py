from dataclasses import dataclass
from enum import Enum


EXAMPLE = """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


class Instruction(str, Enum):
    ADDX = "addx"
    NOOP = "noop"


@dataclass
class CPU:
    x_reg = 1
    counter = 0

    def execute(self, instruction: str):
        split = instruction.split(" ")
        instruction = Instruction(split[0])
        if instruction == Instruction.ADDX:
            self.x_reg += int(split[1])
            self.counter += 2
            return 2
        elif instruction == Instruction.NOOP:
            self.counter += 1
            return 1


@dataclass
class CRT:
    sprite_len: int = 3
    sprite_pos = 0
    width: int = 40
    height: int = 6
    cpu = CPU()
    screen = [[0 for _ in range(40)] for _ in range(6)]
    counter = 0

    def execute(self, instruction: str):
        current_x_reg = self.cpu.x_reg
        self._draw(current_x_reg)
        n = self.cpu.execute(instruction)
        self.counter += 1
        if n > 1:
            self._draw(current_x_reg)
            self.counter += 1

    def _draw(self, current_x_reg: int) -> None:
        x = self.counter % self.width
        y = self.counter // self.width

        symbol = "#" if current_x_reg - 2 < x < current_x_reg + 2 else "."
        self.screen[y][x] = symbol

    def __repr__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self.screen)


def part_1(data: str) -> int:
    cpu = CPU()
    hist = []
    for line in data.splitlines():
        cpu.execute(line)
        hist.append((cpu.counter, cpu.x_reg))

    IDXS = [20, 60, 100, 140, 180, 220]
    match = lambda x: next(filter(lambda y: x <= y[1][0], enumerate(hist)))[0]
    idxs = [x if hist[(x := match(index))][1] == x else x - 1 for index in IDXS]
    values = [hist[index][1] * index_2 for index, index_2 in zip(idxs, IDXS)]
    return sum(values)


def part_2(data: str) -> str:
    screen = CRT()
    for line in data.splitlines():
        screen.execute(line)
    return screen


if __name__ == "__main__":
    # data
    with open("data/10.txt") as f:
        data = f.read()
    # part 1
    assert part_1(EXAMPLE) == 13140
    print("Part 1:", part_1(data))
    # part 2
    print(f"Part 2:\n {part_2(data)}")

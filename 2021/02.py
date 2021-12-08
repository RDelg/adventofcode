from enum import Enum
from dataclasses import dataclass
from typing import List


class Direction(str, Enum):
    forward: str = "forward"
    down: str = "down"
    up: str = "up"


@dataclass
class Submarine:
    position: int = 0
    depth: int = 0
    aim: int = 0

    def move(self, direction: Direction, distance: int):
        if direction == Direction.forward:
            self.position += distance
        elif direction == Direction.down:
            self.depth += distance
        elif direction == Direction.up:
            self.depth -= distance
        else:
            raise ValueError(f"Invalid direction: {direction}")

    def move_using_aim(self, direction: Direction, distance: int):
        if direction == Direction.forward:
            self.position += distance
            self.depth += self.aim * distance
        elif direction == Direction.down:
            self.aim += distance
        elif direction == Direction.up:
            self.aim -= distance
        else:
            raise ValueError(f"Invalid direction: {direction}")


RAW_DEMO = """\
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""

INPUT_DEMO = [x.split(" ") for x in RAW_DEMO.strip().split("\n")]

submarine = Submarine()

for x in INPUT_DEMO:
    submarine.move(x[0], int(x[1]))


# Part 1
assert (submarine.position, submarine.depth) == (15, 10)
assert submarine.position * submarine.depth == 150
with open("data/02.txt", "r") as f:
    INPUT = [x.split(" ") for x in f.read().strip().split("\n")]

submarine = Submarine()

for x in INPUT:
    submarine.move(x[0], int(x[1]))

# Part 2

submarine = Submarine()
for x in INPUT_DEMO:
    submarine.move_using_aim(x[0], int(x[1]))

assert (submarine.position, submarine.depth) == (15, 60)
assert submarine.position * submarine.depth == 900

submarine = Submarine()
for x in INPUT:
    submarine.move_using_aim(x[0], int(x[1]))

print(submarine.position * submarine.depth)

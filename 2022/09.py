from dataclasses import dataclass
from enum import Enum
import math


EXAMPLE = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


class Direction(str, Enum):
    RIGHT = "R"
    LEFT = "L"
    UP = "U"
    DOWN = "D"


@dataclass
class Move:
    direction: Direction
    distance: int


@dataclass
class Position:
    x: int
    y: int


class Rope:
    head: Position
    tail: Position

    def __init__(self, head: Position, tail: Position):
        self.head = head
        self.tail = tail

    @classmethod
    def zero(cls):
        return cls(Position(0, 0), Position(0, 0))

    def _move_tail(self):

        x_diff, x_sign = (
            abs((x := self.head.x - self.tail.x)),
            int(math.copysign(1, x)),
        )

        y_diff, y_sign = (
            abs((x := self.head.y - self.tail.y)),
            int(math.copysign(1, x)),
        )

        # print(self.head, self.tail, x_diff, x_sign, y_diff, y_sign)

        if x_diff == 0 and y_diff == 0:
            return

        if x_diff > 1:
            self.tail.x += x_sign
            if y_diff > 0:
                self.tail.y += y_sign

        if y_diff > 1:
            self.tail.y += y_sign
            if x_diff > 0:
                self.tail.x += x_sign

        return

    def move_head(self, direction: Direction):
        if direction == Direction.RIGHT:
            self.head.x += 1
        elif direction == Direction.LEFT:
            self.head.x -= 1
        elif direction == Direction.UP:
            self.head.y += 1
        elif direction == Direction.DOWN:
            self.head.y -= 1
        else:
            raise ValueError(f"Unknown direction {direction}")

        self._move_tail()

    def __repr__(self):
        return f"Rope({self.head}, {self.tail})"


def part_1(data: str) -> int:
    moves = [
        Move(Direction((y := x.split(" "))[0]), int(y[1])) for x in data.split("\n")
    ]

    rope = Rope.zero()

    tail_history = set()
    for move in moves:
        # print("move", move)
        for _ in range(move.distance):
            rope.move_head(move.direction)
            # print(rope.head, rope.tail)
            tail_history.add((rope.tail.x, rope.tail.y))
    return len(tail_history)


def part_2(data: str) -> int:
    return 0


if __name__ == "__main__":
    # data
    with open("data/09.txt") as f:
        data = f.read()
    # part 1
    assert part_1(EXAMPLE) == 13
    print("Part 1:", part_1(data))
    # part 2
    # print("Part 2:", part_2(EXAMPLE))
    # 4647 low

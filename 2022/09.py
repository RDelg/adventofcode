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

EXAMPLE_2 = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""


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
    knots: list[Position]

    def __init__(self, knots: list[Position]):
        self.knots = knots

    @classmethod
    def zero(cls, length: int = 2):
        return cls([Position(0, 0) for _ in range(length)])

    def _move_tail(self):
        for i in range(1, len(self.knots)):
            head = self.knots[i - 1]
            tail = self.knots[i]

            x_diff, x_sign = (
                abs((x := head.x - tail.x)),
                int(math.copysign(1, x)),
            )

            y_diff, y_sign = (
                abs((x := head.y - tail.y)),
                int(math.copysign(1, x)),
            )

            is_same = x_diff == 0 and y_diff == 0
            is_adjacent = x_diff == 1 and y_diff == 0 or x_diff == 0 and y_diff == 1
            is_diagonal = x_diff == 1 and y_diff == 1

            if is_same or is_adjacent or is_diagonal:
                break

            if x_diff > 1:
                tail.x += x_sign
                if y_diff == 1:
                    tail.y += y_sign

            if y_diff > 1:
                tail.y += y_sign
                if x_diff == 1:
                    tail.x += x_sign
        return

    def move_head(self, direction: Direction):
        if direction == Direction.RIGHT:
            self.knots[0].x += 1
        elif direction == Direction.LEFT:
            self.knots[0].x -= 1
        elif direction == Direction.UP:
            self.knots[0].y += 1
        elif direction == Direction.DOWN:
            self.knots[0].y -= 1
        else:
            raise ValueError(f"Unknown direction {direction}")

        self._move_tail()

    def __repr__(self):
        return f"Rope({self.head}, {self.tail})"


def parse_moves(data: str) -> list[Move]:
    return [
        Move(Direction((y := x.split(" "))[0]), int(y[1])) for x in data.split("\n")
    ]


def part_1(data: str) -> int:
    moves = parse_moves(data)
    rope = Rope.zero()
    tail_history = set()
    for move in moves:
        for _ in range(move.distance):
            rope.move_head(move.direction)
            tail_history.add((rope.knots[-1].x, rope.knots[-1].y))
    return len(tail_history)


def part_2(data: str) -> int:
    moves = parse_moves(data)
    rope = Rope.zero(10)
    tail_history = set()
    for move in moves:
        for m in range(move.distance):
            rope.move_head(move.direction)
            tail_history.add((rope.knots[-1].x, rope.knots[-1].y))
    return len(tail_history)


if __name__ == "__main__":
    # data
    with open("data/09.txt") as f:
        data = f.read()
    # part 1
    assert part_1(EXAMPLE) == 13
    print("Part 1:", part_1(data))
    # part 2
    assert part_2(EXAMPLE) == 1
    assert part_2(EXAMPLE_2) == 36
    print("Part 2:", part_2(data))

from enum import Enum
from typing import List, NamedTuple


RAW_DEMO = """\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""


class Direction(str, Enum):
    x = "x"
    y = "y"


class Point(NamedTuple):
    x: int
    y: int


class Fold(NamedTuple):
    direction: Direction
    value: int


class Paper:
    def __init__(self, data: str) -> None:
        points, folds = data.strip().split("\n\n")
        self.points = self.parse_points(points)
        self.folds = self.parse_folds(folds)
        self.max_point = self.get_max_points()
        self.size = (self.max_point.x + 1, self.max_point.y + 1)
        self.grid = self.create_grid()

    def create_grid(self) -> List[List[int]]:
        grid = [
            [False for _ in range(self.max_point.x + 1)]
            for _ in range(self.max_point.y + 1)
        ]
        for point in self.points:
            grid[point.y][point.x] = True
        return grid

    @staticmethod
    def parse_points(points: str) -> List[Point]:
        return [Point(*map(int, point.split(","))) for point in points.split("\n")]

    @staticmethod
    def parse_folds(folds: str) -> List[Fold]:
        return [
            Fold((x := fold.split(" ")[-1].split("="))[0], int(x[1]))
            for fold in folds.split("\n")
        ]

    def get_max_points(self) -> Point:
        x, y = 0, 0
        for point in self.points:
            x = max(x, point.x)
            y = max(y, point.y)
        return Point(x, y)

    def __str__(self) -> str:
        to_char = lambda x: "#" if x else "."
        return "\n".join(["".join(map(to_char, row)) for row in self.grid])

    def __repr__(self) -> str:
        return str(self)

    def fold(self, just_first: bool = False) -> "Paper":
        for fold in self.folds:
            self.fold_along(fold.direction, fold.value)
            if just_first:
                break
        return self

    def fold_along(self, direction: Direction, value: int):
        if direction == Direction.x:
            self.fold_along_x(value)
        elif direction == Direction.y:
            self.fold_along_y(value)
        else:
            raise ValueError(f"Unknown direction: {direction}")

    def fold_along_x(self, value: int):
        to_char = lambda x: "#" if x else "."
        to_str = lambda x: "".join(list(map(to_char, x)))
        new_grid = [[False for _ in range(value)] for _ in range(self.size[0])]
        for y in range(len(self.grid)):
            a = self.grid[y][:value]
            b = self.grid[y][value + 1 :][::-1]
            new_grid[y] = [xx + yy for xx, yy in zip(a, b)]
        self.grid = new_grid
        self.size = (len(self.grid), len(self.grid[0]))

    def fold_along_y(self, value: int):
        to_char = lambda x: "#" if x else "."
        to_str = lambda x: "\n".join(["".join(map(to_char, row)) for row in x[:value]])
        a = self.grid[:value]
        b = self.grid[value + 1 :][::-1]
        assert len(a) == len(b), f"{len(a)} != {len(b)}"
        assert len(a[0]) == len(b[0]), f"{len(a[0])} != {len(b[0])}"
        self.grid = [[xx + yy for xx, yy in zip(x, y)] for x, y in zip(a, b)]
        self.size = (len(self.grid), len(self.grid[0]))

    def count_points(self) -> int:
        return sum(sum([1 if x else 0 for x in row]) for row in self.grid)


if __name__ == "__main__":
    # Data
    with open("data/13.txt") as f:
        data = f.read()
    # Part 1
    # Demo
    p = Paper(RAW_DEMO)
    p.fold(just_first=True)
    assert p.count_points() == 17
    # Real
    p = Paper(data)
    p.fold(just_first=True)
    print("Part 1:", p.count_points())

    # Part 2
    # Real
    p = Paper(data)
    p.fold(just_first=False)
    print("Part 2:", p.count_points())
    print(p)

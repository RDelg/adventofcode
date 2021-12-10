from dataclasses import dataclass
from typing import List

RAW = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""


@dataclass
class Point:
    x: int
    y: int

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return str(self)


@dataclass
class Line:
    start: Point
    end: Point

    def __str__(self):
        return f"{self.start} -> {self.end}"

    def __repr__(self):
        return str(self)


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

    def __str__(self):
        return "\n".join(
            "".join(str(self.grid[y][x]) for x in range(self.width))
            for y in range(self.height)
        ).replace("0", ".")

    def __repr__(self):
        return str(self)

    def diagonal_linespace(self, start: Point, end: Point) -> List[int]:
        """
        Return a list of all the points in the line space between a and b.
        """

    def draw(self, line: Line, include_diagonals: bool = False):
        start = line.start
        end = line.end
        # Horizontal
        if start.y == end.y:
            for x in range(
                *[n + 1 if i > 0 else n for i, n in enumerate(sorted([start.x, end.x]))]
            ):
                self.increase(x, start.y)
        # Vertical
        elif start.x == end.x:
            for y in range(
                *[n + 1 if i > 0 else n for i, n in enumerate(sorted([start.y, end.y]))]
            ):
                self.increase(start.x, y)
        # Diagonal
        elif abs(end.x - start.x) == abs(end.y - start.y):
            if include_diagonals:
                x_range = (
                    range(start.x, end.x + 1)
                    if start.x < end.x
                    else range(start.x, end.x - 1, -1)
                )
                y_range = (
                    range(start.y, end.y + 1)
                    if start.y < end.y
                    else range(start.y, end.y - 1, -1)
                )
                for x, y in zip(x_range, y_range):
                    self.increase(x, y)
        else:
            raise Exception(f"Invalid line: {line}")

    def increase(self, x, y, value=1):

        if x >= self.width:
            self.grid = [l + [0] * (x - self.width + 1) for l in self.grid]
            self.width = x + 1
        if y >= self.height:
            self.grid += [
                [0 for _ in range(self.width)] for _ in range(y - self.height + 1)
            ]
            self.height = y + 1
        self.grid[y][x] += value

    def get(self, x, y):
        return self.grid[y][x]


if __name__ == "__main__":
    # Part 1
    lines_raw = []
    for line in RAW.splitlines():
        start, end = line.split(" -> ")
        start_x, start_y = [int(x) for x in start.split(",")]
        end_x, end_y = [int(x) for x in end.split(",")]
        lines_raw.append(Line(Point(start_x, start_y), Point(end_x, end_y)))

    grid = Grid(10, 10)

    for line in lines_raw:
        grid.draw(line)

    get_points = lambda g: sum([sum([y >= 2 for y in x]) for x in g])

    assert get_points(grid.grid) == 5

    grid = Grid(10, 10)

    with open("data/05.txt") as f:
        lines = [
            Line(
                Point(*[int(x) for x in line.split(" -> ")[0].split(",")]),
                Point(*[int(x) for x in line.split(" -> ")[1].split(",")]),
            )
            for line in f.readlines()
        ]

    for line in lines:
        grid.draw(line)

    print(f"Part 1: {get_points(grid.grid)}")

    # Part 2
    grid = Grid(10, 10)

    for line in lines_raw:
        grid.draw(line, include_diagonals=True)
    assert get_points(grid.grid) == 12

    grid = Grid(989, 989)
    for i, line in enumerate(lines):
        grid.draw(line, include_diagonals=True)

    print(f"Part 2: {get_points(grid.grid)}")

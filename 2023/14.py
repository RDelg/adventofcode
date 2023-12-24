from typing import NamedTuple

EXAMPLE = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


class Grid(NamedTuple):
    grid: list[list[str]]

    @property
    def width(self) -> int:
        return len(self.grid[0])

    @property
    def height(self) -> int:
        return len(self.grid)

    @classmethod
    def from_str(cls, data: str) -> "Grid":
        return cls([list(line) for line in data.splitlines()])

    def __str__(self) -> str:
        return "\n".join("".join(line) for line in self.grid)

    def tilt_upwards(self) -> bool:
        change = False
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == "O":
                    new_y = max(0, y - 1)
                    if self.grid[new_y][x] == ".":
                        self.grid[new_y][x] = "O"
                        self.grid[y][x] = "."
                        change = True
        return change

    def tilt_downwards(self) -> bool:
        change = False
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                if self.grid[y][x] == "O":
                    new_y = min(self.height - 1, y + 1)
                    if self.grid[new_y][x] == ".":
                        self.grid[new_y][x] = "O"
                        self.grid[y][x] = "."
                        change = True
        return change

    def tilt_left(self) -> bool:
        change = False
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == "O":
                    new_x = max(0, x - 1)
                    if self.grid[y][new_x] == ".":
                        self.grid[y][new_x] = "O"
                        self.grid[y][x] = "."
                        change = True
        return change

    def tilt_right(self) -> bool:
        change = False
        for y in range(self.height):
            for x in range(self.width - 1, -1, -1):
                if self.grid[y][x] == "O":
                    new_x = min(self.width - 1, x + 1)
                    if self.grid[y][new_x] == ".":
                        self.grid[y][new_x] = "O"
                        self.grid[y][x] = "."
                        change = True
        return change

    def total_load(self) -> int:
        return sum(
            line.count("O") * (self.height - i) for i, line in enumerate(self.grid)
        )


def part_1(data: str) -> int:
    grid = Grid.from_str(data)
    while grid.tilt_upwards():
        continue
    return grid.total_load()


def iterate(grid: Grid) -> Grid:
    while grid.tilt_upwards():
        continue
    while grid.tilt_left():
        continue
    while grid.tilt_downwards():
        continue
    while grid.tilt_right():
        continue
    return grid


def part_2(data: str) -> int:
    grid = Grid.from_str(data)
    grid_cache = {}
    n = 1_000_000_000
    i = 0
    while i < n:
        grid = iterate(grid)
        i += 1
        if x := grid_cache.get(str(grid)):
            length = i - x
            i += (n - i) // length * length
        else:
            grid_cache[str(grid)] = i

    return grid.total_load()


if __name__ == "__main__":
    with open("data/14.txt") as f:
        data = f.read()
    assert part_1(EXAMPLE) == 136
    print(f"{part_1(data) = }")  # 105461

    assert part_2(EXAMPLE) == 64
    print(f"{part_2(data) = }")  # 105461

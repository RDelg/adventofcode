import re
from typing import NamedTuple

EXAMPLE = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


class Engine(NamedTuple):
    grid: list[list[str]]
    numbers: list[list[int]]
    numbers_pos: list[list[tuple[int, int]]]

    @property
    def width(self) -> int:
        return len(self.grid[0])

    @property
    def height(self) -> int:
        return len(self.grid)

    @property
    def gears(self) -> list[tuple[int, int]]:
        return [
            (x, y)
            for y, row in enumerate(self.grid)
            for x, cell in enumerate(row)
            if cell == "*"
        ]

    def get_grid_neighbours(self, x: int, y: int) -> list[str]:
        # print(self.grid[y][x])
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                if 0 <= x + i < self.width and 0 <= y + j < self.height:
                    neighbours.append(self.grid[y + j][x + i])
        return neighbours

    def part_numbers_sum(self) -> int:
        # print(self.get_grid_neighbours(x=2, 0))
        value = 0
        for i, numbers in enumerate(self.numbers_pos):
            for j, pos in enumerate(numbers):
                neighbours = set()
                # print(pos[0], pos[1])
                for k in range(pos[0], pos[1]):
                    # print(i, j, k, self.get_grid_neighbours(k, i))
                    #     print(i, j, self.get_grid_neighbours(i, k))
                    neighbours.update(
                        [
                            x
                            for x in self.get_grid_neighbours(k, i)
                            if not x.isnumeric() and x != "."
                        ]
                    )

                if len(neighbours):
                    value += self.numbers[i][j]
                    # self.numbers[i][j] = sum(map(int, neighbours))
        return value

    def gear_ratio(self) -> int:
        # print(self.get_grid_neighbours(x=2, 0))
        value = 0
        print(self.gears)
        return value


def parse(data: str) -> Engine:
    grid = [list(x) for x in data.splitlines()]
    numbers_pos = [
        [(m.start(0), m.end(0)) for m in re.finditer(r"\d+", x)]
        for x in data.splitlines()
    ]
    numbers = [
        [int("".join(grid[i][r[0] : r[1]])) for r in numbers]
        for i, numbers in enumerate(numbers_pos)
    ]
    return Engine(grid=grid, numbers=numbers, numbers_pos=numbers_pos)


def part_1(data: str) -> int:
    grid = parse(data)
    return grid.part_numbers_sum()


def part_2(data: str) -> int:
    grid = parse(data)
    return grid.gear_ratio()


if __name__ == "__main__":
    with open(file="data/03.txt") as f:
        data = f.read()
    assert (part_1(EXAMPLE)) == 4361
    print(f"{part_1(data)=}")

    # assert (part_2(EXAMPLE)) == 30
    print(f"{part_2(EXAMPLE)=}")

from typing import List


RAW = """\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""


class Grid:
    def __init__(self, data: str):
        self.grid = self._parse(data)
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.reset_mask()

    def _parse(self, data: str) -> List[List[int]]:
        return [[int(y) for y in list(x)] for x in data.strip().split("\n")]

    def _get_neighbors(self, x: int, y: int) -> List[int]:
        neighbors = []
        for i in range(max(0, y - 1), min(self.height, y + 2)):
            for j in range(max(0, x - 1), min(self.width, x + 2)):
                if i == y and j == x or self.flashing_mask[i][j]:
                    continue
                neighbors.append((i, j))
        return neighbors

    def maybe_flash_neighbors(self, x: int, y: int) -> None:
        for i, j in self._get_neighbors(x, y):
            if not self.flashing_mask[i][j]:
                self.grid[i][j] += 1
            if self.grid[i][j] > 9 and not self.flashing_mask[i][j]:
                self.flashing_mask[i][j] = True
                self.grid[i][j] = 0
                self.maybe_flash_neighbors(j, i)

    def reset_mask(self) -> None:
        self.flashing_mask = [
            [False for _ in range(self.width)] for _ in range(self.height)
        ]

    def step(self) -> int:
        self.reset_mask()
        for y in range(self.height):
            for x in range(self.width):
                if not self.flashing_mask[y][x]:
                    self.grid[y][x] += 1
                if self.grid[y][x] > 9 and not self.flashing_mask[y][x]:
                    self.flashing_mask[y][x] = True
                    self.grid[y][x] = 0
                    self.maybe_flash_neighbors(x, y)

        return sum(sum(x) for x in self.flashing_mask)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "\n".join(["".join([str(y) for y in x]) for x in g.grid])


if __name__ == "__main__":
    # Data
    with open("data/11.txt", "r") as f:
        data = f.read()

    # Part 1
    # Demo
    g, s = Grid(RAW), 0
    for _ in range(10):
        s += g.step()
    assert s == 204
    # Demo 2
    g, s = Grid(RAW), 0
    for _ in range(100):
        s += g.step()
    assert s == 1656
    # Real
    g, s = Grid(data), 0
    for _ in range(100):
        s += g.step()
    print("Part 1:", s)

    # Part 2
    # Demo
    g, s, n = Grid(RAW), 0, 0
    while True:
        n += 1
        s = g.step()
        if s == (g.width * g.height):
            break
    assert n == 195
    # Real
    g, s, n = Grid(data), 0, 0
    while True:
        n += 1
        s = g.step()
        if s == (g.width * g.height):
            break
    print("Part 2:", n)

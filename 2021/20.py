from typing import List


RAW = """\
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""


class Image:
    @classmethod
    def from_str(cls, data: str) -> "Image":
        sequence, image = data.strip().split("\n\n")
        to_int = lambda x: 1 if x == "#" else 0
        return cls(
            sequence=[to_int(x) for x in sequence],
            image=[[to_int(x) for x in row] for row in image.split("\n")],
        )

    def __init__(self, sequence: List[int], image: List[List[int]]):
        self.sequence = sequence
        self.image = image
        self.m, self.n = len(image), len(image[0])
        self.iterations = 0

    def _get_neighbors(
        self, i: int, j: int, filler: int, n: int = 3
    ) -> List[int]:
        neighbors = []
        middle = n // 2
        for k1 in range(-middle, middle + 1):
            for k2 in range(-middle, middle + 1):
                if 0 <= (x := i + k1) < self.m and 0 <= (y := j + k2) < self.n:
                    neighbors.append(self.image[x][y])
                else:
                    neighbors.append(filler)
        return neighbors

    def enhancement(self) -> "Image":
        self.iterations += 1
        new_image = [[0 for _ in range(self.n + 2)] for _ in range(self.m + 2)]

        filler = 1 if self.sequence[0] == 1 and not self.iterations % 2 else 0
        for i in range(-1, self.m + 1):
            for j in range(-1, self.n + 1):
                neighbors = self._get_neighbors(
                    i,
                    j,
                    filler=filler,
                )
                new_image[i + 1][j + 1] = self.sequence[
                    int("".join(map(str, neighbors)), 2)
                ]
        self.image = new_image
        self.m, self.n = len(new_image), len(new_image[0])
        return self

    def n_ones(self) -> int:
        return sum(sum(row) for row in self.image)

    def __str__(self) -> str:
        return (
            "\n".join(["".join(map(str, row)) for row in self.image])
            .replace("1", "#")
            .replace("0", ".")
        )


if __name__ == "__main__":
    # Data
    with open("data/20.txt") as f:
        data = f.read()

    # Demo
    image = Image.from_str(RAW)
    # Part 1
    image.enhancement()
    image.enhancement()
    assert image.n_ones() == 35
    # Part 2
    for _ in range(50 - 2):
        image.enhancement()
    assert image.n_ones() == 3351

    # Real
    image = Image.from_str(data)
    image.enhancement()
    image.enhancement()
    print("Part 1:", image.n_ones())
    for _ in range(50 - 2):
        image.enhancement()
    print("Part 2:", image.n_ones())

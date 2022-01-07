from typing import List


RAW = """\
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..## #..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.### .######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#. .#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#..... .#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.. ...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#..... ..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

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

    def _get_neighbors(self, i: int, j: int, n: int = 3) -> List[int]:
        neighbors = []
        middle = n // 2
        for k1 in range(-middle, middle + 1):
            for k2 in range(-middle, middle + 1):
                if 0 <= (x := i + k1) < self.m and 0 <= (y := j + k2) < self.n:
                    neighbors.append(self.image[x][y])
                else:
                    neighbors.append(0)
        return neighbors

    def enhancement(self) -> "Image":
        self.iterations += 1
        new_image = [[0 for _ in range(self.n + 2)] for _ in range(self.m + 2)]

        for i in range(-1, self.m + 1):
            for j in range(-1, self.n + 1):
                neighbors = self._get_neighbors(i, j)
                new_image[i + 1][j + 1] = self.sequence[
                    int("".join(map(str, neighbors)), 2)
                ]
                # print(
                #     i,
                #     j,
                #     "".join(map(str, neighbors)),
                #     int("".join(map(str, neighbors)), 2),
                #     new_image[i + 1][j + 1],
                # )
        self.image = new_image
        self.m, self.n = len(new_image), len(new_image[0])
        return self

    def n_ones(self) -> int:
        return sum(sum(row) for row in self.image)

    def __str__(self) -> str:
        return "\n".join(["".join(map(str, row)) for row in self.image])


if __name__ == "__main__":
    with open("data/20.txt") as f:
        data = f.read()

    image = Image.from_str(RAW)
    image.enhancement()
    image.enhancement()
    print(image.m, image.n)
    print(image.n_ones())
    # print(image)
    # # print(image._get_neighbors(1, 3))
    # image.enhancement()
    # print(image)
    # print(image.n_ones())
    # print(image._get_neighbors(-1, -1))

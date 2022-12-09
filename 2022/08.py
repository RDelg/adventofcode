import enum
from dataclasses import dataclass


EXAMPLE = """\
30373
25512
65332
33549
35390"""


class Directions(int, enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()


@dataclass
class Forest:
    n: int
    m: int
    trees: list[list[int]]
    height_from_tree: dict[Directions, tuple[int, int] | None] = None

    @classmethod
    def from_quadcopter(cls, data: str) -> "Forest":
        lines = data.splitlines()
        trees = [[int(line) for line in x] for x in lines]
        n, m = len(lines), len(lines[0])
        height_from_tree = [
            [
                {
                    Directions.UP: None,
                    Directions.DOWN: None,
                    Directions.LEFT: None,
                    Directions.RIGHT: None,
                }
                for _ in range(m)
            ]
            for _ in range(n)
        ]
        return cls(n, m, trees, height_from_tree)

    def __getitem__(self, key: tuple[int, int]) -> int:
        return self.trees[key[0]][key[1]]

    def towards_up_height_from_point(self, i: int, j: int) -> list[int]:
        return [tree[j] for tree in self.trees[:i]][::-1]

    def get_down_height_from_point(self, i: int, j: int) -> list[int]:
        return [tree[j] for tree in self.trees[i + 1 :]]

    def get_left_height_from_point(self, i: int, j: int) -> list[int]:
        return self.trees[i][:j][::-1]

    def get_right_height_from_point(self, i: int, j: int) -> list[int]:
        return self.trees[i][j + 1 :]

    def is_visible(self, i: int, j: int, direction: Directions) -> bool:
        if direction == Directions.UP:
            return self.trees[i][j] > max(self.towards_up_height_from_point(i, j))
        elif direction == Directions.DOWN:
            return self.trees[i][j] > max(self.get_down_height_from_point(i, j))
        elif direction == Directions.LEFT:
            return self.trees[i][j] > max(self.get_left_height_from_point(i, j))
        elif direction == Directions.RIGHT:
            return self.trees[i][j] > max(self.get_right_height_from_point(i, j))
        else:
            raise ValueError("Invalid direction")

    def space(self, i: int, j: int) -> int:
        fist_equal_or_higher = lambda x: x[1] >= self.trees[i][j]
        distance = lambda x: next(
            filter(fist_equal_or_higher, enumerate(x, 1)), (len(x), None)
        )[0]
        up = self.towards_up_height_from_point(i, j)
        down = self.get_down_height_from_point(i, j)
        left = self.get_left_height_from_point(i, j)
        right = self.get_right_height_from_point(i, j)
        return distance(up) * distance(down) * distance(left) * distance(right)


def part_1(data: str) -> int:
    forest = Forest.from_quadcopter(data)
    return (
        sum(
            sum(
                1
                for j in range(1, forest.m - 1)
                if forest.is_visible(i, j, Directions.UP)
                or forest.is_visible(i, j, Directions.DOWN)
                or forest.is_visible(i, j, Directions.LEFT)
                or forest.is_visible(i, j, Directions.RIGHT)
            )
            for i in range(1, forest.n - 1)
        )
        + (forest.n + forest.m) * 2
        - 4
    )


def part_2(data: str) -> int:
    forest = Forest.from_quadcopter(data)
    return max(
        [
            forest.space(i, j)
            for i in range(1, forest.n - 1)
            for j in range(1, forest.m - 1)
        ]
    )


if __name__ == "__main__":
    # data
    with open("data/08.txt") as f:
        data = f.read()
    # part 1
    assert part_1(EXAMPLE) == 21
    print(f"Part 1:\n{part_1(data)}")
    # part 2
    assert part_2(EXAMPLE) == 8
    print(f"Part 2: {part_2(data)}")

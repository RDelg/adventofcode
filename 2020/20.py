import operator
from typing import List
from itertools import accumulate


class Tile:
    def __init__(self, str_data: str):
        str_data = str_data.split(":\n")
        self.id = str_data[0].split(" ")[1]
        self.data = str_data[1].split("\n")
        self._get_borders()

    def _get_borders(self):
        self.up = self.data[0]
        self.down = self.data[-1]
        self.left = "".join([x[0] for x in self.data])
        self.right = "".join([x[-1] for x in self.data])
        assert len(self.up) == len(self.down)
        assert len(self.left) == len(self.right)
        self.shape = (len(self.up), len(self.left))

    def rotate_90(self):
        self.data = [
            "".join([self.data[j][i] for j in reversed(range(self.shape[0]))])
            for i in range(self.shape[1])
        ]
        self._get_borders()

    def flip_v(self):
        self.data = self.data[::-1]
        self._get_borders()

    def __repr__(self) -> str:
        return "\n".join(self.data)


with open("data/20.txt", "r") as file:
    data = file.read().split("\n\n")
tiles_bag = [Tile(x) for x in data]


def find_context(tiles_bag, tile):
    right = []
    left = []
    up = []
    down = []
    for t in tiles_bag:
        for _ in range(2):
            for _ in range(4):
                if tile.right == t.left:
                    right.append(t)
                elif tile.left == t.right:
                    left.append(t)
                elif tile.up == t.down:
                    up.append(t)
                elif tile.down == t.up:
                    down.append(t)
                t.rotate_90()
            t.flip_v()
    assert len(right) <= 1
    assert len(left) <= 1
    assert len(up) <= 1
    assert len(down) <= 1
    return right, left, up, down


corners = []
for tile in tiles_bag:
    right, left, up, down = find_context(tiles_bag, tile)
    if len(right) + len(left) + len(up) + len(down) == 2:
        corners.append(tile)

print([x.id for x in corners])
print(list(accumulate([int(x.id) for x in corners], operator.mul))[-1])


class Image:
    def __init__(self, tiles: List[Tile]):
        tile = tiles[0]
        self.image = [[tile]]
        self.shape = (1, 1)
        self.set_context(0, 0)

    def extend_right(self):
        for i in range(self.shape[0]):
            self.image[i].append(None)
        self.shape = (self.shape[0], self.shape[1] + 1)

    def extend_left(self):
        for i in range(self.shape[0]):
            self.image[i].insert(0, None)
        self.shape = (self.shape[0], self.shape[1] + 1)

    def extend_up(self):
        self.image.insert(0, [None] * self.shape[1])
        self.shape = (self.shape[0] + 1, self.shape[1])

    def extend_down(self):
        self.image.append([None] * self.shape[1])
        self.shape = (self.shape[0] + 1, self.shape[1])

    def set_context(self, x, y):
        assert 0 <= x < self.shape[0]
        assert 0 <= y < self.shape[1]
        right = left = up = down = "|"
        tile = self.image[x][y]
        for t in tiles_bag:
            found = False
            for _ in range(2):
                for _ in range(4):
                    if tile.right == t.left:
                        right = t
                        found = True
                        break
                    elif tile.left == t.right:
                        left = t
                        found = True
                        break
                    elif tile.up == t.down:
                        up = t
                        found = True
                        break
                    elif tile.down == t.up:
                        down = t
                        found = True
                        break
                    else:
                        t.rotate_90()
                if found:
                    break
                t.flip_v()

        x, y = self.extend(x, y)
        self.image[x][y + 1] = right
        self.image[x][y - 1] = left
        self.image[x - 1][y] = up
        self.image[x + 1][y] = down

    def extend(self, x, y):
        if y + 1 >= self.shape[1]:
            self.extend_right()
        if y - 1 < 0:
            self.extend_left()
            y += 1
        if x + 1 >= self.shape[0]:
            self.extend_down()
        if x - 1 < 0:
            self.extend_up()
            x += 1
        return x, y

    def get_context(self, x, y):
        assert 0 <= x < self.shape[0]
        assert 0 <= y < self.shape[1]
        right = left = up = down = None
        if y < self.shape[1] - 1 and (c := self.image[x][y + 1]) is not None:
            right = c
        if y > 0 and (c := self.image[x][y - 1]) is not None:
            left = c
        if x > 0 and (c := self.image[x - 1][y]) is not None:
            up = c
        if x < self.shape[0] - 1 and (c := self.image[x + 1][y]) is not None:
            down = c

        return right, left, up, down

    def fill_image(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if self.image[i][j] is None:
                    right, left, up, down = self.get_context(i, j)
                    if isinstance(right, Tile):
                        self.set_context(i, j + 1)
                    elif isinstance(left, Tile):
                        self.set_context(i, j - 1)
                    elif isinstance(up, Tile):
                        self.set_context(i - 1, j)
                    elif isinstance(down, Tile):
                        self.set_context(i + 1, j)

    def __repr__(self) -> str:
        r = []
        for i in range(self.shape[0]):
            r.append(
                " ".join(
                    [
                        x.id if isinstance(x, Tile) else "None" if x is None else x
                        for x in self.image[i]
                    ]
                )
            )
        return "\n".join(r)


x = Image(tiles_bag)
for _ in range(1000):
    x.fill_image()
print(x)
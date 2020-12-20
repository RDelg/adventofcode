from itertools import accumulate
import operator


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

print(corners)
print(list(accumulate([int(x.id) for x in corners], operator.mul))[-1])
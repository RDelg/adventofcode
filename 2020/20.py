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


with open("data/20_test.txt", "r") as file:
    data = file.read().split("\n\n")

x = Tile(data[0])
print(x, "\n")

x.rotate_90()
print(x, "\n")

x.flip_v()
print(x, "\n")
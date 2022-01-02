from collections import defaultdict
from typing import Iterator, List, NamedTuple


RAW = """\
--- scanner 0 ---
-1,-1,1
-2,-2,2
-3,-3,3
-2,-3,1
5,6,-4
8,0,7
"""


class Point3D(NamedTuple):
    x: int
    y: int
    z: int


class Scanner:
    @classmethod
    def from_str(cls, data: str) -> "Scanner":
        data = data.strip().splitlines()
        header, points = data[0], [Point3D(*map(int, x.split(","))) for x in data[1:]]
        return cls(id=int(header.split(" ")[-2]), points=points)

    @classmethod
    def from_copy(cls, scanner: "Scanner") -> "Scanner":
        return cls(id=scanner.id, points=scanner.points)

    def __init__(self, id: str, points: List[Point3D]):
        self.id = id
        self.points = points

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"--- scanner {self.id} ---\n" + "\n".join(
            [f"{p.x},{p.y},{p.z}" for p in self.points]
        )

    def rotate_x_90(self) -> "Scanner":
        self.points = [Point3D(p.x, -p.z, p.y) for p in self.points]
        return self

    def rotate_y_90(self) -> "Scanner":
        self.points = [Point3D(p.z, p.y, -p.x) for p in self.points]
        return self

    def rotate_z_90(self) -> "Scanner":
        self.points = [Point3D(-p.y, p.x, p.z) for p in self.points]
        return self

    # https://stackoverflow.com/a/58471362
    def rotations(self) -> Iterator["Scanner"]:
        for roll_index in range(6):
            yield self.rotate_x_90()
            for turn_index in range(3):
                yield self.rotate_y_90() if roll_index % 2 == 0 else self.rotate_z_90()


if __name__ == "__main__":

    s = Scanner.from_str(RAW)
    rotations = [Scanner.from_copy(rot) for rot in s.rotations()]
    # for rot in rotations:
    #     print(rot)
    d = defaultdict(lambda: 0)
    for rot in rotations:
        print(rot)
        d[str(rot)] += 1

    for k, v in d.items():
        print(v)

# print(max(d.values()))
# print(unique(rotations))

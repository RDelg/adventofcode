from itertools import product
from typing import List, Tuple

RAW = """\
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
"""


class Cube:
    @classmethod
    def from_str(cls, s: str) -> "Cube":
        points = [
            tuple(sorted(map(int, x.split("=")[1].split("..")))) for x in s.split(",")
        ]
        x, y, z = tuple([p[0] for p in points])
        w, h, d = tuple([p[1] - p[0] for p in points])
        return cls(x, y, z, w, h, d)

    def __init__(self, x: int, y: int, z: int, w: int, h: int, d: int):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.d = d

    def __str__(self):
        return "Cube(x={}, y={}, z={}, w={}, h={}, d={})".format(
            self.x, self.y, self.z, self.w, self.h, self.d
        )

    def __repr__(self):
        return self.__str__()

    def is_overlap(self, other: "Cube") -> bool:
        return (
            self.x <= other.x + other.w
            and self.x + self.w >= other.x
            and self.y <= other.y + other.h
            and self.y + self.h >= other.y
            and self.z <= other.z + other.d
            and self.z + self.d >= other.z
        )

    def is_contained(self, other: "Cube") -> bool:
        return (
            self.x >= other.x
            and self.y >= other.y
            and self.z >= other.z
            and self.x + self.w <= other.x + other.w
            and self.y + self.h <= other.y + other.h
            and self.z + self.d <= other.z + other.d
        )

    def overlap(self, other: "Cube") -> "Cube":
        return Cube(
            (x := max(self.x, other.x)),
            (y := max(self.y, other.y)),
            (z := max(self.z, other.z)),
            min(self.x + self.w, other.x + other.w) - x,
            min(self.y + self.h, other.y + other.h) - y,
            min(self.z + self.d, other.z + other.d) - z,
        )

    @staticmethod
    def _sort(cubes: List["Cube"]) -> List["Cube"]:
        return sorted(cubes, key=lambda c: min(c.x, c.y, c.z))

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z, self.w, self.h, self.d))

    def __eq__(self, other: "Cube") -> bool:
        return hash(self) == hash(other)

    def __add__(self, other: "Cube") -> List["Cube"]:
        if self.is_contained(other):
            return [other]
        elif other.is_contained(self):
            return [self]
        elif self.is_overlap(other):
            result = []
            cubes = self._sort([self, other])
            for i, j, k in product([0, 1], repeat=3):
                c = Cube(
                    cubes[i].x,
                    cubes[j].y,
                    cubes[k].z,
                    cubes[i - 1].x - cubes[i].x + cubes[i - 1].w * i,
                    cubes[j - 1].y - cubes[j].y + cubes[j - 1].h * j,
                    cubes[k - 1].z - cubes[k].z + cubes[k - 1].d * k,
                )
                if c.w > 0 and c.h > 0 and c.d > 0:
                    result.append(c)
            overlap = self.overlap(other)
            cubes = [overlap, cubes[-1]]
            for i, j, k in product([0, 1], repeat=3):
                c = Cube(
                    cubes[0].x + cubes[i].w * (i == 0),
                    cubes[0].y + cubes[j].h * (j == 0),
                    cubes[0].z + cubes[k].d * (k == 0),
                    cubes[i - 1].w - cubes[0].w * (i == 0),
                    cubes[j - 1].h - cubes[0].h * (j == 0),
                    cubes[k - 1].d - cubes[0].d * (k == 0),
                )
                if c.w > 0 and c.h > 0 and c.d > 0:
                    result.append(c)

            return list(set(result))
        else:
            return [self, other]

    def __sub__(self, other: "Cube") -> List["Cube"]:
        if self.is_contained(other):
            return []
        elif other.is_contained(self):
            return [
                Cube(
                    self.x, self.y, self.z, self.w, other.y - self.y, other.z - self.z
                ),
                Cube(
                    self.x,
                    other.y + other.h,
                    other.z + other.d,
                    self.w,
                    self.y + self.h - other.y - other.h,
                    self.z + self.d - other.z - other.d,
                ),
                Cube(self.x, other.y, other.z, other.x - self.x, other.h, other.d),
                Cube(
                    other.x + other.w,
                    other.y,
                    other.z,
                    self.x + self.w - other.x - other.w,
                    other.y,
                    other.z,
                ),
            ]
        elif self.is_overlap(other):
            cubes = self._sort([self, other])
            overlap = self.overlap(other)
            self_idx = cubes.index(self)
            result = []
            if self_idx:
                cubes = [overlap, cubes[-1]]
                for i, j, k in product([0, 1], repeat=3):
                    c = Cube(
                        cubes[0].x + cubes[i].w * (i == 0),
                        cubes[0].y + cubes[j].h * (j == 0),
                        cubes[0].z + cubes[k].d * (k == 0),
                        cubes[i - 1].w - cubes[0].w * (i == 0),
                        cubes[j - 1].h - cubes[0].h * (j == 0),
                        cubes[k - 1].d - cubes[0].d * (k == 0),
                    )
                    if c != overlap and c.w > 0 and c.h > 0 and c.d > 0:
                        result.append(c)
            else:
                for i, j, k in product([0, 1], repeat=3):
                    c = Cube(
                        cubes[i].x,
                        cubes[j].y,
                        cubes[k].z,
                        cubes[i - 1].x - cubes[i].x + cubes[i - 1].w * i,
                        cubes[j - 1].y - cubes[j].y + cubes[j - 1].h * j,
                        cubes[k - 1].z - cubes[k].z + cubes[k - 1].d * k,
                    )
                    if c != overlap and c.w > 0 and c.h > 0 and c.d > 0:
                        result.append(c)
            return result
        else:
            return [self]

    @property
    def volume(self) -> int:
        return self.w * self.h * self.d


def parse(s: str) -> List[Tuple[str, Cube]]:
    return [
        ((x := s.split(" "))[0], Cube.from_str(x[1])) for s in RAW.strip().split("\n")
    ]


def part_1(cubes: List[Tuple[str, Cube]]) -> int:
    new_cubes = [cubes.pop(0)[1]]
    for action, cube in cubes:
        p = max(abs(cube.x), abs(cube.y), abs(cube.z))
        if p > 50:
            print(f"passing {cube}")
            continue
        else:
            if action == "on":
                new_cubes = list(set([c2 for c in new_cubes for c2 in (c + cube)]))
            elif action == "off":
                new_cubes = list(set([c2 for c in new_cubes for c2 in (c - cube)]))
            else:
                raise ValueError(f"unknown action {action}")
    return sum(c.volume for c in new_cubes)


if __name__ == "__main__":
    cubes = parse(RAW)
    print(part_1(cubes))

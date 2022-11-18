from dataclasses import dataclass
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
        return (self.w + 1) * (self.h + 1) * (self.d + 1)


def parse(data: str) -> List[Tuple[str, Cube]]:
    return [
        ((x := s.split(" "))[0], Cube.from_str(x[1])) for s in data.strip().split("\n")
    ]






if __name__ == "__main__":
    # Data
    with open("data/22.txt") as f:
        data = f.read()
    # Part 1
    # Demo
    # cubes = parse(RAW)
    # print(cubes[0][1] + cubes[0][1])

    @dataclass
    class Segment:
        start: int
        end: int

        def __add__(self, other: "Segment") -> List["Segment"]:
            if self.is_overlap(other):
                return [Segment(min(self.start, other.start), max(self.end, other.end))]
            else:
                return [self, other]
        
        def __sub__(self, other: "Segment") -> List["Segment"]:
            if self.is_overlap(other):
                result = []
                if (x:=Segment(self.start, other.start - 1)).is_valid():
                    result.append(x)
                if (x:=Segment(other.end + 1, self.end)).is_valid():
                    result.append(x)
                return result
            else:
                return [self]
            
        def __contains__(self, item: int) -> bool:
            return self.start <= item <= self.end

        def is_overlap(self, other: "Segment") -> bool:
            return self.start <= other.start <= self.end or self.start <= other.end <= self.end
        
        def __repr__(self) -> str:
            return f"Segment({self.start}, {self.end})"
        
        def is_valid(self) -> bool:
            return self.start <= self.end
        
        def max_distance_from_origin(self) -> int:
            return max(abs(self.start), abs(self.end))
        
    @dataclass
    class Square:
        x: Segment
        y: Segment
        
        def __add__(self, other: "Square") -> List["Square"]:
            if self.is_overlap(other):
                return [Square(self.x + other.x, self.y + other.y)]
            else:
                return [self, other]
        
        def __sub__(self, other: "Square") -> List["Square"]:
            if self.is_overlap(other):
                result = []
                for x in self.x - other.x:
                    for y in self.y - other.y:
                        result.append(Square(x, y))
                return result
            else:
                return [self]
        
        def __repr__(self) -> str:
            return f"Square({self.x}, {self.y})"
        
        def is_overlap(self, other: "Square") -> bool:
            return self.x.is_overlap(other.x) and self.y.is_overlap(other.y)
        
        def is_valid(self) -> bool:
            return self.x.is_valid() and self.y.is_valid()
        
        def volume(self) -> int:
            return (self.x.end - self.x.start + 1) * (self.y.end - self.y.start + 1)
        
    
    # print(Square(Segment(0, 10), Segment(0, 10)) - Square(Segment(2, 4), Segment(2, 4)))
    
    @dataclass
    class Cube:
        x: Segment
        y: Segment
        z: Segment
        
        def __add__(self, other: "Cube") -> List["Cube"]:
            # if self.is_overlap(other):
            #     return [Cube(self.x + other.x, self.y + other.y, self.z + other.z)]
            if self.is_overlap(other):
                result = []
                for x in self.x + other.x:
                    for y in self.y + other.y:
                        for z in self.z + other.z:
                            result.append(Cube(x, y, z))
                return result
            else:
                return [self, other]
        
        def __sub__(self, other: "Cube") -> List["Cube"]:
            if self.is_overlap(other):
                result = []
                for x in self.x - other.x:
                    for y in self.y - other.y:
                        for z in self.z - other.z:
                            result.append(Cube(x, y, z))
                return result
            else:
                return [self]
        
        def __repr__(self) -> str:
            return f"Cube({self.x}, {self.y}, {self.z})"
        
        def is_overlap(self, other: "Cube") -> bool:
            return self.x.is_overlap(other.x) and self.y.is_overlap(other.y) and self.z.is_overlap(other.z)
        
        def is_valid(self) -> bool:
            return self.x.is_valid() and self.y.is_valid() and self.z.is_valid()
        
        def volume(self) -> int:
            return (self.x.end - self.x.start + 1) * (self.y.end - self.y.start + 1) * (self.z.end - self.z.start + 1)
            
        @classmethod
        def from_str(cls, s: str) -> "Cube":
            x, y, z = s.split(",")
            return Cube(
                Segment(int((xx:=x.split("=")[1].split(".."))[0]), int(xx[1])),
                Segment(int((yy:=y.split("=")[1].split(".."))[0]), int(yy[1])),
                Segment(int((zz:=z.split("=")[1].split(".."))[0]), int(zz[1])),
            )
        
        def max_distance_from_origin(self) -> int:
            return max(self.x.max_distance_from_origin(), self.y.max_distance_from_origin(), self.z.max_distance_from_origin())

        def overlap_volume(self, other: "Cube") -> int:
            if self.is_overlap(other):
                return (self.x.end - max(self.x.start, other.x.start) + 1) * (self.y.end - max(self.y.start, other.y.start) + 1) * (self.z.end - max(self.z.start, other.z.start) + 1)
            else:
                return 0
            
    
    class Space:
        def __init__(self, cubes: list[Cube]) -> None:
            self._volume = 0
            self._cubes = cubes
            self._added_cubes = []
            for cube in cubes:
                self._add_volume(cube)
        
        def _add_volume(self, cube: Cube) -> None:
            if self._volume == 0:
                self._volume = cube.volume()
                self._added_cubes.append(cube)
            else:
                new_cubes = [cube]
                for c in self._added_cubes:
                    new_cubes = [item for sublist in [n - c for n in new_cubes] for item in sublist] #[item for sublist in new_result for item in sublist]
                self._added_cubes.append(cube)
                self._volume += sum([c.volume() for c in new_cubes])
        
        @property
        def volume(self) -> int:
            return self._volume

    
    def parse(data: str) -> List[Tuple[str, Cube]]:
        return [
            ((x := s.split(" "))[0], Cube.from_str(x[1])) for s in data.strip().split("\n")
        ]

    def solution(data: str) -> int:
        cubes = parse(data)
        result = [cubes.pop(0)[1]]
        for action, cube in cubes:
            p = cube.max_distance_from_origin()
            if p > 50:
                print(f"passing {cube}")
                continue
            else:
                if action == "on":
                    new_result = [r + cube for r in result]    
                elif action == "off":
                    new_result = [r - cube for r in result]
                else:
                    raise ValueError(f"unknown action {action}")
                result = [item for sublist in new_result for item in sublist]
        s = Space(result)
        print(s.volume)
        
        return 

    solution(RAW)
    

    # s = r[0].volume()
    # for i in range(1, len(r)):
    #     l = []
    #     for j in range(i):
    #         l.


    # print(parse(RAW)[0][1] + parse(RAW)[0][1])

    # assert part_1(cubes)[0] == 590784
#     # Real
#     cubes = parse(data)
#     print("Part 1:", part_1(cubes)[0])

#     RAW = """\
# on x=-0..4,y=0..4,z=0..4
# off x=1..2,y=1..2,z=1..2
# """
#     cubes = parse(RAW)[:2]
#     print(cubes)
#     print(part_1(cubes))

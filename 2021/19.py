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

RAW_2 = """\
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
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
        self.aligned = False
        self.reference = None
        self.pos = None

    def align(self, reference: "Scanner", pos: Point3D) -> None:
        self.reference = reference
        self.pos = pos
        self.aligned = True

    def __iter__(self) -> Iterator[Point3D]:
        return iter(self.points)

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

    def move(self, x: int, y: int, z: int) -> "Scanner":
        self.points = [Point3D(p.x - x, p.y - y, p.z - z) for p in self.points]
        return self

    def matches(self, other: "Scanner") -> int:
        return len(set(self.points) & set(other.points))


def load_scanners(data: str) -> List[Scanner]:
    return [Scanner.from_str(x) for x in data.strip().split("\n\n")]


class Map:
    def __init__(self, scanners: List[Scanner], extra_border: int = 100):
        max_range = self._maximum_range(scanners)
        self.aligned_scanners = [scanners.pop()]
        self.remaining_scanners = scanners
        self.max_range = max_range + extra_border
        self.align_scanners()

    @staticmethod
    def _maximum_range(scanners: List[Scanner]) -> int:
        return max(
            [
                max([max(abs(p.x), abs(p.y), abs(p.z)) for p in s.points])
                for s in scanners
            ]
        )

    def align_scanners(self) -> None:
        print(set(self.remaining_scanners[0]))
        print("ASD")
        m = self.remaining_scanners[1].move(-68, -1246, -43)
        for rot in m.rotations():
            print(rot)

        # for i in range(-self.max_range, self.max_range + 1):
        #     for j in range(-self.max_range, self.max_range + 1):
        #         for k in range(-self.max_range, self.max_range + 1):
        #             for rot in self.remaining_scanners[1].rotations():
        #                 if len((x := set(self.remaining_scanners[0]) & set(rot))):
        #                     print("ZXCZXC")

        #             for scanner in self.remaining_scanners:
        #                 scanner.move(i, j, k)


if __name__ == "__main__":
    RAW_0 = """
--- scanner 0 ---
-485,-357,347
"""
    # scanner = Scanner.from_str(RAW_0).move(+68, -1246, -43)
    # # print(scanner)
    # # print("ASDDS")
    # for rot in scanner.rotations():
    #     # print(rot)
    #     a = [int(x) for x in str(rot).split("\n")[-1].split(",")]
    #     # print(a)
    #     if a[0] == 553 and a[1] == 889:
    #         print(a)
    #         asd = Scanner.from_copy(rot)

    # print(asd.matches(scanner))

    # 553,889,-390

    # scanners = load_scanners(RAW_2)
    # m = Map(scanners)

    # s = Scanner.from_str(RAW)
    # rotations = [Scanner.from_copy(rot) for rot in s.rotations()]
    # # for rot in rotations:
    # #     print(rot)
    # d = defaultdict(lambda: 0)
    # for rot in rotations:
    #     print(rot)
    #     d[str(rot)] += 1

    # for k, v in d.items():
    #     print(v)

# print(max(d.values()))
# print(unique(rotations))

from typing import Iterator, List, NamedTuple, Set


RAW = """\
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

    def rotate_x_90(self) -> "Point3D":
        return Point3D(self.x, -self.z, self.y)

    def rotate_y_90(self) -> "Point3D":
        return Point3D(self.z, self.y, -self.x)

    def rotate_z_90(self) -> "Point3D":
        return Point3D(-self.y, self.x, self.z)

    def edist(self, other: "Point3D") -> float:
        return (sum((x - y) ** 2 for x, y in zip(self, other))) ** 0.5


class PointsList:
    def __init__(self, points: List[Point3D]):
        self.points = points

    def rotate_x_90(self) -> "Scanner":
        for i, p in enumerate(self.points):
            self.points[i] = p.rotate_x_90()
        return self

    def rotate_y_90(self) -> "Scanner":
        for i, p in enumerate(self.points):
            self.points[i] = p.rotate_y_90()
        return self

    def rotate_z_90(self) -> "Scanner":
        for i, p in enumerate(self.points):
            self.points[i] = p.rotate_z_90()
        return self

    def __iter__(self) -> Iterator[Point3D]:
        return iter(self.points)

    # https://stackoverflow.com/a/16467849
    def rotations(self) -> Iterator["Scanner"]:
        for cycle in range(2):
            for step in range(3):  # Yield RTTT 3 times
                yield self.rotate_x_90()
                for i in range(3):  #    Yield TTT
                    yield self.rotate_z_90()
            self.rotate_x_90().rotate_z_90().rotate_x_90()  # Do RTR

    def __sub__(self, other: "PointsList") -> "PointsList":
        return PointsList(
            [
                Point3D(a[0] - b[0], a[1] - b[1], a[2] - b[2])
                for a, b in zip(self.points, other.points)
            ]
        )

    # Calculates the pairwise distanse between all points
    def pdist(self):
        return [p1.edist(p2) for p1 in self.points for p2 in self.points if p1 != p2]


class Scanner:
    @classmethod
    def from_str(cls, data: str) -> "Scanner":
        data = data.strip().splitlines()
        header, points = data[0], PointsList(
            [Point3D(*map(int, x.split(","))) for x in data[1:]]
        )
        return cls(id=int(header.split(" ")[-2]), points=points)

    @classmethod
    def from_copy(cls, scanner: "Scanner") -> "Scanner":
        return cls(id=scanner.id, points=scanner.points)

    def __init__(self, id: str, points: PointsList):
        self.id = id
        self.points = points
        self.aligned = False
        self.reference = None
        self.pos = None

    def align(self, reference: "Scanner", pos: Point3D) -> "Scanner":
        self.reference = reference
        self.pos = pos
        self.aligned = True
        return self

    def __iter__(self) -> Iterator[Point3D]:
        return iter(self.points)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"--- scanner {self.id} ---\n" + "\n".join(
            [f"{p.x},{p.y},{p.z}" for p in self.points]
        )

    def rotate_x_90(self) -> "Scanner":
        self.points.rotate_x_90()
        return self

    def rotate_y_90(self) -> "Scanner":
        self.points.rotate_y_90()
        return self

    def rotate_z_90(self) -> "Scanner":
        self.points.rotate_z_90()
        return self

    # https://stackoverflow.com/a/16467849
    def rotations(self) -> Iterator["Scanner"]:
        for cycle in range(2):
            for step in range(3):  # Yield RTTT 3 times
                yield self.rotate_x_90()
                for i in range(3):  #    Yield TTT
                    yield self.rotate_z_90()
            self.rotate_x_90().rotate_z_90().rotate_x_90()  # Do RTR

    def move(self, x: int, y: int, z: int) -> "Scanner":
        self.points = [Point3D(p[0] - x, p[1] - y, p[2] - z) for p in self.points]
        return self

    def matches(self, other: "Scanner") -> Set[float]:
        return set(self.points.pdist()) & set(other.points.pdist())

    def points_from_distances(self, distances: Set[float]) -> PointsList:
        points = list(
            set(
                [
                    point1
                    for point1 in self.points
                    for point2 in self.points
                    if point1.edist(point2) in distances
                ]
            )
        )
        return PointsList(
            sorted(points, key=lambda p: sum([p.edist(p2) for p2 in points]))
        )


def load_scanners(data: str) -> List[Scanner]:
    return [Scanner.from_str(x) for x in data.strip().split("\n\n")]


class Map:
    def __init__(self, scanners: List[Scanner]):
        self.aligned_scanners = [scanners.pop(0).align(None, Point3D(0, 0, 0))]
        self.remaining_scanners = scanners
        self.align_scanners()

    def align_scanners(self) -> None:
        pass


if __name__ == "__main__":
    scanners = load_scanners(RAW)
    distances = scanners[0].matches(scanners[1])
    points_a = scanners[0].points_from_distances(distances)
    points_b = scanners[1].points_from_distances(distances)

    for i, rot in enumerate(points_b.rotations()):
        if len(s := set((points_a - rot).points)) == 1:
            print("rotation: ", i, "offset:", s.pop())

    for i, rot in enumerate(points_a.rotations()):
        if len(s := set((points_b - rot).points)) == 1:
            print("rotation: ", i, "offset:", s.pop())

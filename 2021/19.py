from typing import Iterable, Iterator, List, NamedTuple, Set, Tuple


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

    def euclidean_dist(self, other: "Point3D") -> float:
        return (sum((x - y) ** 2 for x, y in zip(self, other))) ** 0.5

    def manhattan_dist(self, other: "Point3D") -> float:
        return sum(abs(x - y) for x, y in zip(self, other))


def rotations(points: List[Point3D]) -> Iterable[List[Point3D]]:
    # https://stackoverflow.com/a/16467849
    for cycle in range(2):
        for step in range(3):  # Yield RTTT 3 times
            points = [p.rotate_x_90() for p in points]
            yield points
            for i in range(3):  # Yield TTT
                points = [p.rotate_z_90() for p in points]
                yield points
        points = [p.rotate_x_90().rotate_z_90().rotate_x_90() for p in points]  # Do RTR


def sub_list(x: List[Point3D], y: List[Point3D]) -> List[Point3D]:
    return [Point3D(a[0] - b[0], a[1] - b[1], a[2] - b[2]) for a, b in zip(x, y)]


# Calculates the pairwise euclidean distanse between all points
def pdist(points: List[Point3D]) -> List[float]:
    return [p1.euclidean_dist(p2) for p1 in points for p2 in points if p1 != p2]


# Calculates the pairwise manhattan distanse between all points
def manhattan_pdist(points: List[Point3D]) -> List[float]:
    return [p1.manhattan_dist(p2) for p1 in points for p2 in points if p1 != p2]


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

    def align(self, reference: "Scanner", pos: Point3D) -> "Scanner":
        if reference is not None:
            print("ALIGNING", self.id, reference.id, reference.aligned, pos)
        self.reference = reference
        self.move(*pos)
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

    def rotate(self, iters: int) -> "Scanner":
        for _, rot in zip(range(iters), rotations(self.points)):
            pass
        self.points = rot
        return self

    def move(self, x: int, y: int, z: int) -> "Scanner":
        self.points = [Point3D(p[0] + x, p[1] + y, p[2] + z) for p in self.points]
        return self

    def matches(self, other: "Scanner") -> Set[float]:
        return set(pdist(self.points)) & set(pdist(other.points))

    def points_from_distances(self, distances: Set[float]) -> List[Point3D]:
        points = list(
            set(
                [
                    point1
                    for point1 in self.points
                    for point2 in self.points
                    if point1.euclidean_dist(point2) in distances
                ]
            )
        )
        return sorted(
            points, key=lambda p: sum([p.euclidean_dist(p2) for p2 in points])
        )


def load_scanners(data: str) -> List[Scanner]:
    return [Scanner.from_str(x) for x in data.strip().split("\n\n")]


class Map:
    def __init__(self, scanners: List[Scanner]):
        self.aligned_scanners = [scanners.pop(0).align(None, Point3D(0, 0, 0))]
        self.remaining_scanners = scanners
        self.align_scanners()

    def find_rotation(
        self, points_a: List[Point3D], points_b: List[Point3D]
    ) -> Tuple[int, Point3D]:
        for i, rot in enumerate(rotations(points_b)):
            if len(s := set(sub_list(points_a, rot))) == 1:
                offset = s.pop()
                iterations = i
                return iterations + 1, offset
        return None, None

    def align_scanners(self) -> None:
        remaining = len(self.remaining_scanners)
        while remaining > 0:
            for i, scanner in enumerate(self.remaining_scanners):
                for j, reference in enumerate(self.aligned_scanners):
                    if (
                        not scanner.aligned
                        and len(distances := scanner.matches(reference)) == 66
                    ):
                        points_s = scanner.points_from_distances(distances)
                        points_r = reference.points_from_distances(distances)
                        iterations, offset = self.find_rotation(points_r, points_s)
                        self.aligned_scanners.append(
                            scanner.rotate(iters=iterations).align(reference, offset)
                        )
                        remaining -= 1

    def beacons(self) -> List[Point3D]:
        return list(
            set(
                [point for scanner in self.aligned_scanners for point in scanner.points]
            )
        )


if __name__ == "__main__":
    # Data
    with open("data/19.txt") as f:
        data = f.read()

    # Demo
    scanners = load_scanners(RAW)
    m = Map(scanners)
    # Part 1
    assert len(m.beacons()) == 79
    # Part 2
    assert max(manhattan_pdist([s.pos for s in m.aligned_scanners])) == 3621

    # Real
    scanners = load_scanners(data)
    m = Map(scanners)
    print("Part 1:", len(m.beacons()))
    print("Part 2:", max(manhattan_pdist([s.pos for s in m.aligned_scanners])))

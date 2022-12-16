import re
from collections import defaultdict
from dataclasses import dataclass


EXAMPLE = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


@dataclass
class Segment:
    start: int
    end: int

    def __post_init__(self):
        self.start, self.end = sorted([self.start, self.end])

    def overlap(self, other: "Segment") -> bool:
        return (
            self.start <= other.start <= self.end
            or self.start <= other.end <= self.end
            or other.start <= self.start <= other.end
            or other.start <= self.end <= other.end
        )

    def __add__(self, other: "Segment") -> list["Segment"]:
        if self.overlap(other):
            return [Segment(min(self.start, other.start), max(self.end, other.end))]
        return [self, other]

    def __sub__(self, other: "Segment") -> list["Segment"]:
        if self.is_contained(other):
            return []
        if other.is_contained(self):
            return [
                Segment(self.start, other.start - 1),
                Segment(other.end + 1, self.end),
            ]
        if self.overlap(other):
            if self.start < other.start:
                return [Segment(self.start, other.start - 1)]
            return [Segment(other.end + 1, self.end)]

        return [self]

    def is_contained(self, other: "Segment") -> bool:
        return self.start >= other.start and self.end <= other.end

    def isin(self, integer: int) -> bool:
        return self.start <= integer <= self.end


def manhattan_distance(a: complex, b: complex) -> int:
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))


def parse(data: str) -> list[tuple[complex, complex]]:
    digits = re.compile(r"-?\d+")
    sensors = [
        (complex(*(y := list(map(int, digits.findall(x))))[:2]), complex(*y[2:]))
        for x in data.split("\n")
    ]
    return sensors


def part_1(data: str, line: int) -> int:
    sensors = parse(data)
    space = defaultdict(list)
    for i, (sensor, beacon) in enumerate(sensors):
        print("Sensor", i)
        distance = manhattan_distance(sensor, beacon)
        x, y = int(sensor.real), int(sensor.imag)
        rows_away = abs(y - line)
        for z in range(x - distance, x + distance + 1):
            if rows_away <= distance:
                space[z].append(
                    Segment(
                        y - (distance - abs(z - x)),
                        y + (distance - abs(z - x)),
                    ),
                )

    not_availables = sum(
        [any([seg.isin(line) for seg in segments]) for segments in space.values()]
    )
    beacons_in_line = len(
        set([beacon for _, beacon in sensors if int(beacon.imag) == line])
    )

    return not_availables - beacons_in_line


def part_2(data: str, max_line: int) -> int:
    sensors = parse(data)
    space = defaultdict(list)
    for i, (sensor, beacon) in enumerate(sensors):
        print("Sensor", i)
        distance = manhattan_distance(sensor, beacon)
        x, y = int(sensor.real), int(sensor.imag)
        for z in range(x - distance, x + distance + 1):
            space[z].append(
                Segment(
                    y - (distance - abs(z - x)),
                    y + (distance - abs(z - x)),
                ),
            )

    available = {x: [Segment(0, max_line)] for x in space.keys() if 0 <= x <= max_line}
    for x, _ in available.items():
        for seg in space[x]:
            new_segments = []
            for segment in available[x]:
                new_segments += segment - seg
            available[x] = new_segments
    for x, segments in available.items():
        for seg in segments:
            if (
                0 <= seg.start <= max_line
                and seg.end - seg.start == 0
                and 0 <= x <= max_line
            ):
                print(
                    f"Sensor at x={x}, y={seg.start} "
                    + " Frequency:"
                    + str((x) * 4_000_000 + seg.start)
                )

    return 0


if __name__ == "__main__":
    # data
    with open("data/15.txt", "r") as f:
        data = f.read()

    # part 1
    assert part_1(EXAMPLE, 10) == 26
    print(f"Part 1: {part_1(data, 2_000_000)}")
    # part 2
    print(f"Part 2: {part_2(data, 4_000_000)}")

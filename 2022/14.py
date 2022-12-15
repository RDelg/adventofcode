from dataclasses import dataclass


EXAMPLE = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


@dataclass
class Segment:
    start: complex
    end: complex


class Cave:
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    segments: list[Segment]
    space: dict[complex, str]
    sand_source: complex

    def __init__(
        self,
        segments: list[Segment],
        sand_source: complex,
        add_floor: bool = False,
    ):
        self.segments = segments
        self.sand_source = sand_source
        self.add_floor = add_floor
        self.x_max = int(max(max(s.start.real, s.end.real) for s in segments))
        self.x_min = int(min(min(s.start.real, s.end.real) for s in segments))
        self.y_max = int(max(max(s.start.imag, s.end.imag) for s in segments))
        self.y_min = 0
        self.space = {
            complex(x, y): "."
            for y in range(self.y_min, self.y_max + 1)
            for x in range(self.x_min, self.x_max + 1)
        }
        self.space[sand_source] = "+"
        for s in segments:
            self._add_segment(s)

    def _add_segment(self, segment: Segment) -> None:
        start = segment.start
        end = segment.end
        x1, y1 = int(start.real), int(start.imag)
        x2, y2 = int(end.real), int(end.imag)
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])
        if x1 == x2:
            for y in range(y1, y2 + 1):
                self.space[complex(x1, y)] = "#"
        else:
            for x in range(x1, x2 + 1):
                self.space[complex(x, y1)] = "#"

    def is_blocked(self, point: complex) -> bool:
        if self.add_floor:
            return (
                point.imag >= self.y_max + 2
                or self.space.get(point, ".") == "#"
                or self.space.get(point, ".") == "o"
            )

        return self.space[point] == "#" or self.space[point] == "o"

    def drop_sand(
        self,
        drop: complex | None = None,
    ) -> complex | None:
        if drop is not None and self.space.get(drop, None) == "o":
            print("ASD")
            return None
        drop = self.sand_source if drop is None else drop
        if not self.add_floor and (
            drop.imag >= self.y_max
            or drop.real <= self.x_min
            or drop.real >= self.x_max
        ):
            return None
        move = self.get_move(drop)
        if move is not None:
            return self.drop_sand(drop + move)
        self.space[drop] = "o"
        return drop

    def get_move(self, point: complex) -> complex | None:
        return (
            y[0]
            if len(
                y := [
                    x
                    for x in [0 + +1j, -1 + 1j, 1 + 1j]
                    if not self.is_blocked(point + x)
                ]
            )
            else None
        )

    def _translate(self, point: complex) -> complex:
        return point - complex(self.x_min, self.y_min)

    def __repr__(self):
        xs = [int(x.real) for x in self.space.keys()]
        ys = [int(x.imag) for x in self.space.keys()]
        xmin = min(xs)
        xmax = max(xs)
        ymin = min(ys)
        ymax = max(ys)
        return "\n".join(
            "".join(self.space.get(complex(x, y), ".") for x in range(xmin, xmax + 1))
            for y in range(ymin, ymax + 1)
        )


def parse_segments(data: str) -> list[Segment]:
    segments = [x.split(" -> ") for x in data.split("\n")]
    segments = [[complex(*tuple(map(int, x.split(",")))) for x in s] for s in segments]
    segments = [[Segment(v, s[i]) for i, v in enumerate(s[:-1], 1)] for s in segments]
    return [item for sublist in segments for item in sublist]


def part_1(data: str) -> int:
    SOURCE = 500 + 0j
    segments = parse_segments(data)
    cave = Cave(segments, SOURCE)
    i = 0
    for i in range(10_000):
        if cave.drop_sand() is None:
            break

    return i


def part_2(data: str) -> int:
    SOURCE = 500 + 0j
    segments = parse_segments(data)
    cave = Cave(segments, SOURCE, add_floor=True)
    i = 0
    for i in range(100_000):
        if (x := cave.drop_sand()) is not None and x == SOURCE:
            break
    return i + 1


if __name__ == "__main__":
    # data
    with open("data/14.txt", "r") as f:
        data = f.read()

    # part 1
    assert part_1(EXAMPLE) == 24
    print("Part  1:", part_1(EXAMPLE))
    # part 2
    assert part_2(EXAMPLE) == 93
    print("Part  2:", part_2(data))

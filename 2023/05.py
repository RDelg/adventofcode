from itertools import chain
from typing import NamedTuple

EXAMPLE = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


class Range(NamedTuple):
    start: int
    length: int

    @property
    def end(self) -> int:
        return self.start + self.length

    def __contains__(self, item: int) -> bool:
        return self.start <= item < self.end

    def __repr__(self) -> str:
        return f"Range(start={self.start}, length={self.length})"


class Mapper(NamedTuple):
    name: str
    mappers: list[tuple[Range, Range]]

    def map(self, value: int) -> int:
        for input_range, output_range in self.mappers:
            if value in input_range:
                # print(f"{i}: {self.name}: {value=} {input_range=} {output_range=}")
                return output_range.start + value - input_range.start
        return value

    @classmethod
    def from_str(cls, data: str) -> "Mapper":
        name, ranges = data.split(":")
        ranges = [
            (Range((x := list(map(int, r.split())))[1], x[2]), Range(x[0], x[2]))
            for r in ranges.strip().split("\n")
        ]

        return cls(name=name, mappers=ranges)


class Farm(NamedTuple):
    mappers: list[Mapper]

    def map(self, value: int) -> int:
        for mapper in self.mappers:
            value = mapper.map(value)
        return value

    @classmethod
    def from_list(cls, data: list[str]) -> "Farm":
        return cls(mappers=[Mapper.from_str(x) for x in data])


def parse(data: str) -> tuple[list[int], Farm]:
    parsed = data.split("\n\n")
    seeds = list(map(int, parsed[0].split()[1:]))
    farm = Farm.from_list(parsed[1:])
    return seeds, farm


def part_1(data: str) -> int:
    seeds, farm = parse(data)
    locations = [farm.map(x) for x in seeds]
    return min(locations)


def part_2(data: str) -> int:
    seeds, farm = parse(data)
    # TODO
    # return min(locations)


if __name__ == "__main__":
    with open(file="data/05.txt") as f:
        data = f.read()
    assert (part_1(EXAMPLE)) == 35
    print(f"{part_1(data) = }")

    assert (part_2(EXAMPLE)) == 46
    print(f"{part_2(EXAMPLE) = }")

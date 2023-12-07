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
56 93 48"""


class Mapper(NamedTuple):
    a: int
    b: int
    delta: int


def parse(data: str) -> tuple[list[int], list[list[Mapper]]]:
    parsed = data.split("\n\n")
    seeds = list(map(int, parsed[0].split()[1:]))
    mappers = [
        [
            (Mapper((y := list(map(int, r.split())))[0], y[1], y[2]))
            for r in x.split("\n")[1:]
        ]
        for x in parsed[1:]
    ]
    return seeds, mappers


def farm(
    seeds: list[tuple[int, int]], mappers: list[list[Mapper]]
) -> list[tuple[int, int]]:
    for intervals in mappers:
        images = list()
        while seeds:
            x, y = seeds.pop()
            for interval in intervals:
                right = interval.b + interval.delta - 1
                if interval.b <= x <= y <= right:
                    images.append(
                        (x - interval.b + interval.a, y - interval.b + interval.a)
                    )
                    break
                if interval.b <= x <= right < y:
                    seeds.extend([(x, right), (right + 1, y)])
                    break
            else:
                images.append((x, y))
        seeds = images
    return seeds


def part_1(data: str) -> int:
    seeds_raw, mappers = parse(data)
    seeds: list[tuple[int, int]] = [
        (seeds_raw[i], seeds_raw[i]) for i in range(len(seeds_raw))
    ]
    seeds = farm(seeds, mappers)
    return min([x[0] for x in seeds])


def part_2(data: str) -> int:
    seeds, mappers = parse(data)
    seeds = [(seeds[i], seeds[i] + seeds[i + 1] - 1) for i in range(0, len(seeds), 2)]
    seeds = farm(seeds, mappers)
    return min([x[0] for x in seeds])


if __name__ == "__main__":
    with open(file="data/05.txt") as f:
        data = f.read()
    assert (part_1(EXAMPLE)) == 35
    print(f"{part_1(data) = }")

    assert (part_2(EXAMPLE)) == 46
    print(f"{part_2(data) = }")

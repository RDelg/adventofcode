from ast import literal_eval
from itertools import zip_longest
from typing import List, Union


EXAMPLE = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


Packet = List[Union["Packet", int]]


def parse(date: str) -> list[tuple[Packet, Packet]]:
    return [
        (literal_eval((y := x.split("\n"))[0]), literal_eval(y[1]))
        for x in date.split("\n\n")
    ]


def are_packets_ordered(packet_1: Packet, packet_2: Packet) -> bool | None:
    for a, b in zip_longest(packet_1, packet_2, fillvalue=None):
        if b is None:
            return False
        if isinstance(a, int) and isinstance(b, int):
            if a == b:
                continue
            return a < b
        elif isinstance(a, list) and isinstance(b, list):
            if (x := are_packets_ordered(a, b)) is not None:
                return x
        elif isinstance(a, list) and isinstance(b, int):
            if (x := are_packets_ordered(a, [b])) is not None:
                return x
        elif isinstance(b, list) and isinstance(a, int):
            if (x := are_packets_ordered([a], b)) is not None:
                return x
    return True


def part_1(data: str) -> int:
    return sum(
        [
            i if are_packets_ordered(packet_1, packet_2) else 0
            for i, (packet_1, packet_2) in enumerate(parse(data), 1)
        ]
    )


def quick_sort(packets: list[Packet]) -> list[Packet]:
    if len(packets) <= 1:
        return packets
    pivot = packets[0]
    left = [x for x in packets[1:] if are_packets_ordered(x, pivot)]
    right = [x for x in packets[1:] if not are_packets_ordered(x, pivot)]
    return quick_sort(left) + [pivot] + quick_sort(right)


def part_2(data: str) -> int:
    A: Packet = [[2]]
    B: Packet = [[6]]
    packets = parse(data)
    flat = [x for y in packets for x in y]
    flat.append(A)
    flat.append(B)
    flat = quick_sort(flat)
    a_pos, b_pos = flat.index(A) + 1, flat.index(B) + 1
    return a_pos * b_pos


if __name__ == "__main__":
    # data
    with open("data/13.txt", "r") as f:
        data = f.read()
    # part 1
    assert part_1(EXAMPLE) == 13
    print("Part  1:", part_1(data))
    # part 2
    assert part_2(EXAMPLE) == 10 * 14
    print("Part  2:", part_2(data))

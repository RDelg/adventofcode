import ast
import re
from typing import List, Tuple

# Test explode
RAW_DEMO_1 = "[[[[[9,8],1],2],3],4]"
RAW_DEMO_2 = "[7,[6,[5,[4,[3,2]]]]]"
RAW_DEMO_3 = "[[6,[5,[4,[3,2]]]],1]"
RAW_DEMO_4 = "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]"
# Test split
RAW_DEMO_5 = "[[[[0,7],4],[15,[0,13]]],[1,1]]"
# Test sum_numbers
RAW_DEMO_6 = """\
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
"""
RAW_DEMO_7 = """\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""


PAIR_REGEXP = re.compile(r"(\[\d+,\d+\])")
BRACKET_REGEXP = re.compile(r"(\[)|(\])")
NUMBER_REGEXP = re.compile(r"(\d+)")


def explode(number: str) -> str:
    pairs: List[Tuple[Tuple[int, int], Tuple[int, int]]] = sorted(
        [
            (x, tuple(map(int, m.group(1)[1:-1].split(","))))
            for m in PAIR_REGEXP.finditer(number)
            if (x := m.span(1)) != (-1, -1)
        ],
        key=lambda x: x[0][0],
    )

    brackets: List[Tuple[int, str]] = [
        (x[0], m.group(idx))
        for idx in range(1, 3)
        for m in BRACKET_REGEXP.finditer(number)
        if (x := m.span(idx)) != (-1, -1)
    ]
    to_int = lambda x: 1 if x == "[" else -1
    pairs_depth = [
        sum([to_int(bracket) for pos, bracket in brackets if pos < span[0]])
        for span, _ in pairs
    ]
    explode_idx = [i for i, depth in enumerate(pairs_depth) if depth >= 4]

    if not len(explode_idx):
        new_number = number
    else:
        span, values = pairs[explode_idx[0]]
        numbers: List[Tuple[Tuple[int, int], int]] = sorted(
            [
                (m.span(idx), int(m.group(idx)))
                for idx in range(1, 2)
                for m in NUMBER_REGEXP.finditer(number)
            ],
            key=lambda x: x[0][0],
        )
        left_numbers = [
            (span2, value) for span2, value in numbers if span2[1] < span[0]
        ]
        left_number = left_numbers[-1] if len(left_numbers) else None
        right_numbers = [
            (span2, value) for span2, value in numbers if span2[0] > span[1]
        ]
        right_number = right_numbers[0] if len(right_numbers) else None

        if left_number is not None:
            new_number = (
                number[: left_number[0][0]]
                + str(left_number[1] + values[0])
                + number[left_number[0][1] : span[0]]
            )
        else:
            new_number = number[: span[0]]

        new_number += "0"

        if right_number is not None:
            new_number += (
                number[span[1] : right_number[0][0]]
                + str(right_number[1] + values[1])
                + number[right_number[0][1] :]
            )
        else:
            new_number += number[span[1] :]

    return new_number


def split(number: str) -> str:
    numbers: List[Tuple[Tuple[int, int], int]] = sorted(
        [
            (m.span(idx), x)
            for idx in range(1, 2)
            for m in NUMBER_REGEXP.finditer(number)
            if (x := int(m.group(idx))) > 9
        ],
        key=lambda x: x[0][0],
    )

    if not len(numbers):
        new_number = number
    else:
        span, value = numbers[0]
        new_number = (
            number[: span[0]]
            + f"[{( x:= value//2)},{1 + x if value%2 else x}]"
            + number[span[1] :]
        )

    return new_number


def sum_numbers(a: str, b: str) -> str:
    return f"[{a},{b}]"


def reduce_number(number: str) -> str:
    while True:
        new_number = explode(number)
        if new_number == number:
            new_number = split(number)
            if new_number == number:
                break
            else:
                number = new_number
        else:
            number = new_number
    return number


def sum_number_list(data: str) -> str:
    data = data.strip().splitlines()
    result = data[0]
    for number in data[1:]:
        result = reduce_number(sum_numbers(result, number))
    return result


def get_sum(data: list, mult: int = 1) -> int:
    LEFT = 3
    RIGHT = 2
    if isinstance(data[0], list) and isinstance(data[1], list):
        return get_sum(data[0], LEFT * mult) + get_sum(data[1], RIGHT * mult)
    elif isinstance(data[0], list):
        return get_sum(data[0], LEFT * mult) + data[1] * (RIGHT * mult)
    elif isinstance(data[1], list):
        return data[0] * (LEFT * mult) + get_sum(data[1], RIGHT * mult)
    else:
        return data[0] * (LEFT * mult) + data[1] * (RIGHT * mult)


def solution_2(data: str) -> int:
    data = data.strip().splitlines()
    values = [
        get_sum(ast.literal_eval(reduce_number(sum_numbers(*pair))))
        for pair in [(a, b) for a in data for b in data if a != b]
    ]
    return max(values)


if __name__ == "__main__":
    # Data
    with open("data/18.txt", "r") as f:
        data = f.read()
    # Part 1
    # Explode
    assert explode(RAW_DEMO_1) == "[[[[0,9],2],3],4]"
    assert explode(RAW_DEMO_2) == "[7,[6,[5,[7,0]]]]"
    assert explode(RAW_DEMO_3) == "[[6,[5,[7,0]]],3]"
    assert explode(RAW_DEMO_4) == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
    assert explode(explode(RAW_DEMO_4)) == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"
    # Split
    assert split(RAW_DEMO_5) == "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"
    assert split(split(RAW_DEMO_5)) == "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"
    # Reduce test
    assert (
        reduce_number(sum_numbers("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]"))
        == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    )
    # Sum test
    assert (
        sum_number_list(RAW_DEMO_6)
    ) == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"
    # Solution 1
    print("Part 1:", get_sum(ast.literal_eval(sum_number_list(data))))

    # Part 2
    # Demo
    assert solution_2(RAW_DEMO_7) == 3993
    print("Part 2:", solution_2(data))

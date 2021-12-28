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
RAW_DEMO = """\
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


EXPLODE_REGEXP = re.compile(r"\[{3}(\[\d,\d\])|(\[\d,\d\])\]{3}")
NUMBER_REGEXP = re.compile(r"(\d+)")


def explode(number: str) -> str:
    explodes: List[Tuple[Tuple[int, int], Tuple[int, int]]] = sorted(
        [
            (x, tuple(map(int, m.group(idx)[1:-1].split(","))))
            for idx in range(1, 3)
            for m in EXPLODE_REGEXP.finditer(number)
            if (x := m.span(idx)) != (-1, -1)
        ],
        key=lambda x: x[0][0],
    )

    numbers: List[Tuple[Tuple[int, int], int]] = sorted(
        [
            (m.span(idx), int(m.group(idx)))
            for idx in range(1, 2)
            for m in NUMBER_REGEXP.finditer(number)
        ],
        key=lambda x: x[0][0],
    )

    if not len(explodes):
        new_number = number
    else:
        span, values = explodes[0]
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
                + ","
            )
        else:
            # TODO: Validate this
            new_number = number[: span[0]]

        new_number += "0"

        if right_number is not None:
            new_number += (
                number[span[1] : right_number[0][0]]
                + str(right_number[1] + values[1])
                + number[right_number[0][1] :]
            )
        else:
            # TODO: Validate this
            new_number += number[span[1] :]

    return new_number


def split(number: str) -> List[str]:
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
    print(number)
    while True:
        new_number = explode(number)
        print("explode", new_number)
        if new_number == number:
            new_number = split(number)
            if new_number == number:
                break
            else:
                number = new_number
            break
        else:
            number = new_number

    return number


if __name__ == "__main__":
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
    # Full test

    print(reduce_number(sum_numbers("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]")))

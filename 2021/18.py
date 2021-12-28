import re
from typing import List, Tuple

RAW_DEMO_1 = "[[[[[9,8],1],2],3],4]"
RAW_DEMO_2 = "[7,[6,[5,[4,[3,2]]]]]"
RAW_DEMO_3 = "[[6,[5,[4,[3,2]]]],1]"
RAW_DEMO_4 = "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]"

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

    numbers: List[Tuple[Tuple[int, int], int]] = [
        (m.span(idx), int(m.group(idx)))
        for idx in range(1, 2)
        for m in NUMBER_REGEXP.finditer(number)
    ]

    if len(explodes):
        span, values = explodes[0]
        left_numbers = sorted(
            [(span2, value) for span2, value in numbers if span2[1] < span[0]],
            key=lambda x: x[0][0],
        )
        left_number = left_numbers[-1] if len(left_numbers) else None
        right_numbers = sorted(
            [(span2, value) for span2, value in numbers if span2[0] > span[1]],
            key=lambda x: x[0][0],
        )
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


if __name__ == "__main__":
    assert explode(RAW_DEMO_1) == "[[[[0,9],2],3],4]"
    assert explode(RAW_DEMO_2) == "[7,[6,[5,[7,0]]]]"
    assert explode(RAW_DEMO_3) == "[[6,[5,[7,0]]],3]"
    assert explode(RAW_DEMO_4) == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
    assert explode(explode(RAW_DEMO_4)) == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"

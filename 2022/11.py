from enum import Enum
import re
from dataclasses import dataclass
from typing import Callable

EXAMPLE = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


class Operation(str, Enum):
    ADD = "+"
    MULTIPLY = "*"


def generate_operator(operation: Operation, value: int | None) -> Callable[[int], int]:
    if operation == Operation.ADD:
        return lambda old: old + (value if value is not None else old)
    elif operation == Operation.MULTIPLY:
        return lambda old: old * (value if value is not None else old)


def generate_test(value: int) -> Callable[[int], bool]:
    return lambda x: x % value == 0


@dataclass
class Monkey:
    id: int
    items: list[int]
    operation: Callable[[int], int]
    test: Callable[[int], bool]
    throw_true: int
    throw_false: int


def parse_monkeys(data: str) -> list[Monkey]:
    monkeys = []
    digits = re.compile(r"\d+")
    for monkey in data.split("\n\n")[:1]:
        lines = monkey.splitlines()

        id = int(digits.findall(lines[0])[0])
        items = list(map(int, digits.findall(lines[1])))
        operation = generate_operator(
            Operation((x := lines[2][23:].strip().split(" "))[0]),
            int(y) if (y := x[1]) != "old" else None,
        )
        test = generate_test(int(digits.findall(lines[3])[0]))
        throw_true = int(digits.findall(lines[4])[0])
        throw_false = int(digits.findall(lines[5])[0])
        monkeys.append(Monkey(id, items, operation, test, throw_true, throw_false))
    return monkeys


def part_1(data: str) -> int:
    monkeys = parse_monkeys(data)
    print(monkeys)
    return 0


if __name__ == "__main__":
    # data
    with open("data/11.txt") as f:
        data = f.read()
    # part 1
    print("part 1:", part_1(EXAMPLE))

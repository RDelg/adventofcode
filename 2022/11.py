import math
import re
from enum import Enum
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


@dataclass
class Monkey:
    id: int
    items: list[int]
    operation: Callable[[int], int]
    divide_by: int
    throw_true: int
    throw_false: int


def parse_monkeys(data: str) -> list[Monkey]:
    monkeys = []
    digits = re.compile(r"\d+")
    for monkey in data.split("\n\n"):
        lines = monkey.splitlines()

        id = int(digits.findall(lines[0])[0])
        items = list(map(int, digits.findall(lines[1])))
        operation = generate_operator(
            Operation((x := lines[2][23:].strip().split(" "))[0]),
            int(y) if (y := x[1]) != "old" else None,
        )
        divide_by = int(digits.findall(lines[3])[0])
        throw_true = int(digits.findall(lines[4])[0])
        throw_false = int(digits.findall(lines[5])[0])
        monkeys.append(Monkey(id, items, operation, divide_by, throw_true, throw_false))
    return monkeys


class KeepAway:
    moves: list[int]

    @classmethod
    def from_str(cls, data: str) -> "KeepAway":
        return cls(parse_monkeys(data))

    def __init__(self, monkeys: list[Monkey], divide: bool = True):
        self.monkeys = monkeys
        self.moves = [0 for _ in self.monkeys]
        self.divide = divide
        self.modulo = self._calculate_modulo()

    def _calculate_modulo(self) -> int:
        return math.prod([x.divide_by for x in self.monkeys])

    def round(self) -> None:
        for monkey in self.monkeys:
            for _ in range(len(monkey.items)):
                if not monkey.items:
                    continue
                value = monkey.items.pop()
                new_value = monkey.operation(value)
                if self.divide:
                    new_value = new_value // 3
                if new_value % monkey.divide_by == 0:
                    self.monkeys[monkey.throw_true].items.append(
                        new_value % self.modulo
                    )
                else:
                    self.monkeys[monkey.throw_false].items.append(
                        new_value % self.modulo
                    )
                self.moves[monkey.id] += 1
        return

    def __repr__(self) -> str:
        return "\n".join(f"{monkey.id}: {monkey.items}" for monkey in self.monkeys)


def calcualte_n_iterations(game: KeepAway, rounds: int) -> int:
    for _ in range(rounds):
        game.round()
    return math.prod(
        [
            x[1]
            for x in sorted(enumerate(game.moves), key=lambda x: x[1], reverse=True)[:2]
        ]
    )


def part_1(data: str) -> int:
    game = KeepAway.from_str(data)
    ROUNDS = 20
    return calcualte_n_iterations(game, ROUNDS)


def part_2(data: str) -> int:
    game = KeepAway.from_str(data)
    game.divide = False
    ROUNDS = 10_000
    return calcualte_n_iterations(game, ROUNDS)


if __name__ == "__main__":
    # data
    with open("data/11.txt") as f:
        data = f.read()
    # part 1
    assert part_1(EXAMPLE) == 10605
    print("part 1:", part_1(EXAMPLE))
    # part 2
    assert part_2(EXAMPLE) == 2713310158
    print("part 2:", part_2(data))

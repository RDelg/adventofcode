from enum import Enum

RAW = """\
A Y
B X
C Z"""


class RockPaperScissors(int, Enum):
    rock = 1
    paper = 2
    scissors = 3

    @classmethod
    def from_abc(cls, char: str) -> "RockPaperScissors":
        if char == "A":
            return cls.rock
        elif char == "B":
            return cls.paper
        elif char == "C":
            return cls.scissors
        else:
            raise ValueError(f"Invalid character: {char}")

    @classmethod
    def from_xyz(cls, char: str) -> "RockPaperScissors":
        if char == "X":
            return cls.rock
        elif char == "Y":
            return cls.paper
        elif char == "Z":
            return cls.scissors
        else:
            raise ValueError(f"Invalid character: {char}")


class Strategy(str, Enum):
    lose = "X"
    draw = "Y"
    win = "Z"


def get_hand_by_strategy(
    strategy: Strategy, contrincant: RockPaperScissors
) -> RockPaperScissors:
    if strategy == Strategy.win:
        if contrincant == RockPaperScissors.rock:
            return RockPaperScissors.paper
        elif contrincant == RockPaperScissors.paper:
            return RockPaperScissors.scissors
        elif contrincant == RockPaperScissors.scissors:
            return RockPaperScissors.rock
        else:
            raise ValueError(f"Invalid contrincant: {contrincant}")
    elif strategy == Strategy.draw:
        return contrincant
    elif strategy == Strategy.lose:
        if contrincant == RockPaperScissors.rock:
            return RockPaperScissors.scissors
        elif contrincant == RockPaperScissors.paper:
            return RockPaperScissors.rock
        elif contrincant == RockPaperScissors.scissors:
            return RockPaperScissors.paper
        else:
            raise ValueError(f"Invalid contrincant: {contrincant}")
    else:
        raise ValueError(f"Invalid strategy: {strategy}")


def get_points_from_round(round: tuple[RockPaperScissors, RockPaperScissors]) -> int:
    contrincant, me = round
    points = me.value
    LOSE, DRAW, WIN = 0, 3, 6
    if contrincant == me:
        points += DRAW
    elif contrincant == RockPaperScissors.rock:
        if me == RockPaperScissors.paper:
            points += WIN
        elif me == RockPaperScissors.scissors:
            points += LOSE
    elif contrincant == RockPaperScissors.paper:
        if me == RockPaperScissors.rock:
            points += LOSE
        elif me == RockPaperScissors.scissors:
            points += WIN
    elif contrincant == RockPaperScissors.scissors:
        if me == RockPaperScissors.rock:
            points += WIN
        elif me == RockPaperScissors.paper:
            points += LOSE
    else:
        raise ValueError(f"Invalid round: {round}")

    return points


def part_1(data: str) -> int:
    rounds: list[tuple[RockPaperScissors, RockPaperScissors]] = [
        (
            RockPaperScissors.from_abc((y := x.split(" "))[0]),
            RockPaperScissors.from_xyz(y[1]),
        )
        for x in data.split("\n")
    ]
    return sum(get_points_from_round(r) for r in rounds)


def part_2(data: str) -> int:
    rounds = [
        (
            (z := RockPaperScissors.from_abc((y := x.split(" "))[0])),
            get_hand_by_strategy(y[1], z),
        )
        for x in data.split("\n")
    ]

    return sum(get_points_from_round(r) for r in rounds)


if __name__ == "__main__":
    # data
    with open("data/02.txt") as f:
        data = f.read()
    # Part 1
    assert part_1(RAW) == 15
    print("Part 1:", part_1(data))
    # Part 2
    assert part_2(RAW) == 12
    print("Part 2:", part_2(data))

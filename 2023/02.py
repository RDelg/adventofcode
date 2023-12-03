from typing import NamedTuple

EXAMPLE = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


class Hand(NamedTuple):
    red: int
    green: int
    blue: int

    @classmethod
    def from_list_of_tuples(cls, s: list[tuple[str, int]]) -> "Hand":
        return cls(
            red=sum([x[1] for x in s if x[0] == "red"]),
            green=sum([x[1] for x in s if x[0] == "green"]),
            blue=sum([x[1] for x in s if x[0] == "blue"]),
        )


class Game(NamedTuple):
    id: int
    hands: list[Hand]


def parse_games(data: str) -> list[Game]:
    return [
        Game(
            int((y := x.split(":"))[0].split(" ")[1]),
            [
                Hand.from_list_of_tuples(
                    [
                        ((yy := xx.strip().split(" "))[1], int(yy[0]))
                        for xx in z.strip().split(",")
                    ]
                )
                for z in y[1].split(";")
            ],
        )
        for x in data.splitlines()
    ]


def part_1(data: str, max_hand: Hand) -> int:
    games = parse_games(data)
    posibble_hands = []
    for game in games:
        posible = True
        for hand in game.hands:
            if (
                hand.red > max_hand.red
                or hand.green > max_hand.green
                or hand.blue > max_hand.blue
            ):
                # print(f"Game {game.id} is invalid")
                posible = False
                break
        if posible:
            posibble_hands.append(game.id)
    return sum(posibble_hands)


def part_2(data: str) -> int:
    games = parse_games(data)

    score = 0
    for game in games:
        min_red = min_green = min_blue = 0
        for hand in game.hands:
            if hand.red > min_red:
                min_red = hand.red
            if hand.green > min_green:
                min_green = hand.green
            if hand.blue > min_blue:
                min_blue = hand.blue
        score += min_red * min_green * min_blue

    return score


if __name__ == "__main__":
    with open(file="data/02.txt") as f:
        data = f.read()
    assert (part_1(EXAMPLE, Hand(red=12, green=13, blue=14))) == 8
    print(f"{part_1(data, Hand(red=12, green=13, blue=14))=}")

    assert (part_2(EXAMPLE)) == 2286
    print(f"{part_2(data)=}")

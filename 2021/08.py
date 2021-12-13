from collections import defaultdict
from typing import Dict, List, Set, Tuple
from typing import NamedTuple


RAW_0 = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"

RAW = """\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""

NUMBER_SEGMENTS = [
    "abcefg",
    "cf",
    "acdeg",
    "acdfg",
    "bcdf",
    "abdfg",
    "abdefg",
    "acf",
    "abcdefg",
    "abcdfg",
]


class Row(NamedTuple):
    p1: List[str]
    p2: List[str]


class NumberTuple(NamedTuple):
    n: int
    set: Set[str]


def parse(raw: str) -> List[Row]:
    return [
        Row((z := y.split(" | "))[0].split(" "), z[1].split(" "))
        for y in raw.strip().split("\n")
    ]


def count_unique(data: List[Row]) -> int:
    count = 0
    for row in data:
        for word in row.p2:
            if len(word) in [2, 4, 3, 7]:
                count += 1
    return count


def group_by_len(segments: Dict[int, Set[str]]) -> Dict[int, NumberTuple]:
    grouped = defaultdict(lambda: [])
    for k, v in segments.items():
        grouped[len(v)].append(NumberTuple(k, v))
    return grouped


def get_known_coded_segment_using_unique_len(
    row: Row, segments: Dict[int, Set[str]]
) -> Tuple[Dict[int, Set[str]], Dict[int, List[NumberTuple]]]:
    grouped = group_by_len(segments)
    uniq = {lenght: v for lenght, v in grouped.items() if len(v) == 1}
    non_uniq = {lenght: v for lenght, v in grouped.items() if lenght not in uniq}
    known = {}
    unknown = {}
    for word in row.p1 + row.p2:
        if (x := len(word)) in uniq and x not in known:
            known[uniq[x][0][0]] = set(word)
        elif x in non_uniq:
            unknown[x] = non_uniq[x]
    return known, unknown


def generate_translation(
    segments: Dict[int, Set[str]],
    known_segments: Dict[int, Set[str]],
    unknown_segments: Dict[int, List[NumberTuple]],
):
    # translator = {}
    # # for n1, code1 in known_segments.items():
    # #     for n2, code2 in known_segments.items():
    # #         if len(diff := code1.difference(code2)) == 1:
    # #             translator[list(diff)[0]] = list(segments[n1].difference(segments[n2]))[
    # #                 0
    # #             ]
    # print(translator)
    guesses = {}
    # Populate it with the known segments
    for key, encoded in sorted(known_segments.items(), key=lambda x: len(x[1])):
        original = segments[key]
        for code in encoded:
            if code not in guesses.keys():
                guesses[code] = original

    # print(guesses)
    # Filter using what is known so far
    for n1 in guesses:
        for n2 in guesses:
            if len(guesses[n1]) > len(guesses[n2]) and n1 != n2:
                new_guess = guesses[n1] - guesses[n2]
                guesses[n1] = (
                    new_guess if len(new_guess) < len(guesses[n1]) else guesses[n1]
                )

    # print(guesses)

    # print(unknown_segments)

    for lenght, numbers in unknown_segments.items():
        print(lenght, numbers)
        for number in numbers:
            print(number)

    # print(guesses)
    # print(original)
    # if guesses.get()
    # print(f"{key} Original {original}\nNew {encoded}")
    # for c in encoded:
    #     print(f"{c}")

    # def guess_check(a: str, b: str) -> bool:
    #     pass

    # # translator = {chr(ord("a") + i): None for i in range(7)}
    # letters = "abcdefg"
    # for a in letters:
    #     if a not in translator:
    #         for b in letters:
    #             if a != b:
    #                 guess_check(a, b)
    #                 # print(a, b)
    # print(base)
    # print(segments)
    # # print(segments)
    # print(encoded_segments)


def decode_by_intersection(row: List[Row]):
    segments = {i: set(x) for i, x in enumerate(NUMBER_SEGMENTS)}
    known_segments, unknown_segments = get_known_coded_segment_using_unique_len(
        row=row, segments=segments
    )
    # print(known_segments)
    # print(unknown_segments)
    print(generate_translation(segments, known_segments, unknown_segments))
    # for k, v in known_segments.items():
    #     print(f"{k} Original {segments[k]}\nNew {v}")

    #     for word in row.p1 + row.p2:
    #         print(word)
    #         for k, v in known_segments.items():
    #             if set(word) == v:
    #                 print("found", k, v, word)


if __name__ == "__main__":

    input_demo_0 = parse(RAW_0)
    # input_demo = parse(RAW)
    # with open("data/08.txt") as f:
    #     input_real = parse(f.read())

    # assert count_unique(input_demo) == 26

    # # Part 1
    # print(f"Part 1: {count_unique(input_real)}")

    # # Part 2
    for row in input_demo_0:
        decode_by_intersection(row)

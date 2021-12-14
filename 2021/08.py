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
) -> Tuple[Dict[int, Set[str]], Dict[int, List[Set[str]]]]:
    grouped = group_by_len(segments)
    uniq = {lenght: v for lenght, v in grouped.items() if len(v) == 1}
    non_uniq = {lenght: v for lenght, v in grouped.items() if lenght not in uniq}
    known = {}
    unknown = defaultdict(lambda: [])
    for word in row.p1:
        if (x := len(word)) in uniq and x not in known:
            known[uniq[x][0][0]] = set(word)
        elif x in non_uniq:
            unknown[x].append(set(word))
    return known, unknown


def generate_translation(
    segments: Dict[int, Set[str]],
    known_segments: Dict[int, Set[str]],
    unknown_segments: Dict[int, List[Set[str]]],
) -> Dict[str, str]:
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

    # Filter using what is known so far
    for n1 in guesses:
        for n2 in guesses:
            new_guess = guesses[n1].difference(guesses[n2])
            if len(new_guess) and new_guess.issubset(guesses[n1]):
                # print("n1", n1, new_guess, len(new_guess))
                guesses[n1] = new_guess
    # print(guesses)
    # print(unknown_segments)

    translator = {
        code: list(guess)[0] for code, guess in guesses.items() if len(guess) == 1
    }
    # print(translator)
    # print(unknown_segments)
    # print(set(x) for x in NUMBER_SEGMENTS])
    grouped = group_by_len(segments)

    # print("*" * 30)
    # for lenght, numbers in known_segments.items():
    #     print(lenght, numbers)
    #     # for number in numbers:
    #     #     print(number)

    # print("*" * 30)
    # print(known_segments)

    def iterate():
        for lenght, encoded_segments in unknown_segments.items():
            for encoded_segment in encoded_segments:
                for guess in grouped[lenght]:
                    # print(guess)
                    for number, segment in known_segments.items():
                        x = encoded_segment.difference(segment).difference(
                            translator.keys()
                        )
                        # print(guess.n, number)
                        if len(x) == 1 and len(x) == len(
                            y := guess.set.difference(segments[number]).difference(
                                translator.values()
                            )
                        ):
                            translator[x.pop()] = y.pop()
                        # print(
                        #     "ASD",
                        #     guess,
                        #     number,
                        #     segment,
                        #     encoded_segment - set(translator.keys()),
                        #     guess.set - segment - set(translator.values()),
                        # )

                        # for number2, segment2 in known_segments.items():
                        #     x = (
                        #         encoded_segment.difference(segment)
                        #         .difference(segment2)
                        #         .difference(translator.keys())
                        #     )
                        #     if len(x) == 1 and len(x) == len(
                        #         y := segments[guess.n]
                        #         .difference(segments[number])
                        #         .difference(segments[number2])
                        #         .difference(translator.values())
                        #     ):
                        #         translator[x.pop()] = y.pop()
                        #     for number3, segment3 in known_segments.items():
                        #         x = (
                        #             encoded_segment.difference(segment)
                        #             .difference(segment2)
                        #             .difference(segment3)
                        #             .difference(translator.keys())
                        #         )
                        #         if len(x) == 1 and len(x) == len(
                        #             y := segments[guess.n]
                        #             .difference(segments[number])
                        #             .difference(segments[number2])
                        #             .difference(segments[number3])
                        #             .difference(translator.values())
                        #         ):
                        #             translator[x.pop()] = y.pop()

    iterate()
    # print(translator)
    # print(guesses)

    def check_translation(x: str, y: str) -> bool:
        new_translator = {**translator, x: y}
        if len(new_translator) == 6:
            a = set("abcdefg").difference(set(new_translator.keys()))
            b = set("abcdefg").difference(set(new_translator.values()))
            new_translator[a.pop()] = b.pop()

        inv_translator = {v: k for k, v in new_translator.items()}
        # print(new_translator)
        # print(inv_translator)

        translate = lambda values, lookup: set(
            [y for x in values if (y := lookup[x]) is not None]
        )

        # print(unknown_segments)
        for lenght, encoded_segments in unknown_segments.items():
            for encoded in encoded_segments:
                decoded = translate(encoded, new_translator)
                for segment in grouped[lenght]:
                    if not len(segment.set.difference(decoded)):
                        break
                for number, segment2 in segments.items():
                    a = encoded - translate(segment2, inv_translator)
                    b = translate(segments[segment.n] - segment2, inv_translator)
                    if a != b:
                        return False
        return True

    # check_translation("a", "f")
    def iterate_2():
        for lenght, encoded_segments in unknown_segments.items():
            for encoded_segment in encoded_segments:
                for guess in grouped[lenght]:
                    for _, segment in segments.items():
                        inv_translator = {v: k for k, v in translator.items()}
                        x = (
                            encoded_segment
                            - set(
                                [
                                    y
                                    for x in segment
                                    if (y := inv_translator.get(x, None)) is not None
                                ]
                            )
                            - set(translator.keys())
                        )

                        y = guess.set - segment - set(translator.values())
                        if len(x) == 1 and len(y) == 1:
                            if check_translation((x := x.pop()), (y := y.pop())):
                                translator[x] = y

    iterate_2()
    return translator


def decode_by_intersection(row: Row) -> int:
    segments = {i: set(x) for i, x in enumerate(NUMBER_SEGMENTS)}
    known_segments, unknown_segments = get_known_coded_segment_using_unique_len(
        row=row, segments=segments
    )

    translate = lambda values, lookup: set([lookup[x] for x in values])

    translator = generate_translation(segments, known_segments, unknown_segments)
    print(len(translator), translator)

    def to_number(segment: Set[str]) -> str:
        for number, segment2 in segments.items():
            if segment == segment2:
                return str(number)
        return None

    return int("".join([to_number(translate(word, translator)) for word in row.p2]))


if __name__ == "__main__":

    input_demo_0 = parse(RAW_0)
    input_demo = parse(RAW)
    # with open("data/08.txt") as f:
    #     input_real = parse(f.read())

    # assert count_unique(input_demo) == 26

    # # Part 1
    # print(f"Part 1: {count_unique(input_real)}")

    # Part 2
    for row in input_demo_0:
        assert decode_by_intersection(row) == 5353

    s = 0
    for row in input_demo:
        print(row)
        s += decode_by_intersection(row)
    print(s)

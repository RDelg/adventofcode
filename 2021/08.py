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
    non_uniq = {
        lenght: v for lenght, v in grouped.items() if lenght not in uniq
    }
    known = {}
    unknown = defaultdict(lambda: [])
    for word in row.p1:
        if (x := len(word)) in uniq and uniq[x][0].n not in known:
            known[uniq[x][0].n] = set(word)
        elif x in non_uniq:
            unknown[x].append(set(word))
    return known, unknown


def generate_translation(
    segments: Dict[int, Set[str]],
    known_segments: Dict[int, Set[str]],
    unknown_segments: Dict[int, List[Set[str]]],
) -> Dict[str, str]:
    guesses = defaultdict(lambda: set())
    # Populate it with the known segments
    for key, encoded in sorted(
        known_segments.items(), key=lambda x: len(x[1])
    ):
        original = segments[key]
        for code in encoded:
            if code not in guesses.keys():
                guesses[code] = original

    # Filter using what is known so far
    for n1 in guesses:
        for n2 in guesses:
            new_guess = guesses[n1].difference(guesses[n2])
            if len(new_guess) and new_guess.issubset(guesses[n1]):
                guesses[n1] = new_guess

    translator = {
        code: list(guess)[0]
        for code, guess in guesses.items()
        if len(guess) == 1
    }
    grouped = group_by_len(segments)

    def iterate():
        for lenght, encoded_segments in unknown_segments.items():
            for encoded_segment in encoded_segments:
                for guess in grouped[lenght]:
                    # print(guess)
                    for number, segment in known_segments.items():
                        x = encoded_segment.difference(segment).difference(
                            translator.keys()
                        )
                        y = guess.set.difference(segments[number]).difference(
                            translator.values()
                        )
                        for a in x:
                            for b in y:
                                guesses[a].add(b)

    iterate()

    all_segments = [y for x in unknown_segments.values() for y in x] + [
        x for x in known_segments.values()
    ]

    translate = lambda values, lookup: set([lookup[x] for x in values])

    for a in guesses["a"]:
        for b in guesses["b"]:
            for c in guesses["c"]:
                for d in guesses["d"]:
                    for e in guesses["e"]:
                        for f in guesses["f"]:
                            for g in guesses["g"]:
                                found = 0
                                for segment in all_segments:
                                    translator = {
                                        "a": a,
                                        "b": b,
                                        "c": c,
                                        "d": d,
                                        "e": e,
                                        "f": f,
                                        "g": g,
                                    }

                                    decoded = translate(segment, translator)
                                    if decoded in segments.values():
                                        found += 1
                                    if found == len(segments):
                                        return translator

    return translator


def decode_by_intersection(row: Row) -> int:
    segments = {i: set(x) for i, x in enumerate(NUMBER_SEGMENTS)}
    (
        known_segments,
        unknown_segments,
    ) = get_known_coded_segment_using_unique_len(row=row, segments=segments)

    translate = lambda values, lookup: set([lookup[x] for x in values])

    translator = generate_translation(
        segments, known_segments, unknown_segments
    )

    def to_number(segment: Set[str]) -> str:
        len_to_int = {2: 1, 4: 4, 3: 7, 7: 8}
        if (x := len_to_int.get(len(segment), None)) is not None:
            return str(x)
        for number, segment2 in segments.items():
            if translate(segment, translator) == segment2:
                return str(number)
        return None

    return int("".join([to_number(word) for word in row.p2]))


if __name__ == "__main__":

    input_demo_0 = parse(RAW_0)
    input_demo = parse(RAW)
    with open("data/08.txt") as f:
        input_real = parse(f.read())

    assert count_unique(input_demo) == 26

    # Part 1
    print(f"Part 1: {count_unique(input_real)}")

    # Part 2
    for row in input_demo_0:
        assert decode_by_intersection(row) == 5353

    s = 0
    for row in input_demo:
        s += (x := decode_by_intersection(row))
    assert s == 61229

    s = 0
    for row in input_real:
        s += (x := decode_by_intersection(row))
    print("Part 2:", s)

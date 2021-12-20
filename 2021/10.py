from typing import List, Tuple


RAW = """\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""

OPEN_TO_CLOSE = {
    "[": "]",
    "(": ")",
    "{": "}",
    "<": ">",
}

ILLEGAL_POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

INCOMPLETE_POINTS = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


# Returns a list of all the points that are open.
# If it finds an illegal point, it is returned as tyhe first value of the tuple
def check_syntax(data: str, verbose=False) -> Tuple[str, List[str]]:
    stack = []
    for c in data:
        if c in OPEN_TO_CLOSE:
            stack.append(c)
        elif not stack or (x := OPEN_TO_CLOSE[stack.pop()]) != c:
            if verbose:
                print(f"Expected {x}, but found {c} instead.")
            return c, None
    return None, stack


def incomplete_points(data: List[str]) -> int:
    incomplete_lines = []
    for line in data:
        if (x := check_syntax(line))[0] is None:
            incomplete_lines.append(x[1])

    close = lambda x: [OPEN_TO_CLOSE[y] for y in x][::-1]

    ss = []
    for line in incomplete_lines:
        line = close(line)
        s_line = 0
        for x in line:
            s_line *= 5
            s_line += INCOMPLETE_POINTS[x]
        ss.append(s_line)

    return sorted(ss)[len(ss) // 2]


if __name__ == "__main__":
    input_raw = RAW.strip().splitlines()
    with open("data/10.txt") as f:
        input_real = f.read().strip().splitlines()

    # Part 1
    # Demo
    s = 0
    for line in input_raw:
        if (x := check_syntax(line, True))[0] is not None:
            s += ILLEGAL_POINTS[x[0]]
    assert s == 26397

    # Real
    s = 0
    for line in input_real:
        if (x := check_syntax(line))[0] is not None:
            s += ILLEGAL_POINTS[x[0]]
    print("\nPart 1:", s)

    # Part 2
    # Demo
    assert incomplete_points(input_raw) == 288957

    # Real
    print("Part 2:", incomplete_points(input_real))

from typing import List

RAW = """\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""

INPUT_DEMO = RAW.strip().split("\n")


def most_common_bit(input: List[str]) -> str:
    lenght = len(input[0])
    c = [0] * lenght
    for e in input:
        for i in range(lenght):
            if e[i] == "1":
                c[i] += 1
    return "".join(["1" if c[i] >= len(input) // 2 else "0" for i in range(lenght)])


def bit_criteria_filtering(
    input: List[str], iteration: int = 0, greater: bool = True
) -> List[str]:
    if len(input) == 1:
        return input
    lenght = len(input)
    s_0 = sum([1 for x in input if x[iteration] == "0"])
    s_1 = lenght - s_0

    if greater:
        v = "1" if s_0 <= s_1 else "0"
    else:
        v = "0" if s_0 <= s_1 else "1"

    return bit_criteria_filtering(
        [x for x in input if x[iteration] == str(v)], iteration + 1, greater=greater
    )


inverse = lambda x: "".join([str(int(not int(y))) for y in x])

result = most_common_bit(INPUT_DEMO)

assert (int(result, 2) * int(inverse(result), 2)) == 198


# Part 1

with open("data/03.txt", "r") as f:
    INPUT = f.read().strip().split("\n")

result = most_common_bit(INPUT)
print(int(result, 2) * int(inverse(result), 2))

# Part 2
assert (
    int(bit_criteria_filtering(INPUT_DEMO)[0], 2)
    * int(bit_criteria_filtering(INPUT_DEMO, greater=0)[0], 2)
    == 230
)

print(
    int(bit_criteria_filtering(INPUT)[0], 2)
    * int(bit_criteria_filtering(INPUT, greater=0)[0], 2)
)

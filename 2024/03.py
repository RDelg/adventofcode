import re

EXAMPLE = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
EXAMPLE2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def part_1(data: str) -> int:
    reg = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    return sum(int(x) * int(y) for x, y in reg.findall(data))


def part_2(data: str) -> int:
    reg = re.compile(r"(mul)\((\d{1,3}),(\d{1,3})\)|(don't|do)\(\)")
    state = "do"
    val = 0
    for mul, a, b, dd in reg.findall(data):
        if mul:
            if state == "do":
                val += int(a) * int(b)
        else:
            state = dd

    return val
    # return sum(int(x) * int(y) for x, y in mul_reg.findall(data))


if __name__ == "__main__":
    # data
    with open("data/03.txt") as f:
        data = f.read()

    # part 1
    assert part_1(EXAMPLE) == 161
    print(f"{part_1(data)= }")

    # part 2
    assert part_2(EXAMPLE2) == 48
    print(f"{part_2(data)= }")

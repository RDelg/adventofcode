RAW_DEMO = """\
199
200
208
210
200
207
240
269
260
263
"""

INPUT_DEMO = RAW_DEMO.strip().split("\n")

with open("./data/01.txt") as f:
    INPUT = f.read().strip().split("\n")


def count_increases(numbers, windows=1):
    count = 0
    for i in range(len(numbers) - windows):
        if int(numbers[i]) < int(numbers[i + windows]):
            count += 1
    return count


# Part 1
assert count_increases(INPUT_DEMO) == 7


print(count_increases(INPUT))

# Part 2
assert count_increases(INPUT_DEMO, 3) == 5
print(count_increases(INPUT, 3))

from collections import defaultdict, OrderedDict

EXAMPLE = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def hash(string: str) -> int:
    value = 0
    for char in string:
        value += ord(char)
        value *= 17
        value %= 256
    return value


def part_1(data: str) -> int:
    words = data.split(",")
    hashes = [hash(word) for word in words]
    return sum(hashes)


def part_2(data: str) -> int:
    words = data.split(",")
    hash_map = defaultdict(OrderedDict)
    for word in words:
        if word.endswith("-"):
            label = word[:-1]
            hash_map[hash(label)].pop(label, None)
        else:
            label, value = word.split("=")
            hash_map[hash(label)][label] = int(value)

    total = 0
    for h, labels in hash_map.items():
        for i, (_, value) in enumerate(labels.items()):
            total += (h + 1) * (i + 1) * value
    return total


if __name__ == "__main__":
    with open("data/15.txt") as f:
        data = f.read()
    assert part_1(EXAMPLE) == 1320
    print(f"{part_1(data) = }")
    assert part_2(EXAMPLE) == 145
    print(f"{part_2(data) = }")

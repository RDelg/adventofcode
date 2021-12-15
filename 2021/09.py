from functools import reduce
from typing import Any, Callable, List, Tuple


RAW_DEMO = """\
2199943210
3987894921
9856789892
8767896789
9899965678
"""


def convolve_function(
    data: List[List[int]],
    fun: Callable,
    patch_size: int = 3,
    init_value: int = None,
) -> List[List[Any]]:
    middle = patch_size // 2
    m, n = len(data), len(data[0])
    result = [[init_value for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            patch = [[init_value for _ in range(patch_size)] for _ in range(patch_size)]
            for k1 in range(-middle, middle + 1):
                for k2 in range(-middle, middle + 1):
                    if 0 <= (x := i + k1) < m and 0 <= (y := j + k2) < n:
                        patch[k1 + middle][k2 + middle] = data[x][y]
            result[i][j] = fun(patch)
    return result


def parse(data: str) -> List[List[int]]:
    return [[int(y) for y in list(x)] for x in data.strip().splitlines()]


def low_point(data: List[List[int]]) -> int:
    up, down, left, right, center = (
        data[0][1],
        data[2][1],
        data[1][0],
        data[1][2],
        data[1][1],
    )
    if center < up and center < down and center < left and center < right:
        return center + 1
    return 0


def dilate(data: List[List[int]], index: Tuple[int, int]) -> List[List[bool]]:
    m, n = len(data), len(data[0])
    mask = [[False for _ in range(n)] for _ in range(m)]
    mask[index[0]][index[1]] = True

    get_neighbors = lambda idx: [
        (x, y)
        for x, y in [
            (idx[0] - 1, idx[1]),
            (idx[0] + 1, idx[1]),
            (idx[0], idx[1] - 1),
            (idx[0], idx[1] + 1),
        ]
        if 0 <= x < m and 0 <= y < n
    ]
    neighbors = get_neighbors(index)

    while len(neighbors) > 0:
        x, y = neighbors.pop()
        if data[x][y] > data[index[0]][index[1]] and data[x][y] != 9 and not mask[x][y]:
            mask[x][y] = True
            neighbors.extend(get_neighbors((x, y)))
    return mask


def get_k_bigger_masks(masks: List[List[bool]], k: int) -> List[List[bool]]:
    return sorted(
        [(sum([sum(x) for x in m]), m) for m in masks], key=lambda x: x[0], reverse=True
    )[:k]


if __name__ == "__main__":
    input_demo = parse(RAW_DEMO)
    with open("data/09.txt") as f:
        input_real = parse(f.read())

    # Part 1
    result_demo = convolve_function(input_demo, low_point, init_value=1000)
    assert sum([sum(x) for x in result_demo]) == 15

    result = convolve_function(input_real, low_point, init_value=1000)
    print("Part 1:", sum([sum(x) for x in result]))

    # Part 2
    # Demo
    indexes = []
    for i in range(len(result_demo)):
        for j in range(len(result_demo[i])):
            if result_demo[i][j] > 0:
                indexes.append((i, j))

    masks = [dilate(input_demo, index) for index in indexes]
    masks = get_k_bigger_masks(masks, 3)
    mult = lambda x, y: x * y
    assert reduce(mult, [x[0] for x in masks]) == 1134

    # Real
    indexes = []
    for i in range(len(result)):
        for j in range(len(result[i])):
            if result[i][j] > 0:
                indexes.append((i, j))

    masks = [dilate(input_real, index) for index in indexes]
    masks = get_k_bigger_masks(masks, 3)
    mult = lambda x, y: x * y
    print("Part 2:", reduce(mult, [x[0] for x in masks]))

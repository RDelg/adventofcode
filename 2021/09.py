from typing import Any, Callable, List


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
    result_init_valie: Any = False,
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
            result[i][j] = fun(i, j, patch)
    return result


def parse(data: str) -> List[List[int]]:
    return [[int(y) for y in list(x)] for x in data.strip().splitlines()]


def low_point(i, j, data: List[List[int]]) -> int:
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


if __name__ == "__main__":
    input_demo = parse(RAW_DEMO)
    with open("data/09.txt") as f:
        input_data = parse(f.read())

    # Part 1
    assert (
        sum([sum(x) for x in convolve_function(input_demo, low_point, init_value=1000)])
        == 15
    )

    print(
        "Part 1:",
        sum(
            [sum(x) for x in convolve_function(input_data, low_point, init_value=1000)]
        ),
    )

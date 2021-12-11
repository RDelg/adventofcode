from typing import Callable, List, Tuple


INPUT = "16,1,2,0,4,2,7,1,2,14"


def histogram(a: List[int]) -> List[int]:
    # it assumes that the values' range is from 0 to max(a) + 1
    hist = [0] * (max(a) + 1)
    for i in a:
        hist[i] += 1
    return hist


def argmin(iterable):
    return min(enumerate(iterable), key=lambda x: x[1])[0]


def find_least_fuel_usage(
    a: List[int], method: Callable[[List[int], int, int], int]
) -> Tuple[int, int]:
    hist = histogram(a)
    costs = []
    for i in range(len(hist)):
        sum_cost = 0
        for j in range(len(hist)):
            sum_cost += (move_cost := method(hist, i, j))
            # print(f"Move from {j} to {i}: {move_cost}")
        costs.append(sum_cost)
    return (x := argmin(costs)), costs[x]


if __name__ == "__main__":
    position_demo = [int(x) for x in INPUT.split(",")]
    with open("data/07.txt") as f:
        position = [int(x) for x in f.read().split(",")]

    # Part 1
    linear_method = lambda h, i, j: abs(i - j) * h[j]

    assert (find_least_fuel_usage(position_demo, linear_method)) == (2, 37)
    print("Part 1:")
    print(find_least_fuel_usage(position, linear_method))

    # Part 2
    quad_method = lambda h, i, j: (x := (abs(i - j))) * (x + 1) // 2 * h[j]
    assert (find_least_fuel_usage(position_demo, quad_method)) == (5, 168)
    print("Part 2:")
    print(find_least_fuel_usage(position, quad_method))

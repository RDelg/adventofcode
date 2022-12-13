from collections import defaultdict
import string


EXAMPLE = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


class Grid:
    def __init__(
        self,
        graph: dict[complex, list[complex]],
        points: dict[complex, int],
        start: complex,
        end: complex,
        starts: list[complex],
    ):
        self.graph = graph
        self.points = points
        self.start = start
        self.end = end
        self.starts = starts

    @classmethod
    def from_string(cls, data: str) -> "Grid":
        points = {}
        graph = defaultdict(list)
        start, starts, end = 0 + 0j, [], 0 + 0j
        for y, line in enumerate(data.splitlines()):
            for x, letter in enumerate(line):
                point = complex(x, y)
                if letter == "S":
                    value = 0
                    start = point
                    starts.append(point)
                elif letter == "a":
                    value = 0
                    starts.append(point)
                elif letter == "E":
                    value = 25
                    end = point
                else:
                    value = string.ascii_lowercase.index(letter)
                points[point] = value

        for point in points:
            for neighbor in [1 + 0j, -1 + 0j, 0 + 1j, 0 - 1j]:
                if (point + neighbor) in points:
                    graph[point].append(point + neighbor)

        return cls(graph, points, start, end, starts)

    def dijkstra(self, source: complex) -> dict[complex, int]:
        Q = list(self.graph.keys())
        dist = {v: float("inf") for v in self.graph}
        dist[source] = 0

        while Q:
            u = min(Q, key=dist.get)  # type: ignore
            Q.remove(u)
            for v in self.graph[u]:
                alt = dist[u] + 1
                if alt < dist[v] and self.points[u] - self.points[v] <= 1:
                    dist[v] = alt
        return dist  # type: ignore


def part_1(data: str) -> int:
    grid = Grid.from_string(data)
    return grid.dijkstra(grid.end)[grid.start]


def part_2(data: str) -> int:
    grid = Grid.from_string(data)
    paths = grid.dijkstra(grid.end)
    return min(paths[s] for s in grid.starts)


if __name__ == "__main__":
    with open("data/12.txt") as f:
        data = f.read()
    # Part 1
    assert part_1(EXAMPLE) == 31
    print("Part 1:", part_1(data))
    # Part 2
    assert part_2(EXAMPLE) == 29
    print("Part 2:", part_2(data))

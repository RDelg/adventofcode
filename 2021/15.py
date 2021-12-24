import sys
from typing import List

RAW_DEMO = """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""


class Graph:
    def __init__(self, data: str) -> None:
        parsed = [[int(y) for y in x] for x in data.strip().split("\n")]
        self.size = (len(parsed), len(parsed[0]))
        self.V = self.size[0] * self.size[1]
        self.build_graph(parsed)

    def build_graph(self, data: List[List[int]]) -> None:
        self.graph = [[0 for _ in range(self.V)] for _ in range(self.V)]

        get_neighbors = lambda i, j: [
            (x, y)
            for x, y in [
                (i - 1, j),
                (i + 1, j),
                (i, j - 1),
                (i, j + 1),
            ]
            if 0 <= x < self.size[0] and 0 <= y < self.size[1]
        ]

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                neighbors = get_neighbors(i, j)
                for ii, jj in neighbors:
                    self.graph[i * self.size[0] + j][ii * self.size[0] + jj] = data[ii][
                        jj
                    ]

    def minDistance(self, dist: List[int], sptSet: List[bool]) -> int:
        min = sys.maxsize
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
        return min_index

    def dijk(self, source: int) -> List[int]:
        dist = [sys.maxsize] * self.V
        dist[source] = 0
        sptSet = [False] * self.V

        for cout in range(self.V):
            u = self.minDistance(dist, sptSet)
            sptSet[u] = True
            for v in range(self.V):
                if (
                    self.graph[u][v] > 0
                    and sptSet[v] == False
                    and dist[v] > dist[u] + self.graph[u][v]
                ):
                    dist[v] = dist[u] + self.graph[u][v]

        return [dist[node] for node in range(self.V)]


if __name__ == "__main__":
    with open("data/15.txt") as f:
        data = f.read()
    # Part 1
    # Demo
    f = Graph(RAW_DEMO)
    assert f.dijk(0)[-1] == 40
    # Real
    f = Graph(data)
    print("Part 1", f.dijk(0)[-1])

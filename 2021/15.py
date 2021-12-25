from typing import List, Optional

import numpy as np
from numba import jit
from scipy.sparse import lil_matrix

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


@jit(nopython=True)
def min_distance_idx(dist: List[int], ignore: List[bool]) -> int:
    min = np.iinfo(np.int32).max
    for v in range(len(dist)):
        if dist[v] < min and not ignore[v]:
            min = dist[v]
            min_index = v
    return min_index


class Graph:
    def __init__(self, data: str, expand_n: Optional[int] = 1) -> None:
        assert expand_n > 0, "expand_n must be greater than 0"
        grid = np.array(
            [[int(y) for y in x] for x in data.strip().split("\n")], dtype=np.int8
        )
        if expand_n > 1:
            grid = self.expand_grid(grid=grid, n=expand_n)
        self.size = (len(grid), len(grid[0]))
        self.V = self.size[0] * self.size[1]
        self.build_graph(grid)

    @staticmethod
    def expand_grid(grid: List[List[int]], n: int) -> List[List[int]]:
        size = (len(grid), len(grid[0]))
        new_grid = np.zeros((size[1] * n, size[0] * n), dtype=np.int8)
        for j in range(size[1] * n):
            for i in range(size[0] * n):
                new_grid[j][i] = (
                    x % 10
                    if (
                        x := (
                            grid[j % size[1]][i % size[0]] + j // size[1] + i // size[0]
                        )
                    )
                    < 10
                    else x % 10 + 1
                )
        return new_grid

    def build_graph(self, data: List[List[int]]) -> None:
        graph = lil_matrix((self.V, self.V), dtype=np.int8)
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
                    graph[i * self.size[0] + j, ii * self.size[0] + jj] = data[ii][jj]
        self.graph = graph.tocsr()

    @staticmethod
    @jit(nopython=True)
    def dijkstra(
        graph: np.ndarray, iis: np.ndarray, jjs: np.ndarray, n: int, src: int
    ) -> np.ndarray:
        dist = np.ones((n,), dtype=np.int32) * np.iinfo(np.int32).max
        dist[src] = 0
        ignore = np.zeros(n, dtype=np.int8)
        for _ in range(n):
            u = min_distance_idx(dist, ignore)
            ignore[u] = True
            for i in range(iis[u], iis[u + 1]):
                if not ignore[jjs[i]] and dist[jjs[i]] > dist[u] + graph[i]:
                    dist[jjs[i]] = dist[u] + graph[i]
        return dist

    def dijk(self, source: int) -> List[int]:
        dist = self.dijkstra(
            self.graph.data,
            self.graph.indptr,
            self.graph.indices,
            self.size[0] ** 2,
            source,
        )
        return [dist[node] for node in range(self.V)]


if __name__ == "__main__":
    with open("data/15.txt") as f:
        data = f.read()
    # Part 1
    # Demo
    f = Graph(RAW_DEMO)
    assert (x := f.dijk(0)[-1]) == 40, f"Part 1 Demo Failed: {x}"
    # Real
    f = Graph(data)
    print("Part 1", f.dijk(0)[-1])
    # Part 2
    # Demo
    f = Graph(RAW_DEMO, expand_n=5)
    assert f.dijk(0)[-1] == 315
    # Real
    f = Graph(data, expand_n=5)
    print("Part 2", f.dijk(0)[-1])

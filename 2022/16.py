import re

EXAMPLE = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


def parse_input(data: str) -> dict[str, tuple[int, list[str]]]:
    uppers = re.compile(r"[A-Z]+")
    return {
        (y := x.split(";"))[0].split(" ")[1]: (
            int(y[0].split("=")[1]),
            uppers.findall(y[1]),
        )
        for x in data.splitlines()
    }


class Graph:
    def __init__(self, data: str):
        self.valves = parse_input(data)
        self.graph, self.values = self.build_graph()

    def build_graph(self) -> tuple[dict[str, list[str]], dict[str, int]]:
        graph = {}
        values = {}
        for valve, (flow, tunnels) in self.valves.items():
            graph[valve] = tunnels
            values[valve] = flow
        return graph, values


def part_1(data: str) -> int:
    g = Graph(data)
    print(g.graph, g.values)
    return 0


if __name__ == "__main__":
    print(part_1(EXAMPLE))

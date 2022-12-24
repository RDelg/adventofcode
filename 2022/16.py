import math
import random
import re
from collections import defaultdict
from typing import NamedTuple

from tqdm import trange

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


class State(NamedTuple):
    current_valve: str
    valves_opened_at: tuple[int, ...]


class StepInfo(NamedTuple):
    done: bool
    state: State
    reward: float


class Graph:
    def __init__(self, data: str):
        self.valves = parse_input(data)
        self.graph, self.values = self._build_graph()

    def _build_graph(self) -> tuple[dict[str, list[str]], dict[str, int]]:
        graph = {}
        values = {}
        for valve, (flow, tunnels) in self.valves.items():
            graph[valve] = tunnels
            values[valve] = flow
        return graph, values


class Environment:
    def __init__(
        self,
        connections: dict[str, list[str]],
        values: dict[str, int],
        max_time: int = 30,
    ):
        self.connections = connections
        self.flow_rate = values
        self.valves = list(connections.keys())
        self.valves_to_idx = {v: i for i, v in enumerate(self.valves)}
        self.n_valves = len(self.valves)
        self.max_time = max_time
        self._max_flow_rate = max(self.flow_rate.values())
        self.reset()

    @classmethod
    def from_graph(cls, graph: Graph):
        return cls(graph.graph, graph.values)

    def reset(self) -> State:
        self.current_valve = "AA"
        self.valves_opened_at = [self.max_time for _ in self.valves]
        self.time = 1
        self._n_valves_with_flow = sum(1 for x in self.flow_rate.values() if x > 0)
        return self.state

    @property
    def state(self) -> State:
        return State(
            self.current_valve,
            tuple(self.valves_opened_at),
        )

    def legal_actions(self, state: State) -> tuple[str]:
        return tuple([x for x in self.connections[state.current_valve]]) + (
            ("open",)
            if state.valves_opened_at[self.valves_to_idx[state.current_valve]]
            == self.max_time
            and self.flow_rate[state.current_valve] > 0
            else tuple()
        )

    def step(self, action: str) -> StepInfo:
        if action == "open":
            x = self.valves_to_idx[self.current_valve]
            self.valves_opened_at[x] = self.time
            self._n_valves_with_flow -= 1
        else:
            self.current_valve = action

        self.time += 1
        reward = (
            -1.0
            if action != "open"
            else (
                (self.flow_rate[self.current_valve] * (self.max_time - self.time))
                / (self._max_flow_rate)
            )
        )
        if self.time == self.max_time:
            reward -= 10
        if self._n_valves_with_flow == 0:
            reward += 10

        return StepInfo(
            self.time == self.max_time or self._n_valves_with_flow == 0,
            self.state,
            reward,
        )


class SarsaLearner:
    def __init__(
        self,
        env: Environment,
        epsilon: float = 0.5,
        gamma: float = 0.9,
        alpha: float = 0.1,
    ):
        self.env = env
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.c = 10
        self.reset()

    def reset(self):
        self.env.reset()
        self.iterations = 0
        self.Q = defaultdict(lambda: 0.0)
        self.Q2 = defaultdict(lambda: 0.0)
        self.action_count = defaultdict(lambda: 0)

    def learn(self, n_episodes: int = 1000):
        for _ in trange(n_episodes):
            self._episode()

    def _episode(self):
        state, done, reward = self.env.reset(), False, 0.0
        while not done:
            action = self._choose_action(self.Q, state, 0.0)
            self.action_count[(state, action)] += 1
            done, next_state, reward = self.env.step(action)
            # double q learning
            # if random.random() < 0.5:
            #     Q = self.Q
            #     target_Q = self.Q2
            # else:
            #     Q = self.Q2
            #     target_Q = self.Q
            # on policy q learning
            # uncomment the following line and comment the above 4 lines
            Q = self.Q
            target_Q = self.Q

            self._update_Q(Q, target_Q, state, action, reward, next_state)
            state = next_state

    def _choose_action(
        self, Q: dict[tuple[State, str], float], state: State, epsilon: float
    ) -> str:
        actions = self.env.legal_actions(state)
        Qs = [
            Q[(state, action)]
            + (
                self.c
                * math.sqrt(
                    math.log(self.iterations + 1)
                    / (self.action_count[(state, action)] + 1e-5)
                )
            )
            for action in actions
        ]
        return (
            random.choice(actions)
            if random.random() < epsilon
            else actions[Qs.index(max(Qs))]
        )

    def _update_Q(
        self,
        Q: dict[tuple[State, str], float],
        target_Q: dict[tuple[State, str], float],
        state: State,
        action: str,
        reward: float,
        next_state: State,
    ):
        next_action = self._choose_action(target_Q, next_state, 0.0)
        # soft decay of alpha based on number of iterations
        # alpha = max(0.01, self.alpha / (1 + self.iterations / 1000))

        # print(alpha)
        x = self.alpha * (
            (reward + self.gamma * Q[(next_state, next_action)]) - Q[(state, action)]
        )
        # print(state, action, x)
        # print(x)
        Q[(state, action)] = Q[(state, action)] + x
        self.iterations += 1


def part_1(data: str, iterations: int = 100_000) -> int:
    g = Graph(data)
    env = Environment.from_graph(g)
    learner = SarsaLearner(env, epsilon=0.3, gamma=0.9, alpha=0.1)
    learner.learn(iterations)
    state, done, _ = env.reset(), False, 0
    while not done:
        action = learner._choose_action(learner.Q, state, epsilon=0.0)
        done, next_state, _ = env.step(action)
        state = next_state
    print(
        sorted(
            [(y, x) for x, y in zip(state.valves_opened_at, env.valves) if x != 30],
            key=lambda x: x[1],
        ),
    )
    return sum(
        [
            ((30 - x) * env.flow_rate[y])
            for x, y in zip(state.valves_opened_at, env.valves)
        ]
    )


if __name__ == "__main__":
    # data
    with open("data/16.txt") as f:
        data = f.read()
    # part 1
    print(part_1(EXAMPLE, 10_000), "should be 1651")  # 1651
    # print(part_1(data, 10_000))  # 1376
    # part 2
    # print(part_2(EXAMPLE))  # 1707

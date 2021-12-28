from dataclasses import dataclass, field
from typing import List, Tuple

from tqdm import tqdm


RAW_DEMK_1 = "target area: x=20..30, y=-10..-5"


@dataclass
class Vec2D:
    x: int
    y: int


sign = lambda x: (1, -1)[x < 0]


@dataclass
class Probe:
    vel: Vec2D
    ace: Vec2D = field(default_factory=lambda: Vec2D(0, -1))
    pos: Vec2D = field(default_factory=lambda: Vec2D(0, 0))
    drag: int = 1

    def step(self) -> "Probe":
        # change position
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        # drag force
        self.vel.x -= (self.drag) * sign(self.vel.x) if self.vel.x else 0
        # change velocity
        self.vel.x += self.ace.x
        self.vel.y += self.ace.y

        return self


@dataclass
class Target:
    a: Vec2D
    b: Vec2D

    @classmethod
    def from_str(cls, s: str) -> "Target":
        x, y = s.split(":")[1].split(", ")
        x = x.split("=")[1].split("..")
        y = y.split("=")[1].split("..")
        return cls(Vec2D(int(x[0]), int(y[0])), Vec2D(int(x[1]), int(y[1])))

    def intersect(self, probe: Probe) -> bool:
        return (self.a.x <= probe.pos.x <= self.b.x) and (
            self.a.y <= probe.pos.y <= self.b.y
        )

    def miss(self, probe: Probe) -> bool:
        return probe.pos.x > self.b.x or probe.pos.y < self.a.y


def get_valocities(target: Target, y_limit: int, iters: int) -> List[Tuple[Vec2D, int]]:
    velocities = []
    for j in tqdm(range(y_limit, -y_limit, -1)):
        for i in range(1, target.b.x + 1):
            p = Probe(vel=Vec2D(i, j))
            for step in range(iters):
                p.step()
                if target.intersect(p):
                    velocities.append((Vec2D(i, j), step))
                    break
                elif target.miss(p):
                    break
    return velocities


def find_max_y_vel(
    target: str, y_limit: int, iters: int = 500
) -> Tuple[Tuple[Vec2D, int], int]:
    return (
        max(
            (x := get_valocities(Target.from_str(target), y_limit, iters)),
            key=lambda x: x[0].y,
        ),
        len(x),
    )


def find_max_y_pos(vel: Vec2D, iters: int = 500) -> int:
    p = Probe(vel=vel)
    return max([p.step().pos.y for _ in range(iters)])


if __name__ == "__main__":
    # Data
    with open("data/17.txt") as f:
        data = f.read().strip()
    # Part 1
    # Demo
    assert find_max_y_vel(RAW_DEMK_1, 100)[0][0].y == 9
    # Real
    (vel, iters), q = find_max_y_vel(data, 1_000, 500)
    p = Probe(vel=vel)
    print("Part 1: ", find_max_y_pos(vel, iters))
    # Part 2
    (vel, iters), q = find_max_y_vel(RAW_DEMK_1, 30, 400)
    assert q == 112
    (vel, iters), q = find_max_y_vel(data, 10_000, 5000)
    print("Part 2:", q)

from collections.abc import Iterator
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Self


type Pair[T] = tuple[T, T]


@dataclass
class Robot:
    origin: Pair[int]
    velocity: Pair[int]
    position: Pair[int] = field(init=False)

    def __post_init__(self):
        self.position = (self.origin[0], self.origin[1])

    @classmethod
    def from_data(cls, data: str) -> Self:
        origin, velocity = data.split()
        x, y = tuple(int(v) for v in origin[2:].split(","))
        origin = (x, y)
        x, y = tuple(int(v) for v in velocity[2:].split(","))
        velocity = (x, y)
        return cls(origin, velocity)

    def move(self, width, height):
        x = self.position[0] + self.velocity[0]
        y = self.position[1] + self.velocity[1]
        x %= width
        y %= height
        self.position = (x, y)


class Puzzle:
    __test__ = {
        "data": [
            """
11 7

p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
            """,
        ],
        "expected": [12],
    }

    def __init__(self, day: int | None = None, part: int | None = None):
        if day is None:
            # d{day:02}p{part}.py
            name = __file__[-8:-3]
            day = int(name[1:3])
            part = int(name[4:5])
        self.day = day
        self.part = part

    def get_data(self, path: str) -> str:
        with open(path) as f:
            return f.read().strip()

    def get_groups(self, data) -> list[list[str]]:
        current_lines = []
        line_groups = [current_lines]
        for line in data.splitlines():
            line = line.strip()
            if len(line) == 0:
                current_lines = []
                line_groups.append(current_lines)
            else:
                current_lines.append(line)
        return line_groups

    def get_lines(self, data: str) -> list[str]:
        groups = self.get_groups(data)
        assert len(groups) == 1
        return groups[0]

    def get_input(self) -> str:
        return self.get_data(f"../io/y2024/input//d{self.day:02}.in")

    def get_test_data(self) -> Iterator[tuple[str, Any]]:
        cfg = self.__test__
        assert len(cfg["data"]) == len(cfg["expected"])
        return zip([data.strip() for data in cfg["data"]], cfg["expected"])

    def print(self, robots: list[Robot], width: int, height: int, quadrant=False):
        grid = []
        for _ in range(height):
            line = []
            for _ in range(width):
                line.append(0)
            grid.append(line)
        for robot in robots:
            grid[robot.position[1]][robot.position[0]] += 1
        if quadrant:
            grid[int(height / 2)] = [" "] * width
            x = int(width / 2)
            for y in range(height):
                grid[y][x] = " "
        print("\n".join("".join("." if p == 0 else str(p) for p in line) for line in grid))

    def solution(self, data: str) -> Any:
        groups = self.get_groups(data)
        lines = groups[-1]
        if len(groups) == 2:
            width, height = groups[0][0].split()
            width = int(width)
            height = int(height)
        else:
            width = 101
            height = 103
        robots = [Robot.from_data(line) for line in lines]
        for _ in range(100):
            for robot in robots:
                robot.move(width, height)
        # self.print(robots, width, height, True)
        mid_width = int(width / 2)
        mid_height = int(height / 2)
        quadrants = [0, 0, 0, 0]
        for robot in robots:
            x = robot.position[0]
            y = robot.position[1]
            if x == mid_width or y == mid_height:
                continue
            if x < mid_width:
                quadrant = 0 if y < mid_height else 2
            else:
                quadrant = 1 if y < mid_height else 3
            quadrants[quadrant] += 1
        safety_factor = quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]
        # print(quadrants)
        return safety_factor

    def solve(self, test: bool | str = True) -> None:
        if isinstance(test, str):
            print(self.solution(test))
            return
        if test:
            for i, (data, expected) in enumerate(self.get_test_data()):
                solution = self.solution(data)
                assert solution == expected, f"[{i}] --- solution != result: {solution} != {expected}"
        print(self.solution(self.get_input()))


if __name__ == "__main__":
    Puzzle().solve()

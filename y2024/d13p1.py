from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any
from typing import Self


@dataclass
class Point:
    x: int
    y: int

    def __repr__(self):
        return f"({self.x}, {self.y})"


@dataclass
class ClawMachine:
    a: Point
    b: Point
    prize: Point

    @classmethod
    def from_data(cls, data: list[str]) -> Self:
        buttons = []
        for line in data[:2]:
            offset = line[len("button n: ") :]
            x, y = offset.split(", ")
            x = int(x[1:])
            y = int(y[1:])
            buttons.append(Point(x, y))
        prize = data[-1][len("prize: ") :]
        x, y = prize.split(", ")
        x = int(x[2:]) + 10000000000000
        y = int(y[2:]) + 10000000000000
        machine = cls(*buttons, Point(x, y))
        return machine

    def __repr__(self):
        return f"{self.prize}, A: {self.a}, B: {self.b}"


class Puzzle:
    __test__ = {
        "data": [
            """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
            """,
        ],
        "expected": [875318608908],
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
        return self.get_data(f"inputs/d{self.day:02}.in")

    def get_test_data(self) -> Iterator[tuple[str, Any]]:
        cfg = self.__test__
        assert len(cfg["data"]) == len(cfg["expected"])
        return zip([data.strip() for data in cfg["data"]], cfg["expected"])

    def solution(self, data: str) -> Any:
        machines = [ClawMachine.from_data(group) for group in self.get_groups(data)]
        total = 0
        for machine in machines:
            numerator = (machine.a.y * machine.prize.x) - (machine.a.x * machine.prize.y)
            denominator = (machine.a.y * machine.b.x) - (machine.a.x * machine.b.y)
            if numerator % denominator != 0:
                continue
            b = int(numerator / denominator)
            a = int((machine.prize.x - (b * machine.b.x)) / machine.a.x)
            location = Point(a * machine.a.x + b * machine.b.x, a * machine.a.y + b * machine.b.y)
            if location == machine.prize:
                total += a * 3
                total += b
        return total

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

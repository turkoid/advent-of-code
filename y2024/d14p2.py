import os
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any
from typing import Self

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

type Pair[T] = tuple[T, T]


class WrappedSet(set):
    def __repr__(self):
        s = ", ".join(repr(o) for o in self)
        return f"{{{s}}}" if s else ""


@dataclass(frozen=True)
class Robot:
    origin: Pair[int]
    velocity: Pair[int]

    @classmethod
    def from_data(cls, data: str) -> Self:
        origin, velocity = data.split()
        x, y = tuple(int(v) for v in origin[2:].split(","))
        origin = (x, y)
        x, y = tuple(int(v) for v in velocity[2:].split(","))
        velocity = (x, y)
        return cls(origin, velocity)

    def at_seconds(self, seconds, width, height) -> Pair[int]:
        x = (self.origin[0] + self.velocity[0] * seconds) % width
        y = (self.origin[1] + self.velocity[1] * seconds) % height
        return x, y

    def __repr__(self):
        return f"R[{self.origin[0]}, {self.origin[1]}]"


class Puzzle:
    __test__ = {
        "data": [],
        "expected": [],
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

    def print(self, grid: list[list[set[Robot]]], seconds=None, console=True, file=False):
        buffer = []
        for line in grid:
            buffer_line = []
            for robots in line:
                num_robots = len(robots)
                buffer_line.append(str(num_robots) if num_robots else ".")
            buffer.append(buffer_line)
        output = "\n".join("".join(line) for line in buffer)
        if console:
            print(output)
            print("")
        if file and seconds:
            output_dir = "output/d14p2"
            filename = f"{output_dir}/grid{seconds:0>5}.jpg"
            if os.path.exists(filename):
                return
            bg = 20
            fg = 210
            width = 750
            height = 1800
            img = Image.new(mode="RGB", size=(width, height), color=(bg, bg, bg))
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("../resources/JetBrainsMono-Regular.ttf", 12)
            point = (width / 2, height / 2)
            draw.text(point, output, fill=(fg, fg, fg), font=font, anchor="mm")
            img = img.resize((1000, 1000))
            os.makedirs(output_dir, exist_ok=True)
            img.save(filename)

    def find_tree(self, grid: list[list[set[Robot]]], group_min: int = 5, line_min: int = 10):
        num_contiguous = 0
        for row in grid:
            line = "".join("^" if len(robots) >= 1 else " " for robots in row)
            line = line.strip()
            contiguous = line.split()
            if any(len(part) >= group_min for part in contiguous):
                num_contiguous += 1
            if num_contiguous >= line_min:
                return True
        return False

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
        grid = [[WrappedSet() for _ in range(width)] for _ in range(height)]
        robots = []
        seconds = 0
        for line in lines:
            robot = Robot.from_data(line)
            robots.append(robot)
            initial_x, initial_y = robot.at_seconds(seconds, width, height)
            grid[initial_y][initial_x].add(robot)
        # self.print(grid)
        while True:
            seconds += 1
            # print(seconds)
            origin_count = 0
            for robot in robots:
                last_x, last_y = robot.at_seconds(seconds - 1, width, height)
                x, y = robot.at_seconds(seconds, width, height)
                origin_count += 1 if robot.origin == (x, y) else 0
                grid[last_y][last_x].remove(robot)
                grid[y][x].add(robot)
            if origin_count == len(robots):
                print(f"Positions reset @ {seconds} seconds")
                return None
            if self.find_tree(grid):
                self.print(grid, seconds, file=True)
                print(f"Possible tree found @ {seconds} seconds")

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

import importlib.util
import os.path
from typing import Any

type Pair[T] = tuple[T, T]


class Day15Part1:
    def __init__(self, day: int | None = None, part: int | None = None):
        if day is None:
            # d{day:02}p{part}.py
            name = __file__[-8:-3]
            day = int(name[1:3])
            part = int(name[4:5])
        self.day = day
        self.part = part
        year_folder = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        self.year = int(year_folder[1:])

    @property
    def input_dir(self):
        return f"../io/y{self.year}/input"

    @property
    def output_dir(self):
        return f"../io/y{self.year}/output/d{self.day:02}p{self.part}"

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
        return self.get_data(f"{self.input_dir}/d{self.day:02}.in")

    def get_output(self, path: str):
        output_path = f"{self.output_dir}/{path}"
        os.makedirs(output_path, exist_ok=True)
        return output_path

    def get_test_data(self) -> list[tuple[str, Any]]:
        module_path = f"{self.input_dir}/d{self.day:02}.py"
        if not os.path.exists(module_path):
            return []
        spec = importlib.util.spec_from_file_location(f"d{self.day:02}", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        test_data = getattr(module, f"p{self.part}", [])
        test_data = [(raw.strip(), expected) for raw, expected in test_data]
        return test_data

    def print(self, grid):
        print("\n".join("".join(line) for line in grid))

    def solution(self, data: str) -> Any:
        groups = self.get_groups(data)
        grid = []
        robot = None
        for y, line in enumerate(groups[0]):
            row = []
            for x, c in enumerate(line):
                if c == "@":
                    robot = (x, y)
                row.append(c)
            grid.append(row)
        instructions = "".join(groups[1])
        # self.print(grid)
        offsets = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}

        def swap(a, b):
            a_x, a_y = a
            b_x, b_y = b
            grid[a_y][a_x], grid[b_y][b_x] = grid[b_y][b_x], grid[a_y][a_x]

        for move in instructions:
            offset = offsets[move]
            x = robot[0] + offset[0]
            y = robot[1] + offset[1]
            front = grid[y][x]
            if front == "#":
                continue
            if front == ".":
                swap((x, y), robot)
                robot = (x, y)
                continue
            box = (x, y)
            while True:
                x += offset[0]
                y += offset[1]
                if grid[y][x] == ".":
                    swap((x, y), box)
                    swap(box, robot)
                    robot = box
                    break
                if grid[y][x] == "#":
                    break
        # self.print(grid)
        total = 0
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                if c == "O":
                    gps = y * 100 + x
                    total += gps
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
    Day15Part1().solve()

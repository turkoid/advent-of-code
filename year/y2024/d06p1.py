from typing import Any
from typing import TypedDict


class Data(TypedDict):
    data: str
    expected: Any


class Puzzle:
    __test__: Data = {
        "data": """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
    """,
        "expected": 41,
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

    def get_lines(self, data: str) -> list[list[str]]:
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

    def get_input(self) -> str:
        return self.get_data(f"../io/y2024/input//d{self.day:02}.in")

    def get_test_data(self) -> tuple[str, str]:
        data = self.__test__["data"].strip()
        expected = self.__test__["expected"]
        return data, expected

    def get_guard_pos(self, lab: list[list[str]]) -> tuple[int, int, str]:
        for y, line in enumerate(lab):
            for x, c in enumerate(line):
                if c in "<^v>":
                    return x, y, c
        raise ValueError("no guard found")

    def solution(self, data: str) -> Any:
        lab = self.get_lines(data)[0]
        lab = [list(line) for line in lab]
        x, y, direction = self.get_guard_pos(lab)
        lab[y][x] = "X"
        x_size = len(lab[0])
        y_size = len(lab)
        directions = "^>v<"
        instructions = {"v": (0, 1), "^": (0, -1), ">": (1, 0), "<": (-1, 0)}
        visited = 1
        while True:
            orig_x = x
            orig_y = y
            x_offset, y_offset = instructions[direction]
            x += x_offset
            y += y_offset
            if x < 0 or x == x_size or y < 0 or y == y_size:
                break
            upcoming = lab[y][x]
            if upcoming == "#":
                direction = directions[(directions.index(direction) + 1) % 4]
                x = orig_x
                y = orig_y
                continue
            if upcoming == ".":
                visited += 1
            lab[y][x] = "X"
        return visited

    def solve(self, test: bool | str = True) -> None:
        if isinstance(test, str):
            print(self.solution(test))
            return
        if test:
            data, expected = self.get_test_data()
            solution = self.solution(data)
            assert solution == expected, f"solution != result: {solution} != {expected}"
        print(self.solution(self.get_input()))


if __name__ == "__main__":
    Puzzle().solve()

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
        "expected": 6,
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
        return self.get_data(f"../input/y2024//d{self.day:02}.in")

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

    def print(self, lab, guard_x=None, guard_y=None):
        lines = []
        translation = str.maketrans("^<>v", "|--|")
        for y, line in enumerate(lab):
            sb = []
            for x, c in enumerate(line):
                if x == guard_x and y == guard_y:
                    c = "@"
                elif c.startswith("*"):
                    c = c[-1]
                elif c.startswith("+"):
                    c = c[0]
                else:
                    c = c.translate(translation)
                sb.append(c)
            lines.append("".join(sb))
        print("\n".join(lines))
        print("")

    def solution(self, data: str) -> Any:
        lab = self.get_lines(data)[0]
        lab = [list(line) for line in lab]
        x, y, direction = self.get_guard_pos(lab)
        x_size = len(lab[0])
        y_size = len(lab)
        directions = "^>v<"
        lab_prime = None
        x_prime = None
        y_prime = None
        direction_prime = None
        looping_timelines = 0
        instructions = {"v": (0, 1), "^": (0, -1), ">": (1, 0), "<": (-1, 0)}
        lab[y][x] = f"*{direction}"
        while True:
            current_pos = lab[y][x]
            orig_x = x
            orig_y = y
            x_offset, y_offset = instructions[direction]
            x += x_offset
            y += y_offset
            if x < 0 or x == x_size or y < 0 or y == y_size:
                if lab_prime:
                    lab, x, y, direction = lab_prime, x_prime, y_prime, direction_prime
                    lab_prime = None
                    continue
                else:
                    break
            upcoming_pos = lab[y][x]
            if upcoming_pos[-1] == direction:
                looping_timelines += 1
                # print(looping_timelines)
                # self.print(lab, orig_x, orig_y)
                lab, x, y, direction = lab_prime, x_prime, y_prime, direction_prime
                lab_prime = None
            elif upcoming_pos[-1] in "#O":
                direction = directions[(directions.index(direction) + 1) % 4]
                if current_pos[0] == "+" and current_pos[-1] == direction:
                    looping_timelines += 1
                    # print(looping_timelines)
                    # self.print(lab, orig_x, orig_y)
                    lab, x, y, direction = lab_prime, x_prime, y_prime, direction_prime
                    lab_prime = None
                else:
                    x = orig_x
                    y = orig_y
                    if current_pos[0] != "*":
                        lab[y][x] = f"+{direction}"
            elif upcoming_pos[-1] in directions and upcoming_pos[0] != "*":
                lab[y][x] = f"+{upcoming_pos[-1]}"
            elif upcoming_pos[-1] == ".":
                lab[y][x] = direction
                if not lab_prime:
                    lab_prime = [line[:] for line in lab]
                    x_prime = x
                    y_prime = y
                    direction_prime = direction
                    lab[y][x] = "O"
                    x = orig_x
                    y = orig_y

        return looping_timelines

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

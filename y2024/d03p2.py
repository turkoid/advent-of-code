import re
from typing import Any
from typing import TypedDict


class Data(TypedDict):
    data: str
    expected: Any


class Puzzle:
    __test__: Data = {
        "data": "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))",
        "expected": 48,
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

    def get_lines(self, data: str) -> list[str]:
        lines = [line.strip() for line in data.splitlines() if line.strip() and not line.startswith("#")]
        return lines

    def get_input(self) -> str:
        return self.get_data(f"inputs/d{self.day:02}.in")

    def get_test_data(self) -> tuple[str, str]:
        data = self.__test__["data"].strip()
        expected = self.__test__["expected"]
        return data, expected

    def solution(self, data: str) -> Any:
        data = f"do(){data}don't()"
        total = 0
        while "do()" in data:
            group_start = data.index("do()") + 4
            group_end = data.index("don't()", group_start)
            enabled = data[group_start:group_end]
            for match in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)", enabled):
                total += int(match.group(1)) * int(match.group(2))
            data = data[group_end + 7 :]
        return total

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

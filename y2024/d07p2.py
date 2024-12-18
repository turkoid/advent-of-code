from typing import Any
from typing import TypedDict


class Data(TypedDict):
    data: str
    expected: Any


class Puzzle:
    __test__: Data = {
        "data": """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
    """,
        "expected": 11387,
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

    @staticmethod
    def plus(a, b):
        return a + b

    @staticmethod
    def multiply(a, b):
        return a * b

    def solution(self, data: str) -> Any:
        lines = self.get_lines(data)[0]
        total_result = 0
        for line in lines:
            expected, values = line.split(": ")
            expected = int(expected)
            values = [int(v) for v in values.split()]
            equations: list[tuple[list[str], int]] = [([], values[0])]
            while equations:
                ops, result = equations.pop()
                if len(ops) == len(values) - 1:
                    if result == expected:
                        total_result += expected
                        break
                else:
                    value = values[len(ops) + 1]
                    for op in ["||", "+", "*"]:
                        if op == "||":
                            op_result = int(f"{result}{value}")
                        elif op == "+":
                            op_result = result + value
                        else:
                            op_result = result * value
                        if op_result <= expected:
                            new_ops = ops[:]
                            new_ops.append(op)
                            equations.append((new_ops, op_result))
        return total_result

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

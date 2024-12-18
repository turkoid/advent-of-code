from typing import Any
from typing import TypedDict


class Data(TypedDict):
    data: str
    expected: Any


class Puzzle:
    __test__: Data = {
        "data": """
            MMMSXXMASM
            MSAMXMSMSA
            AMXSXMAAMM
            MSAMASMSMX
            XMASAMXAMM
            XXAMMXXAMA
            SMSMSASXSS
            SAXAMASAAA
            MAMMMXMMMM
            MXMXAXMASX
        """,
        "expected": 18,
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
            return f.read()

    def get_lines(self, data: str) -> list[str]:
        lines = [line.strip() for line in data.splitlines() if line.strip() and not line.startswith("#")]
        return lines

    def get_input(self) -> str:
        return self.get_data(f"../io/y2024/input//d{self.day:02}.in")

    def get_test_data(self) -> tuple[str, str]:
        data = self.__test__["data"].strip()
        expected = self.__test__["expected"]
        return data, expected

    def count_xmas(self, line: str) -> int:
        if len(line) < 4:
            return 0
        return line.count("XMAS") + line[::-1].count("XMAS")

    def add_char(self, lines: list[list[str]], index: int, c: str) -> None:
        if index == len(lines):
            lines.append([c])
        else:
            lines[index].append(c)

    def solution(self, data: str) -> Any:
        lines = self.get_lines(data)
        total = 0
        we_lines: list[str] = []
        ns_liens: list[list[str]] = []
        nw_se_lines: list[list[str]] = []
        ne_sw_lines: list[list[str]] = []
        we_len = len(lines[0]) if lines else 0
        for y, line in enumerate(lines):
            we_lines.append(line)
            for x, c in enumerate(line):
                self.add_char(ns_liens, x, c)
                nw_se_index = x - y
                if nw_se_index < 0:
                    nw_se_index = we_len - nw_se_index - 1
                ne_sw_index = x + y
                self.add_char(nw_se_lines, nw_se_index, c)
                self.add_char(ne_sw_lines, ne_sw_index, c)
        for lines in [we_lines, ns_liens, nw_se_lines, ne_sw_lines]:
            for line in lines:
                line = "".join(line)
                total += self.count_xmas(line)
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

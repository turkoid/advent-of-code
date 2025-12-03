from typing import Any
from typing import TypedDict


class Data(TypedDict):
    data: str
    expected: Any


class Day4Part2:
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
        "expected": 9,
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

    def solution(self, data: str) -> Any:
        lines = self.get_lines(data)
        mas_sam = {"MAS", "SAM"}
        count = 0
        for y, line in enumerate(lines[1:-1], start=1):
            for x, c in enumerate(line[1:-1], start=1):
                if c != "A":
                    continue
                nw_se_diag = f"{lines[y - 1][x - 1]}A{lines[y + 1][x + 1]}"
                sw_ne_diag = f"{lines[y + 1][x - 1]}A{lines[y - 1][x + 1]}"
                if nw_se_diag in mas_sam and sw_ne_diag in mas_sam:
                    count += 1
        return count

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
    Day4Part2().solve()

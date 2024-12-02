from typing import Any


class Puzzle:
    def __init__(self, day: int | None = None, part: int | None = None):
        if day is None:
            # d{day:02}p{part}.py
            name = __file__[-8:-3]
            day = int(name[1:3])
            part = int(name[4:5])
        self.day = day
        self.part = part

    def get_lines(self, path: str) -> list[str]:
        with open(path) as f:
            data = f.read()
        lines = [line.strip() for line in data.splitlines() if line.strip()]
        return lines

    def get_input(self) -> list[str]:
        return self.get_lines(f"inputs/d{self.day:02}.in")

    def get_test_data(self) -> tuple[list[str], str]:
        lines = self.get_lines(f"inputs/d{self.day:02}.test")
        result = lines[-1].split()[self.part - 1]
        lines = lines[:-1]
        return lines, result

    def solution(self, lines: list[str]) -> Any:
        safe_reports = 0
        for line in lines:
            levels = [int(lvl) for lvl in line.split()]
            prev_diff = None
            is_safe = True
            for level, next_level in zip(levels[:-1], levels[1:]):
                diff = level - next_level
                if diff == 0 or abs(diff) > 3:
                    is_safe = False
                    break
                if prev_diff and prev_diff * diff < 0:
                    is_safe = False
                    break
                prev_diff = diff
            if is_safe:
                safe_reports += 1
        return safe_reports

    def solve(self, test: bool = True) -> None:
        if test:
            lines, result = self.get_test_data()
            solution = self.solution(lines)
            assert (
                str(solution) == result
            ), f"solution != result: {solution} != {result}"
        print(self.solution(self.get_input()))


if __name__ == "__main__":
    Puzzle().solve()

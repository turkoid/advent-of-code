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

    def get_data(self, path: str) -> str:
        with open(path) as f:
            return f.read()

    def get_lines(self, data: str) -> list[str]:
        lines = [
            line.strip()
            for line in data.splitlines()
            if line.strip() and not line.startswith("#")
        ]
        return lines

    def get_input(self) -> str:
        return self.get_data(f"inputs/d{self.day:02}.in")

    def get_test_data(self) -> tuple[str, str]:
        data = self.get_data(f"inputs/d{self.day:02}.test")
        lines = self.get_lines(data)
        result = lines[-1].split()[self.part - 1]
        data = "\n".join(lines[:-1])
        return data, result

    def solution(self, data: str) -> Any:
        return None

    def solve(self, test: bool | str = True) -> None:
        if isinstance(test, str):
            print(self.solution(test))
            return
        if test:
            data, result = self.get_test_data()
            solution = self.solution(data)
            assert (
                str(solution) == result
            ), f"solution != result: {solution} != {result}"
        print(self.solution(self.get_input()))


if __name__ == "__main__":
    Puzzle().solve()

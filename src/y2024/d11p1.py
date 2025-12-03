from collections.abc import Iterator
from typing import Any


class Day11Part1:
    __test__ = {
        "data": [
            """
*1 0 1 10 99 999
            """,
            """
*6 125 17
            """,
            """
*25 125 17
            """,
        ],
        "expected": [7, 22, 55312],
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
        return self.get_data(f"../io/y2024/input//d{self.day:02}.in")

    def get_test_data(self) -> Iterator[tuple[str, Any]]:
        cfg = self.__test__
        assert len(cfg["data"]) == len(cfg["expected"])
        return zip([data.strip() for data in cfg["data"]], cfg["expected"])

    def print(self, blink, stones):
        stones = " ".join(stones)
        print(f"[{blink}] {stones}")

    def solution(self, data: str) -> Any:
        stones = data.split()
        count = 25
        if stones[0].startswith("*"):
            count = int(stones[0][1:])
            del stones[0]
        # self.print(0, stones)
        for blink in range(count):
            new_stones = []
            for stone in stones:
                if stone == "0":
                    new_stones.append("1")
                elif len(stone) % 2 == 0:
                    split_point = int(len(stone) / 2)
                    for split_stone in [stone[:split_point], stone[split_point:]]:
                        new_stones.append(str(int(split_stone)))
                else:
                    new_stones.append(str(int(stone) * 2024))
            stones = new_stones
            # self.print(blink, stones)
        return len(stones)

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
    Day11Part1().solve()

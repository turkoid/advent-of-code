from typing import Any
from typing import TypedDict


class Data(TypedDict):
    data: str
    expected: Any


class Day5Part1:
    __test__: Data = {
        "data": """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
    """,
        "expected": 143,
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
            if line.startswith("#"):
                continue
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

    def is_correct_order(self, update: list[int], rules: set[tuple[int, int]]) -> bool:
        for i, page in enumerate(update[:-1]):
            for other_page in update[i + 1 :]:
                page_set = (other_page, page)
                if page_set in rules:
                    return False
        return True

    def solution(self, data: str) -> Any:
        line_groups = self.get_lines(data)
        rules = set()
        for line in line_groups[0]:
            a, b = line.split("|")
            rule = (int(a), int(b))
            rules.add(rule)
        updates = [[int(page) for page in line.split(",")] for line in line_groups[1]]
        total = 0
        for update in updates:
            if self.is_correct_order(update, rules):
                middle_page = update[int(len(update) / 2)]
                total += middle_page
        return total

    def solve(self, test: bool | str = True) -> None:
        if isinstance(test, str):
            print(self.solution(test))
            return
        if test:
            data, expected = self.get_test_data()
            if not data or not expected:
                raise ValueError("No test data")
            solution = self.solution(data)
            assert solution == expected, f"solution != result: {solution} != {expected}"
        print(self.solution(self.get_input()))


if __name__ == "__main__":
    Day5Part1().solve()

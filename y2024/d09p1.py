from typing import Any
from typing import TypedDict


class Data(TypedDict):
    data: str
    expected: Any


class Puzzle:
    __test__: Data = {
        "data": """
2333133121414131402
    """,
        "expected": 1928,
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
        return self.get_data(f"../input/y2024//d{self.day:02}.in")

    def get_test_data(self) -> tuple[str, str]:
        data = self.__test__["data"].strip()
        expected = self.__test__["expected"]
        return data, expected

    def print(self, filesystem):
        print("".join(c[0] for c in filesystem))
        print("")

    def checksum(self, filesystem) -> int:
        checksum = 0
        for i, block in enumerate(filesystem):
            block = block[0]
            if block == ".":
                continue
            id = int(block)
            checksum += i * id
        return checksum

    def solution(self, data: str) -> Any:
        filesystem = []
        id = 0
        for i, digit in enumerate(data):
            blocks = int(digit)
            block = str(id) if i % 2 == 0 else "."
            filesystem.extend([(block,) for _ in range(blocks)])
            if block != ".":
                id += 1
        free_space = (".",)
        if free_space not in filesystem:
            return self.checksum(filesystem)
        # self.print(filesystem)
        free_space_pointer = filesystem.index(free_space)
        block_pointer = 0
        while free_space_pointer < len(filesystem) - block_pointer:
            block_pointer += 1
            block = filesystem[-block_pointer]
            if block != free_space:
                filesystem[free_space_pointer], filesystem[-block_pointer] = (
                    block,
                    free_space,
                )
                free_space_pointer = filesystem.index(free_space, free_space_pointer + 1)
        # self.print(filesystem)
        return self.checksum(filesystem)

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

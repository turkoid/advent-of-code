from dataclasses import dataclass
from typing import Any
from typing import TypedDict


class Data(TypedDict):
    data: str
    expected: Any


FREE_SPACE = "."


@dataclass
class File:
    id: str
    size: int
    moved: bool = False

    @property
    def is_free_space(self):
        return self.id == FREE_SPACE

    def __repr__(self):
        return self.id * self.size


class Puzzle:
    __test__: Data = {
        "data": """
2333133121414131402
    """,
        "expected": 2858,
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

    def print(self, filesystem: list[File], compact=False):
        buffer = ["|"]
        for file in filesystem:
            if file.is_free_space or not compact:
                buffer.append(file.id * file.size)
            else:
                buffer.append(f"{file.id}*{file.size}")
            buffer.append("|")
        print("".join(buffer))

    def checksum(self, filesystem: list[File]) -> int:
        checksum = 0
        block = 0
        for file in filesystem:
            if not file.is_free_space:
                id = int(file.id)
                for i in range(file.size):
                    checksum += (block + i) * id
            block += file.size
        return checksum

    def solution(self, data: str) -> Any:
        filesystem: list[File] = []
        id = 0
        for i, digit in enumerate(data):
            size = int(digit)
            file = File(str(id) if i % 2 == 0 else FREE_SPACE, size)
            if size > 0:
                filesystem.append(file)
            if not file.is_free_space:
                id += 1
        # self.print(filesystem)
        file_pointer = len(filesystem) - 1
        while file_pointer >= 0:
            file = filesystem[file_pointer]
            if file.moved or file.is_free_space:
                file_pointer -= 1
                continue
            # print(file.id)
            free_pointer = None
            for pointer, free_file in enumerate(filesystem):
                if free_file is file:
                    break
                if free_file.is_free_space and file.size <= free_file.size:
                    free_pointer = pointer
                    break
            if free_pointer is not None:
                free_space = filesystem[free_pointer]
                filesystem[file_pointer], filesystem[free_pointer] = free_space, file
                file.moved = True
                file_pointer, free_pointer = free_pointer, file_pointer
                if free_space.size > file.size and free_pointer - file_pointer > 1:
                    free_space_file = File(FREE_SPACE, free_space.size - file.size)
                    filesystem.insert(file_pointer + 1, free_space_file)
                    free_pointer += 1
                    free_space.size = file.size
                for offset in (1, -1):
                    pointer = free_pointer + offset
                    if 0 <= pointer < len(filesystem) and (free_file := filesystem[pointer]).is_free_space:
                        free_space.size += free_file.size
                        del filesystem[pointer]
                        free_pointer = min(free_pointer, pointer)
                file_pointer = free_pointer
            file_pointer -= 1
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

import inspect
import os.path
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from typing import Self

from src.utils import root_dir

type Pair[T] = tuple[T, T]


@dataclass
class Object:
    @classmethod
    def from_data(cls, data: str) -> Self:
        return cls()


class PuzzleTemplate(ABC):
    def __init__(self, day: int | None = None, part: int | None = None):
        file = inspect.getfile(self.__class__)
        if day is None:
            # d{day:02}p{part}.py
            name = file[-8:-3]
            day = int(name[1:3])
            part = int(name[4:5])
        self.day = day
        self.part = part
        year_folder = os.path.basename(os.path.dirname(os.path.abspath(file)))
        self.year = int(year_folder[1:])

    @property
    def root_dir(self) -> Path:
        return root_dir()

    @property
    def io_dir(self) -> str:
        return os.path.join(self.root_dir, f"io/y{self.year}")

    @property
    def input_dir(self) -> str:
        return os.path.join(self.io_dir, "input")

    @property
    def output_dir(self) -> str:
        return os.path.join(self.io_dir, "output")

    def get_data(self, path: str) -> str:
        with open(path) as f:
            return f.read().strip()

    def get_groups(self, data: str) -> list[list[str]]:
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
        input_file = os.path.join(self.input_dir, f"d{self.day:02}p{self.part:02}.in")
        if not os.path.exists(input_file):
            input_file = os.path.join(self.input_dir, f"d{self.day:02}.in")
        return self.get_data(input_file)

    def get_output(self, path: str):
        output_path = f"{self.output_dir}/{path}"
        os.makedirs(output_path, exist_ok=True)
        return output_path

    @abstractmethod
    def solution(self, data: str) -> Any:
        pass

    def solve(self) -> None:
        print(self.solution(self.get_input()))


if __name__ == "__main__":
    PuzzleTemplate().solve()

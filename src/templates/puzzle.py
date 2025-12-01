import inspect
import os.path
import re
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Any

from src.utils import root_dir


class Puzzle(ABC):
    def __init__(self):
        if match := re.match(r"Day(\d+)Part(\d+)", self.__class__.__name__):
            self.day = int(match.group(1))
            self.part = int(match.group(2))
        else:
            raise ValueError("Invalid Class Name")
        file = inspect.getfile(self.__class__)
        year_folder = os.path.basename(os.path.dirname(os.path.abspath(file)))
        self.year = int(year_folder[1:])

    @property
    def name(self) -> str:
        return f"D{self.day:02}P{self.part:02}"

    @property
    def full_name(self):
        return f"Day {self.day}, Part {self.part}"

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

    def solve(self, tests: list[tuple[str, Any]] | None = None) -> None:
        if self.test(tests):
            solution = self.solution(self.get_input())
            print(f"=== {self.full_name} - SOLUTION ===")
            print(solution)

    def test(self, tests: list[tuple[str, Any]] | None) -> bool:
        if not tests:
            return True
        for i, (data, expected) in enumerate(tests):
            solution = self.solution(data.strip())
            if solution != expected:
                print(f"=== {self.full_name} - TEST {i} ===")
                msg = ["FAILED!", "Expected:", expected, "Solution:", solution]
                print("\n".join(str(part) for part in msg))
                return False
        return True


if __name__ == "__main__":
    Puzzle().solve()

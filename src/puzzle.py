import inspect
import os.path
import re
from abc import abstractmethod
from pathlib import Path

from utils import create_banner
from utils import root_dir


class Puzzle[T, R]:
    def __init__(self):
        if match := re.match(r"Day(\d+)Part(\d+)", self.__class__.__name__):
            self.day = int(match.group(1))
            self.part = int(match.group(2))
        else:
            raise ValueError("Invalid Class Name")
        file = inspect.getfile(self.__class__)
        year_folder = os.path.basename(os.path.dirname(os.path.abspath(file)))
        self.year = int(year_folder[1:])
        self.debug: bool = False
        self.logs: list[str] = []

    @property
    def name(self) -> str:
        return f"D{self.day:02}P{self.part:02}"

    @property
    def full_name(self) -> str:
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

    def get_input_groups(self, data: str) -> list[list[str]]:
        data = data.strip()
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

    def get_input_lines(self, data: str) -> list[str]:
        groups = self.get_input_groups(data)
        assert len(groups) == 1
        return groups[0]

    def get_flat_input(self, data: str) -> str:
        groups = self.get_input_lines(data)
        return "".join(groups)

    def get_raw_input(self) -> str:
        input_file = os.path.join(self.input_dir, f"d{self.day:02}p{self.part:02}.in")
        if not os.path.exists(input_file):
            input_file = os.path.join(self.input_dir, f"d{self.day:02}.in")
        return self.get_data(input_file)

    def create_output_path(self, path: str) -> str:
        output_path = f"{self.output_dir}/{path}"
        os.makedirs(output_path, exist_ok=True)
        return output_path

    @abstractmethod
    def parse_data(self, data: str) -> T:
        pass

    @abstractmethod
    def solution(self, parsed_data: T) -> R:
        pass

    def solve(self, tests: list[tuple[str, R]] | None = None, debug: bool = False) -> None:
        if self.test(tests):
            self.debug = debug
            self.logs.clear()
            print(create_banner(f"{self.full_name} - SOLUTION"))
            solution = self.solution(self.parse_data(self.get_raw_input()))
            print(solution)

    def test(self, tests: list[tuple[str, R]] | None) -> bool:
        if not tests:
            return True
        for i, (data, expected) in enumerate(tests):
            self.logs.clear()
            self.log(create_banner(f"{self.full_name} - TEST {i}"))
            solution = self.solution(self.parse_data(data.strip()))
            if solution != expected:
                msg = ["FAILED!", "Expected:", expected, "Solution:", solution]
                self.log("\n".join(str(part) for part in msg))
                self.dump_logs()
                return False
        return True

    def log(self, *args) -> None:
        msg = " ".join(str(arg) for arg in args)
        self.logs.append(msg)
        if self.debug:
            print(msg)

    def dump_logs(self) -> None:
        print("\n".join(self.logs))

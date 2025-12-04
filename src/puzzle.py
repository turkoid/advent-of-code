import inspect
import re
from abc import abstractmethod
from pathlib import Path
from typing import Any

from utils import create_banner
from utils import root_dir


class Puzzle:
    def __init__(self):
        if match := re.match(r"Day(\d+)Part(\d+)", self.__class__.__name__):
            self.day = int(match.group(1))
            self.part = int(match.group(2))
        else:
            raise ValueError("Invalid Class Name")
        file = Path(inspect.getfile(self.__class__))
        year_folder = file.absolute().parent
        self.year = int(year_folder.name[1:])
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
    def io_dir(self) -> Path:
        return self.root_dir.joinpath("io", f"y{self.year:04}")

    @property
    def input_dir(self) -> Path:
        return self.io_dir.joinpath("input")

    @property
    def output_dir(self) -> Path:
        return self.io_dir.joinpath("output")

    def get_data(self, path: Path) -> str:
        return path.read_text()

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

    def get_input_grid(self, data: str) -> list[list[str]]:
        return [list(line) for line in self.get_input_lines(data)]

    def get_raw_input(self) -> str:
        input_path = self.input_dir.joinpath(f"d{self.day:02}p{self.part:02}.in")
        if not input_path.exists():
            input_path = self.input_dir.joinpath(f"d{self.day:02}.in")
        return self.get_data(input_path)

    def create_output_path(self, path: Path | str) -> Path:
        output_path = self.output_dir.joinpath(path)
        output_path.mkdir(parents=True, exist_ok=True)
        return output_path

    @abstractmethod
    def parse_data(self, data: str) -> None:
        pass

    @abstractmethod
    def solution(self, parsed_data: None) -> None:
        pass

    def solve(self, tests: list[tuple[str, Any]] | None = None, debug: bool = False) -> None:
        if self.test(tests):
            self.debug = debug
            self.logs.clear()
            print(create_banner(f"{self.full_name} - SOLUTION"))
            solution = self.solution(self.parse_data(self.get_raw_input()))
            print(solution)

    def test(self, tests: list[tuple[str, Any]] | None) -> bool:
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

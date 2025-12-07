import inspect
import re
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Any

import click
from utils import create_banner
from utils import crop
from utils import MISSING
from utils import root_dir

from aoc import AdventOfCode


class Puzzle(ABC):
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
        self._divider_width: int = 42
        self._in_test: bool = False

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

    def get_file_data(self, path: Path) -> str:
        return path.read_text()

    def get_input_groups(self, data: str) -> list[list[str]]:
        current_lines = []
        line_groups = [current_lines]
        for line in data.splitlines():
            if line.strip() == "":
                current_lines = []
                line_groups.append(current_lines)
            else:
                current_lines.append(line)
        line_groups = [crop(lines) for lines in line_groups if lines]
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

    def get_puzzle_input(self) -> str:
        formatted_day = AdventOfCode.formatted_day(self.day)
        formatted_part = AdventOfCode.formatted_part(self.part)
        input_path = self.input_dir.joinpath(f"{formatted_day}{formatted_part}.in")
        if not input_path.exists():
            input_path = self.input_dir.joinpath(f"{formatted_day}.in")
        return self.get_file_data(input_path)

    def create_output_path(self, path: Path | str) -> Path:
        output_path = self.output_dir.joinpath(path)
        output_path.mkdir(parents=True, exist_ok=True)
        return output_path

    def create_header(self, message: str, update_divider_width: bool = False) -> str:
        banner = create_banner(f"{self.full_name} - {message}")
        if update_divider_width:
            self._divider_width = max(len(line) for line in banner.splitlines())
        return banner

    def print_divider(self, width: int | None = None) -> None:
        if width is None:
            width = self._divider_width
        width = max(width, 1)
        self.log(click.style("=" * width, fg="black", bg="blue"))

    @abstractmethod
    def parse_data(self, data: str) -> None:
        pass

    @abstractmethod
    def solution(self, parsed_data: None) -> None:
        pass

    def is_solved(self, solution: Any, expected: Any) -> bool:
        if solution == expected:
            return True
        msg = ["FAILED!", "Expected:", expected, "Solution:", solution]
        self.log("\n".join(str(part) for part in msg))
        self.dump_logs()
        return False

    def solve(
        self, tests: list[tuple[str, Any]] | None = None, *, expected: Any = MISSING, debug: bool = False
    ) -> None:
        if self.test(tests):
            self.debug = debug
            self.logs.clear()
            self.echo(self.create_header("SOLUTION", True))
            solution = self.solution(self.parse_data(self.get_puzzle_input()))
            if expected is MISSING or self.is_solved(solution, expected):
                self.echo(solution)

    def test(self, tests: list[tuple[str, Any]] | None) -> bool:
        if not tests:
            return True

        try:
            self._in_test = True
            for i, (data, expected) in enumerate(tests):
                self.logs.clear()
                self.log(self.create_header(f"TEST {i}", True))
                solution = self.solution(self.parse_data(data))
                if not self.is_solved(solution, expected):
                    return False
                self.print_divider()
        finally:
            self._in_test = False
        return True

    def echo(self, *args) -> None:
        if self._in_test:
            self.log(*args)
        else:
            click.echo(*args)

    def log(self, *args) -> None:
        msg = " ".join(str(arg) for arg in args)
        self.logs.append(msg)
        if self.debug:
            click.echo(msg)

    def dump_logs(self) -> None:
        click.echo("\n".join(self.logs))

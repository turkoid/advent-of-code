import importlib
from typing import Any

from aoc import AdventOfCode


class Runner:
    def __init__(self, year: int, day: int, parts: int) -> None:
        self.year = year
        self.day = day
        self.parts = parts
        self.runnable: dict[int, bool] = {}
        self.tests: dict[int, list[tuple[str, Any]]] = {}
        self.module = importlib.import_module(AdventOfCode.puzzle_module(self.year, self.day))

    def add_test(self, part: int, data: str, expected: Any) -> None:
        self.tests.setdefault(part, []).append((data, expected))
        self.runnable[part] = True

    def enable(self, part: int) -> None:
        self.runnable[part] = True

    def disable(self, part: int) -> None:
        self.runnable[part] = False

    def run(self, part: int | None = None, *, debug: bool = False) -> None:
        if part is None:
            start = 1
            end = self.parts + 1
        else:
            start = part
            end = start + 1

        for part in range(start, end):
            if not self.runnable.get(part, False):
                continue
            puzzle_class = getattr(self.module, AdventOfCode.puzzle_class(self.day, part))
            puzzle = puzzle_class()
            tests = self.tests.get(part, [])
            puzzle.solve(tests, debug=debug)

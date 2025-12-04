import importlib
from typing import Any


class Runner:
    def __init__(self, year: int, day: int, parts: int) -> None:
        self.year = year
        self.day = day
        self.parts = parts
        self.runnable: dict[int, bool] = {}
        self.tests: dict[int, list[tuple[str, Any]]] = {}
        self.module = importlib.import_module(f"y{self.year:04}.d{self.day:02}")

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

        for _part in range(start, end):
            if not self.runnable.get(_part, False):
                continue
            puzzle_class = getattr(self.module, f"Day{self.day}Part{_part}")
            puzzle = puzzle_class()
            tests = self.tests.get(_part, [])
            puzzle.solve(tests, debug=debug)

from pathlib import Path
from typing import Any


def root_dir() -> Path:
    return Path(__file__).parent.parent


def pretty_grid(self, grid: list[list[Any] | Any]) -> str:
    return "\n".join("".join(str(o) for o in line) if isinstance(line, list) else str(line) for line in grid)


def create_banner(msg: str) -> str:
    banner_line = "-" * (len(msg) + 2)
    banner_line = f"+{banner_line}+"
    lines = [
        banner_line,
        f"| {msg} |",
        banner_line,
    ]
    return "\n".join(lines)

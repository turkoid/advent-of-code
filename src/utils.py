from pathlib import Path
from typing import Any


def root_dir() -> Path:
    return Path(__file__).parent.parent


def pretty_grid(grid: list[list | Any], padding: int = 1) -> str:
    padding = max(padding, 0)
    lines = []
    if padding:
        h_pad = " " * padding
        v_pad = " " * (padding * 2 + len(grid[0]))
        lines.extend([v_pad] * padding)
    else:
        h_pad = ""
        v_pad = ""
    for row in grid:
        if isinstance(row, list):
            row = "".join(str(o) for o in row)
        else:
            row = str(row)
        lines.append(f"{h_pad}{row}{h_pad}")
    if padding:
        lines.extend([v_pad] * padding)

    return "\n".join(lines)


def create_banner(msg: str) -> str:
    banner_line = "-" * (len(msg) + 2)
    banner_line = f"+{banner_line}+"
    lines = [
        banner_line,
        f"| {msg} |",
        banner_line,
    ]
    return "\n".join(lines)

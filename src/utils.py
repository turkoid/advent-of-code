import itertools
from pathlib import Path
from typing import Any

import click


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


def crop[T: (str, list[str])](s: T) -> T:
    lines = s.splitlines() if isinstance(s, str) else s
    lines = [line.rstrip() for line in lines if line.strip()]
    trim_left = min(len(line) - len(line.lstrip()) for line in lines)
    width = max(len(line) - trim_left for line in lines)
    lines = [f"{line[trim_left:]: <{width}}" for line in lines]
    return "\n".join(lines) if isinstance(s, str) else lines


def concat_string_lists(*lists: list[str], fill_char: str = " ", sep: str = " ") -> str:
    buffer = []
    max_widths = [max(len(click.unstyle(s)) for s in lst) for lst in lists]
    fillers = [fill_char * width for width in max_widths]
    for groups in itertools.zip_longest(*lists):
        line_buffer = [
            filler if grp is None else f"{grp:{fill_char}<{width}}"
            for grp, width, filler in zip(groups, max_widths, fillers)
        ]
        buffer.append(sep.join(line_buffer))
    return "\n".join(buffer)

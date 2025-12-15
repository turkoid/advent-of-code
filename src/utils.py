import itertools
from pathlib import Path
from typing import Any
from typing import NamedTuple
from typing import overload
from typing import Self

import click


class MissingType:
    def __repr__(self) -> str:
        return "MISSING"


MISSING = MissingType()


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


type Scalar = int | float


class Point(NamedTuple):
    x: Scalar
    y: Scalar

    @overload
    def equals(self, point: Self | tuple[Scalar, Scalar]) -> bool:
        pass

    @overload
    def equals(self, x: Scalar, y: Scalar) -> bool:
        pass

    def equals(self, *args) -> bool:
        if len(args) == 1:
            pt = args[0]
            if pt is None:
                return False
            x = pt[0]
            y = pt[1]
        else:
            x, y = args
        return self.x == x and self.y == y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


class Point3D(NamedTuple):
    x: Scalar
    y: Scalar
    z: Scalar

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"


class Dimensions(NamedTuple):
    width: Scalar
    height: Scalar

    @property
    def w(self) -> Scalar:
        return self.width

    @property
    def h(self) -> Scalar:
        return self.height

    def __repr__(self) -> str:
        return f"{self.width}x{self.height}"


class Dimensions3D(NamedTuple):
    width: Scalar
    height: Scalar
    depth: Scalar

    @property
    def w(self) -> Scalar:
        return self.width

    @property
    def h(self) -> Scalar:
        return self.height

    @property
    def d(self):
        return self.depth

    def __repr__(self) -> str:
        return f"{self.width}x{self.height}x{self.depth}"


def _parse_xy_or_point(*args) -> tuple[Scalar, Scalar] | None:
    match args:
        case [Point(x, y)]:
            return x, y
        case [x, y]:
            return x, y
        case _:
            return None
    return None

    raise ValueError()

    if len(args) == 1:
        pt = args[0]
        if pt is None:
            return
        x = pt[0]
        y = pt[1]
    else:
        x, y = args
    return x, y


class Line2D(NamedTuple):
    point_a: Point
    point_b: Point

    def is_horizontal(self) -> bool:
        return self.point_a != self.point_b and self.point_a.y == self.point_b.y

    def is_vertical(self) -> bool:
        return self.point_a != self.point_b and self.point_a.x == self.point_b.x

    def contains(self, *args) -> bool:
        if not self.is_horizontal() and not self.is_vertical():
            return False
        x, y = _parse_xy_or_point(*args)
        if x == self.point_a.x:
            return self.min_y <= y <= self.max_y
        else:
            return self.min_x <= x <= self.max_x

    @property
    def min_x(self):
        return min(self.point_a.x, self.point_b.x)

    @property
    def max_x(self):
        return max(self.point_a.x, self.point_b.x)

    @property
    def min_y(self):
        return min(self.point_a.y, self.point_b.y)

    @property
    def max_y(self):
        return max(self.point_a.y, self.point_b.y)

    @property
    def upper_point(self):
        if self.is_horizontal():
            raise ValueError(f"{self} is horizontal")
        return self.point_a if self.point_a.y < self.point_b.y else self.point_b

    @property
    def lower_point(self):
        if self.is_horizontal():
            raise ValueError(f"{self} is horizontal")
        return self.point_a if self.point_a.y > self.point_b.y else self.point_b

    @property
    def left_point(self):
        if self.is_vertical():
            raise ValueError(f"{self} is vertical")
        return self.point_a if self.point_a.x < self.point_b.x else self.point_b

    @property
    def right_point(self):
        if self.is_vertical():
            raise ValueError(f"{self} is vertical")
        return self.point_a if self.point_a.x > self.point_b.x else self.point_b

    def __repr__(self) -> str:
        return f"{self.point_a}---{self.point_b}"


class Rectangle(NamedTuple):
    anchor_a: Point
    anchor_b: Point

    # anchors (edges)

    @property
    def left(self) -> Scalar:
        return min(self.anchor_a.x, self.anchor_b.x)

    @property
    def right(self) -> Scalar:
        return max(self.anchor_a.x, self.anchor_b.x)

    @property
    def top(self) -> Scalar:
        return min(self.anchor_a.y, self.anchor_b.y)

    @property
    def bottom(self) -> Scalar:
        return max(self.anchor_a.y, self.anchor_b.y)

    # anchors (corners)
    @property
    def top_left(self) -> Point:
        return Point(self.left, self.top)

    @property
    def top_right(self) -> Point:
        return Point(self.right, self.top)

    @property
    def bottom_left(self) -> Point:
        return Point(self.left, self.bottom)

    @property
    def bottom_right(self) -> Point:
        return Point(self.right, self.bottom)

    # anchor aliases (corners)

    @property
    def tl(self) -> Point:
        return self.top_left

    @property
    def tr(self) -> Point:
        return self.top_right

    @property
    def bl(self) -> Point:
        return self.bottom_left

    @property
    def br(self) -> Point:
        return self.bottom_right

    # cardinal directions (edges)

    @property
    def north(self) -> Scalar:
        return self.top

    @property
    def east(self) -> Scalar:
        return self.right

    @property
    def south(self) -> Scalar:
        return self.bottom

    @property
    def west(self) -> Scalar:
        return self.left

    # cardinal directions (corners)

    @property
    def north_west(self) -> Point:
        return self.top_left

    @property
    def north_east(self) -> Point:
        return self.top_right

    @property
    def south_east(self) -> Point:
        return self.bottom_right

    @property
    def south_west(self) -> Point:
        return self.bottom_left

    # cardinal aliases (edges)

    @property
    def n(self) -> Scalar:
        return self.top

    @property
    def e(self) -> Scalar:
        return self.right

    @property
    def s(self) -> Scalar:
        return self.bottom

    @property
    def w(self) -> Scalar:
        return self.left

    # cardinal aliases (corners)

    @property
    def nw(self) -> Point:
        return self.top_left

    @property
    def ne(self) -> Point:
        return self.top_right

    @property
    def se(self) -> Point:
        return self.bottom_right

    @property
    def sw(self) -> Point:
        return self.bottom_left

    # dimensions

    @property
    def width(self) -> Scalar:
        return self.right - self.left

    @property
    def height(self) -> Scalar:
        return self.bottom - self.top

    def dimensions(self) -> Dimensions:
        return Dimensions(self.width, self.height)

    # helpers

    @property
    def area(self) -> int:
        return self.width * self.height

    @overload
    def contains(self, point: Point | tuple[int, int]) -> bool:
        pass

    @overload
    def contains(self, x: Scalar, y: Scalar) -> bool:
        pass

    def contains(self, *args) -> bool:
        x, y = _parse_xy_or_point(*args)
        inside = self.left <= x <= self.right and self.top <= y <= self.bottom
        click.echo(f"is {Point(x, y)} in {self}: {inside}")
        return inside

    def encapsulates(self, *args) -> bool:
        x, y = _parse_xy_or_point(*args)
        return self.left < x < self.right and self.top < y < self.bottom

    def corners(self, *exclude: Point) -> list[Point]:
        return [corner for corner in [self.tl, self.tr, self.br, self.bl] if corner not in exclude]

    # joke aliases

    @property
    def never(self) -> Scalar:
        return self.top

    @property
    def eat(self) -> Scalar:
        return self.right

    @property
    def soggy(self) -> Scalar:
        return self.bottom

    @property
    def waffles(self) -> Scalar:
        return self.left

    @property
    def never_waffles(self) -> Point:
        return self.top_left

    @property
    def never_eat(self) -> Point:
        return self.top_right

    @property
    def soggy_eat(self) -> Point:
        return self.bottom_right

    @property
    def soggy_waffles(self) -> Point:
        return self.bottom_left

    @property
    def eat_waffles(self) -> Scalar:
        return self.right - self.left

    @property
    def never_soggy(self) -> Scalar:
        return self.bottom - self.top

    # magic

    def __contains__(self, item):
        return self.contains(item)


class Color:
    # just some common ones, not meant to be exhaustive
    @staticmethod
    def red(text: Any) -> str:
        return click.style(text, fg="red")

    @staticmethod
    def green(text: Any) -> str:
        return click.style(text, fg="green")

    @staticmethod
    def blue(text: Any) -> str:
        return click.style(text, fg="blue")

    @staticmethod
    def yellow(text: Any) -> str:
        return click.style(text, fg="yellow")

    @staticmethod
    def magenta(text: Any) -> str:
        return click.style(text, fg="magenta")

    @staticmethod
    def cyan(text: Any) -> str:
        return click.style(text, fg="cyan")

    @staticmethod
    def success(text: Any) -> str:
        return Color.green(text)

    @staticmethod
    def fail(text: Any) -> str:
        return Color.red(text)

    @staticmethod
    def err(text: Any) -> str:
        return Color.red(text)

    @staticmethod
    def info(text: Any) -> str:
        return Color.yellow(text)

    @staticmethod
    def highlight(text: Any) -> str:
        return Color.magenta(text)

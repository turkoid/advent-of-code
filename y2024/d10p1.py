from collections.abc import Iterator
from dataclasses import dataclass
from dataclasses import field
from dataclasses import InitVar
from typing import Any
from typing import Self


@dataclass(frozen=True, repr=False)
class Point:
    x: int
    y: int

    def translate(self, x: int, y: int) -> Self:
        return Point(self.x + x, self.y + y)

    @property
    def north(self) -> Self:
        return self.translate(0, -1)

    @property
    def south(self) -> Self:
        return self.translate(0, 1)

    @property
    def west(self) -> Self:
        return self.translate(-1, 0)

    @property
    def east(self) -> Self:
        return self.translate(1, 0)

    def neighbors(self):
        return [self.north, self.east, self.south, self.west]

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __iter__(self):
        return iter((self.x, self.y))

    def __getitem__(self, index: int) -> int:
        return list(self)[index]


@dataclass
class Grid:
    lines: InitVar[list[str]]
    cells: list[list[int | str]] = field(init=False)
    width: int = field(init=False)
    height: int = field(init=False)

    def __post_init__(self, lines: list[str]):
        self.cells = [[c if c == "." else int(c) for c in line] for line in lines]
        self.width = len(self.cells[0])
        self.height = len(self.cells)

    def __getitem__(self, pt: Point | tuple[int, int]) -> int | str:
        x, y = pt
        return self.cells[y][x]

    def __contains__(self, pt: Point) -> bool:
        return 0 <= pt.x < self.width and 0 <= pt.y < self.height

    def cells_with_height(self, height: int | str) -> list[Point]:
        return [Point(x, y) for y, row in enumerate(self.cells) for x, cell in enumerate(row) if self[x, y] == height]


class Puzzle:
    __test__ = {
        "data": [
            """
0123
1234
8765
9876
            """,
            """
...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9
            """,
            """
..90..9
...1.98
...2..7
6543456
765.987
876....
987....
            """,
            """
10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01
            """,
            """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
            """,
        ],
        "expected": [1, 2, 4, 3, 36],
    }

    def __init__(self, day: int | None = None, part: int | None = None):
        if day is None:
            # d{day:02}p{part}.py
            name = __file__[-8:-3]
            day = int(name[1:3])
            part = int(name[4:5])
        self.day = day
        self.part = part

    def get_data(self, path: str) -> str:
        with open(path) as f:
            return f.read().strip()

    def get_groups(self, data) -> list[list[str]]:
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
        return self.get_data(f"inputs/d{self.day:02}.in")

    def get_test_data(self) -> Iterator[tuple[str, Any]]:
        cfg = self.__test__
        assert len(cfg["data"]) == len(cfg["expected"])
        return zip([data.strip() for data in cfg["data"]], cfg["expected"])

    def solution(self, data: str) -> Any:
        grid = Grid(self.get_lines(data))
        trail_heads = {pt: [] for pt in grid.cells_with_height(0)}
        # print(trail_heads)
        queue = [[pt] for pt in trail_heads]
        visited: dict[Point, list[list[Point]]] = {}
        while queue:
            path: list[Point] = queue.pop()
            trail_start = path[0]
            cell = path[-1]
            if cell in visited:
                for visited_path in visited[cell]:
                    for previous_cell in reversed(path[:-1]):
                        visited[previous_cell].append(visited_path)
                    trail_end = visited_path[-1]
                    if trail_end not in trail_heads[trail_start]:
                        trail_heads[trail_start].append(trail_end)
                continue
            visited[cell] = []
            height = grid[cell]
            for neighbor in cell.neighbors():
                if neighbor not in grid:
                    continue
                if (neighbor_height := grid[neighbor]) == ".":
                    continue
                if neighbor_height == height + 1:
                    fork = path[:]
                    fork.append(neighbor)
                    if neighbor_height == 9:
                        if neighbor not in trail_heads[trail_start]:
                            trail_heads[trail_start].append(neighbor)
                        for previous_cell in reversed(path):
                            visited[previous_cell].append(fork)
                    queue.append(fork)
        # print(trail_heads)
        total = 0
        for trail_start, trail_ends in trail_heads.items():
            # print(trail_start, len(trail_ends))
            total += len(trail_ends)
        return total

    def solve(self, test: bool | str = True) -> None:
        if isinstance(test, str):
            print(self.solution(test))
            return
        if test:
            for i, (data, expected) in enumerate(self.get_test_data()):
                solution = self.solution(data)
                assert solution == expected, f"[{i}] --- solution != result: {solution} != {expected}"
        print(self.solution(self.get_input()))


if __name__ == "__main__":
    Puzzle().solve()

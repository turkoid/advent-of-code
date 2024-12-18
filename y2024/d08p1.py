from typing import Any
from typing import TypedDict


class Data(TypedDict):
    data: str
    expected: Any


class Puzzle:
    __test__: Data = {
        "data": """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
    """,
        "expected": 14,
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
        return self.get_data(f"../input/y2024//d{self.day:02}.in")

    def get_test_data(self) -> tuple[str, str]:
        data = self.__test__["data"].strip()
        expected = self.__test__["expected"]
        return data, expected

    def print(self, locations: list[list[str]]):
        lines = []
        for row in locations:
            lines.append("".join(c[-1] for c in row))
        print("\n".join(lines))
        print("")

    def solution(self, data: str) -> Any:
        lines = self.get_lines(data)
        grid = [list(line) for line in lines]
        frequencies = {}
        for y, row in enumerate(grid):
            for x, location in enumerate(row):
                if location != ".":
                    frequencies.setdefault(location, []).append((x, y))
        width = len(grid[0])
        height = len(grid)
        unique_antinodes = 0
        for frequency, antennas in frequencies.items():
            for i, a in enumerate(antennas[:-1]):
                for b in antennas[i + 1 :]:
                    slope = (a[0] - b[0], a[1] - b[1])
                    antinode_a = (a[0] + slope[0], a[1] + slope[1])
                    antinode_b = (b[0] - slope[0], b[1] - slope[1])
                    for antinode in (antinode_a, antinode_b):
                        if 0 <= antinode[0] < width and 0 <= antinode[1] < height:
                            location = grid[antinode[1]][antinode[0]]
                            new_location = location
                            if location == ".":
                                new_location = "#"
                            elif location != "#" and len(location) == 1:
                                new_location = f"#{location}"
                            if new_location != location:
                                unique_antinodes += 1
                                grid[antinode[1]][antinode[0]] = new_location
                                # print(a, b)
                                # self.print(locations)
        return unique_antinodes

    def solve(self, test: bool | str = True) -> None:
        if isinstance(test, str):
            print(self.solution(test))
            return
        if test:
            data, expected = self.get_test_data()
            solution = self.solution(data)
            assert solution == expected, f"solution != result: {solution} != {expected}"
        print(self.solution(self.get_input()))


if __name__ == "__main__":
    Puzzle().solve()

from collections.abc import Iterator
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from typing import Any


class Fence(Enum):
    NORTH = ("n", "-")
    EAST = ("e", "|")
    SOUTH = ("s", "-")
    WEST = ("w", "|")


@dataclass
class Plant:
    name: str
    index: int | None
    x: int
    y: int
    fences: set[Fence] = field(default_factory=set)

    @property
    def id(self):
        return self.name, self.index

    def grid(self):
        locations = [
            [(Fence.NORTH, Fence.WEST), (Fence.NORTH,), (Fence.NORTH, Fence.EAST)],
            [(Fence.WEST,), None, (Fence.EAST,)],
            [(Fence.SOUTH, Fence.WEST), (Fence.SOUTH,), (Fence.SOUTH, Fence.EAST)],
        ]
        grid = []
        for row in locations:
            line = []
            for anchor in row:
                if anchor is None:
                    line.append(self.name)
                elif any(fence in self.fences for fence in anchor):
                    line.append("+" if len(anchor) == 2 else anchor[0].value[1])
                else:
                    line.append(" ")
            grid.append(line)
        return grid

    def __str__(self):
        grid = self.grid()
        return "\n".join("".join(line) for line in grid)


@dataclass
class Plot:
    id: tuple[str, int]
    plants: list[Plant] = field(default_factory=list)

    @property
    def area(self):
        return len(self.plants)

    @property
    def perimeter(self):
        total = 0
        for plant in self.plants:
            total += len(plant.fences)
        return total


class Puzzle:
    __test__ = {
        "data": [
            """
AAAA
BBCD
BBCC
EEEC
            """,
            """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
            """,
            """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
            """,
        ],
        "expected": [140, 772, 1930],
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

    def get_test_data(self) -> Iterator[tuple[str, Any]]:
        cfg = self.__test__
        assert len(cfg["data"]) == len(cfg["expected"])
        return zip([data.strip() for data in cfg["data"]], cfg["expected"])

    def print(self, farm: list[list[Plant]]):
        lines = []
        for y, row in enumerate(farm):
            row_lines = [[], [], []]
            for x, plant in enumerate(row):
                grid = plant.grid()
                for i in range(3):
                    if x == 0:
                        row_lines[i].extend(grid[i])
                    else:
                        a = row_lines[i][-1]
                        b = grid[i][0]
                        if a == "|" or b == "|":
                            row_lines[i][-1] = "|"
                        elif a == "+" or b == "+":
                            row_lines[i][-1] = "+"
                        row_lines[i].extend(grid[i][1:])
            if y == 0:
                lines.extend(row_lines)
            else:
                for i, (a, b) in enumerate(zip(lines[-1], row_lines[0])):
                    if "-" in a or "-" in b:
                        lines[-1][i] = "-"
                    elif "+" in a or "+" in b:
                        lines[-1][i] = "+"
                lines.extend(row_lines[1:])
        buffer = []
        for line in lines:
            line = "".join(line)
            buffer.append(line)
        print("\n".join(buffer))

    def solution(self, data: str) -> Any:
        farm = [[plant for plant in row] for row in self.get_lines(data)]
        fenced_farm: list[list[Plant]] = []
        counters: dict[str, int] = {}
        plots: dict[tuple[str, int], Plot] = {}
        for y, row in enumerate(farm):
            farm_row = []
            for x, name in enumerate(row):
                north = fenced_farm[y - 1][x] if y > 0 else None
                east = farm[y][x + 1] if x < len(row) - 1 else None
                south = farm[y + 1][x] if y < len(farm) - 1 else None
                west = farm_row[x - 1] if x > 0 else None
                if north and west and name == north.name and name == west.name and north.index != west.index:
                    index = north.index
                    north_plot = plots[north.id]
                    west_plot = plots[west.id]
                    for plant in west_plot.plants:
                        plant.index = index
                    north_plot.plants.extend(west_plot.plants)
                    del plots[west_plot.id]
                elif north and name == north.name:
                    index = north.index
                elif west and name == west.name:
                    index = west.index
                else:
                    index = counters.setdefault(name, 0)
                    counters[name] += 1
                plant = Plant(name, index, x, y)
                plot = plots.setdefault(plant.id, Plot(plant.id))
                if not north or north.id != plant.id:
                    plant.fences.add(Fence.NORTH)
                if east != name:
                    plant.fences.add(Fence.EAST)
                if south != name:
                    plant.fences.add(Fence.SOUTH)
                if not west or west.id != plant.id:
                    plant.fences.add(Fence.WEST)
                plot.plants.append(plant)
                farm_row.append(plant)
            fenced_farm.append(farm_row)
        # self.print(fenced_farm)
        total = 0
        for id, plot in plots.items():
            cost = plot.area * plot.perimeter
            # print(f"{id[0]}{id[1]}: {plot.area} * {plot.perimeter} = {cost}")
            total += cost
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

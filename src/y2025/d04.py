from puzzle import Puzzle
from utils import pretty_grid

type Grid = list[list[str]]


class Day4Part1(Puzzle):
    def parse_data(self, data: str) -> Grid:
        grid = [list(line) for line in self.get_input_lines(data)]
        assert len(grid) > 0
        width = len(grid[0])
        assert all(len(row) == width for row in grid)
        return grid

    def move_paper_rolls(self, warehouse: Grid, part1: bool = True) -> int:
        width = len(warehouse[0])
        height = len(warehouse)
        moved_paper_rolls = 0
        for y, row in enumerate(warehouse):
            for x, cell in enumerate(row):
                if cell != "@":
                    continue
                adjacent_cells = []
                if y - 1 >= 0:
                    adjacent_cells.extend(warehouse[y - 1][max(x - 1, 0) : min(x + 2, width + 1)])
                if x - 1 >= 0:
                    adjacent_cells.append(row[x - 1])
                if x + 1 < width:
                    adjacent_cells.append(row[x + 1])
                if y + 1 < height:
                    adjacent_cells.extend(warehouse[y + 1][max(x - 1, 0) : min(x + 2, width + 1)])

                if (adjacent_cells.count("@") + (adjacent_cells.count("X") if part1 else 0)) < 4:
                    moved_paper_rolls += 1
                    warehouse[y][x] = "X"
        self.echo(pretty_grid(warehouse))
        return moved_paper_rolls

    def solution(self, parsed_data: Grid) -> int:
        self.echo(pretty_grid(parsed_data))
        moved_paper_rolls = self.move_paper_rolls(parsed_data)
        return moved_paper_rolls


class Day4Part2(Day4Part1):
    def solution(self, parsed_data: Grid) -> int:
        self.echo(pretty_grid(parsed_data))
        moved_paper_rolls = 0
        while removed_paper_rolls := self.move_paper_rolls(parsed_data, False):
            self.echo(f"Removed {removed_paper_rolls} paper rolls")
            moved_paper_rolls += removed_paper_rolls
        return moved_paper_rolls

import copy

from puzzle import Puzzle
from utils import pretty_grid

type Grid = list[list[str]]


class Day4Part1(Puzzle):
    def parse_data(self, data: str) -> Grid:
        grid = [list(line) for line in self.get_input_lines(data)]
        return grid

    def solution(self, parsed_data: Grid) -> int:
        grid = parsed_data
        solution_grid = copy.deepcopy(parsed_data)
        width = len(grid[0])
        height = len(grid)
        self.log(pretty_grid(grid))
        moveable_paper_rolls = 0
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell != "@":
                    continue
                adjacent_cells = []
                if y - 1 >= 0:
                    adjacent_cells.extend(grid[y - 1][max(x - 1, 0) : min(x + 2, width + 1)])
                if x - 1 >= 0:
                    adjacent_cells.append(row[x - 1])
                if x + 1 < width:
                    adjacent_cells.append(row[x + 1])
                if y + 1 < height:
                    adjacent_cells.extend(grid[y + 1][max(x - 1, 0) : min(x + 2, width + 1)])
                if adjacent_cells.count("@") < 4:
                    moveable_paper_rolls += 1
                    solution_grid[y][x] = "X"
        self.log(pretty_grid(solution_grid))
        return moveable_paper_rolls

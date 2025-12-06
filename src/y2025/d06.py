import operator
from functools import reduce

from puzzle import Puzzle


class Day6Part1(Puzzle):
    def parse_data(self, data: str) -> tuple[list[list[int]], list[str]]:
        lines = self.get_input_lines(data)
        values = [[int(v) for v in line] for line in zip(*[line.split() for line in lines[:-1]])]
        ops = lines[-1].split()
        return values, ops

    def solution(self, parsed_data: tuple[list[list[int]], list[str]]) -> int:
        sum = 0
        for values, op in zip(*parsed_data):
            fn = operator.add if op == "+" else operator.mul
            sum += reduce(fn, values)
        return sum


class Day6Part2(Day6Part1):
    def parse_data(self, data: str) -> tuple[list[list[int]], list[str]]:
        lines = self.get_input_lines(data)
        self.log("\n".join(lines))
        ops = lines[-1].split()
        cols = [("".join(line)).strip() for line in zip(*lines[:-1])]
        cols.append("")
        vals = []
        group = []
        for col in cols:
            if col == "":
                vals.append([int(v) for v in group])
                group = []
            else:
                group.append(col)
        assert len(vals) == len(ops)
        return vals, ops

import operator
from functools import reduce

import click
from puzzle import Puzzle

Manifold = list[list[str]]
QuantumManifold = list[list[str | list[int]]]


def pew_pew(manifold: Manifold | QuantumManifold) -> str:
    styled_manifold = []
    for row in manifold:
        styled_row = []
        for cell in row:
            if cell == ".":
                styled_cell = " "
            elif cell == "S":
                styled_cell = click.style(cell, fg="green")
            elif cell == "^":
                styled_cell = click.style(cell, fg="blue")
            elif cell == "|":
                styled_cell = click.style(cell, fg="yellow")
            elif isinstance(cell, list):
                beams = [click.style("|" * size, fg="yellow") for size in cell]
                styled_cell = " ".join(beams)
            else:
                styled_cell = cell
            styled_row.append(styled_cell)
        styled_manifold.append("".join(styled_row))
    return "\n".join(styled_manifold)


class Day7Part1(Puzzle):
    def parse_data(self, data: str) -> Manifold:
        return self.get_input_grid(data)

    def solution(self, parsed_data: Manifold) -> int:
        manifold = parsed_data
        self.echo(pew_pew(manifold))
        self.echo_divider()
        total_splits = 0
        y = 1
        while y < len(manifold):
            row = manifold[y]
            x = 0
            while x < len(row):
                cell = row[x]
                above_cell = manifold[y - 1][x]
                replace_cell = None
                if above_cell in "S|":
                    replace_cell = "|"
                if replace_cell:
                    if cell == "^":
                        total_splits += 1
                        if x - 1 >= 0:
                            row[x - 1] = "|"
                        if x + 1 < len(row):
                            row[x + 1] = "|"
                    else:
                        row[x] = replace_cell
                x += 1
            y += 1
            self.echo(pew_pew([row]))
        return total_splits


class Day7Part2(Puzzle):
    def parse_data(self, data: str) -> QuantumManifold:
        assert "^^" not in data
        return self.get_input_grid(data)

    def solution(self, parsed_data: QuantumManifold) -> int:
        manifold = parsed_data
        width = len(manifold[0])
        self.echo(pew_pew(manifold))
        self.echo_divider()

        y = 1
        while y < len(manifold):
            row = manifold[y]
            x = 0
            while x < len(row):
                cell = row[x]
                above_cell = manifold[y - 1][x]
                if above_cell == "S":
                    manifold[y][x] = [1]
                elif not isinstance(above_cell, str):
                    if cell == "^":
                        merged_beams = reduce(operator.add, above_cell)
                        if x - 1 >= 0:
                            left_cell = manifold[y][x - 1]
                            if isinstance(left_cell, str):
                                manifold[y][x - 1] = [merged_beams]
                            else:
                                left_cell.append(merged_beams)
                        if x + 1 < width:
                            manifold[y][x + 1] = [merged_beams]
                    elif cell == ".":
                        manifold[y][x] = above_cell
                    elif not isinstance(cell, str):
                        cell.extend(above_cell)
                x += 1
            y += 1
        realities = 0
        for cell in manifold[-1]:
            if isinstance(cell, list):
                realities += reduce(operator.add, cell)
        return realities

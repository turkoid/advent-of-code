import click
from puzzle import Puzzle


def pew_pew(manifold: list[list[str]]) -> str:
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
            else:
                styled_cell = cell
            styled_row.append(styled_cell)
        styled_manifold.append("".join(styled_row))
    return "\n".join(styled_manifold)


class Day7Part1(Puzzle):
    def parse_data(self, data: str) -> list[list[str]]:
        return self.get_input_grid(data)

    def solution(self, parsed_data: list[list[str]]) -> int:
        manifold = parsed_data
        self.log(pew_pew(manifold))
        self.print_divider()
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
            self.log(pew_pew([row]))
        # self.echo(pew_pew(manifold))
        return total_splits


class Day7Part2(Puzzle):
    def parse_data(self, data: str) -> None:
        pass

    def solution(self, parsed_data: None) -> None:
        pass

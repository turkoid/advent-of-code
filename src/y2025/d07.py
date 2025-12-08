from dataclasses import dataclass
from dataclasses import field
from typing import Self

import click
from puzzle import Puzzle
from utils import MISSING
from utils import MissingType
from utils import Point


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
        return total_splits


type Manifold = list[list[str]]


@dataclass
class Junction:
    location: Point
    left_junction: Self | MissingType | None = field(init=False, default=MISSING)
    right_junction: Self | MissingType | None = field(init=False, default=MISSING)
    child_realities: int | None = field(init=False, default=None)


class Day7Part2(Puzzle):
    def parse_data(self, data: str) -> Manifold:
        return self.get_input_grid(data)

    def find_next_junction_location(self, manifold: Manifold, x: int, y: int) -> Point | None:
        if 0 <= x < len(manifold[0]):
            while y < len(manifold):
                if manifold[y][x] == "^":
                    return Point(x, y)
                y += 1
        return None

    def find_next_junction(
        self, manifold: Manifold, x: int, y: int, explored_junctions: dict[Point, Junction] | None = None
    ) -> Junction | None:
        loc = self.find_next_junction_location(manifold, x, y)
        if loc is None:
            return None
        explored_junctions = explored_junctions or {}
        junction = explored_junctions.get(loc, Junction(loc))
        return junction

    def solution(self, parsed_data: Manifold) -> int:
        manifold = parsed_data
        self.log(pew_pew(manifold))
        self.print_divider()
        explored_junctions: dict[Point, Junction] = {}
        start = Point(manifold[0].index("S"), 0)
        junction_prime = self.find_next_junction(manifold, start.x, start.y)
        itinerary: list[Junction] = [junction_prime]
        while itinerary:
            junction = itinerary.pop()
            self.log(f"Exploring Junction @ {junction.location}")
            if junction.child_realities is None:
                if junction.left_junction is MISSING:
                    junction.left_junction = self.find_next_junction(
                        manifold, junction.location.x - 1, junction.location.y, explored_junctions
                    )
                if junction.right_junction is MISSING:
                    junction.right_junction = self.find_next_junction(
                        manifold, junction.location.x + 1, junction.location.y, explored_junctions
                    )

                new_destinations = []
                junction.child_realities = 2
                for child_junction in [junction.left_junction, junction.right_junction]:
                    if not isinstance(child_junction, Junction):
                        continue
                    if child_junction.child_realities is None:
                        new_destinations.append(child_junction)
                    else:
                        junction.child_realities += child_junction.child_realities
                if new_destinations:
                    junction.child_realities = None
                    itinerary.append(junction)
                    itinerary.extend(new_destinations)
                else:
                    self.log(f"Explored {junction.child_realities} Realities")
                    explored_junctions[junction.location] = junction

        return junction_prime.child_realities

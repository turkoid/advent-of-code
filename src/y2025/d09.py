import click
from puzzle import Puzzle
from utils import Point
from utils import Rectangle


class Day9(Puzzle):
    def create_floor(self, red_tiles: list[Point]) -> list[list[str]]:
        width = max(pt.x for pt in red_tiles) + 1
        height = max(pt.y for pt in red_tiles) + 1
        if width > 100 or height > 100:
            # im not a gfx api
            return []
        row = ["."] * (width + 2)
        floor = []
        for _ in range(height + 1):
            floor.append(row[:])
        for tile in red_tiles:
            floor[tile.y][tile.x] = "#"
        return floor

    def styled_floor(self, floor: list[list[str]], rect: Rectangle | None = None) -> str:
        lines = []
        for y, row in enumerate(floor):
            buffer = []
            for x, tile in enumerate(row):
                c = tile
                fg = None
                bg = None
                if rect and (pt := (x, y)) in rect:
                    c = "*"
                    bg = "red"
                    if rect.anchor_a == pt or rect.anchor_b == pt:
                        c = "@"
                        fg = "bright_white"
                elif tile == "#":
                    fg = "red"
                buffer.append(click.style(c, fg=fg, bg=bg))
            line = "".join(buffer)
            lines.append(line)
        return "\n".join(lines)


class Day9Part1(Day9):
    def parse_data(self, data: str) -> list[Point]:
        parsed_lines = [[int(v) for v in line.split(",")] for line in self.get_input_lines(data)]
        red_tiles = {Point(*line): True for line in parsed_lines}
        return list(red_tiles.keys())

    def solution(self, parsed_data: list[Point]) -> int:
        self.log("\n".join(str(pt) for pt in parsed_data))
        theater_floor = self.create_floor(parsed_data)
        print_floor = bool(theater_floor)
        self.log(self.styled_floor(theater_floor), condition=print_floor)
        self.print_divider()

        divider = self.create_divider()
        areas: dict[int, Rectangle] = {}
        for i, anchor_a in enumerate(parsed_data[:-1]):
            for anchor_b in parsed_data[i + 1 :]:
                self.log(anchor_a, anchor_b)
                rect = Rectangle(anchor_a, anchor_b)
                self.log(self.styled_floor(theater_floor, rect), condition=print_floor)
                self.log(divider, condition=print_floor)
                areas.setdefault(rect.area, rect)

        self.print_divider()
        largest_area = max(areas)
        largest_rect = areas[largest_area]
        self.log(self.styled_floor(theater_floor, largest_rect), condition=print_floor)
        return largest_area


class Day9Part2(Day9):
    def parse_data(self, data: str) -> None:
        pass

    def solution(self, parsed_data: None) -> None:
        pass

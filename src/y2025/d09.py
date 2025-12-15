import itertools
from operator import itemgetter

import shapely
from puzzle import Puzzle
from shapely import box
from shapely import Polygon
from utils import Point


class Day9(Puzzle):
    def parse_data(self, data: str) -> list[Point]:
        parsed_lines = [[int(v) for v in line.split(",")] for line in self.get_input_lines(data)]
        red_tiles = {Point(*line): True for line in parsed_lines}
        return list(red_tiles.keys())

    def _tile_area(self, polygon: Polygon) -> int:
        return int(polygon.area + (polygon.length / 2) + 1)


class Day9Part1(Day9):
    def solution(self, parsed_data: list[Point]) -> int:
        self.echo("\n".join(str(pt) for pt in parsed_data))
        self.echo_divider()

        rects = [
            (rect := box(a.x, a.y, b.x, b.y), self._tile_area(rect)) for a, b in itertools.combinations(parsed_data, 2)
        ]
        largest_rect, tile_area = next(reversed(sorted(rects, key=itemgetter(1))))
        return tile_area


class Day9Part2(Day9):
    def solution(self, parsed_data: list[Point]) -> int:
        self.echo("\n".join(str(pt) for pt in parsed_data))
        self.echo_divider()
        polygon = Polygon(parsed_data)
        max_area = self._tile_area(polygon)
        shapely.prepare(polygon)
        rects = [
            (rect := box(a.x, a.y, b.x, b.y), self._tile_area(rect)) for a, b in itertools.combinations(parsed_data, 2)
        ]
        for rect, tile_area in reversed(sorted(rects, key=itemgetter(1))):
            self.echo(f"testing {rect}={tile_area}")
            if tile_area > max_area:
                self.echo("too big")
                continue
            bounds = rect.bounds
            if bounds[0] == bounds[2] or bounds[1] == bounds[3]:
                self.echo("returning line")
                return tile_area
            if polygon.contains(rect):
                self.echo("solution found!")
                return tile_area
        raise ValueError("No solution found!")

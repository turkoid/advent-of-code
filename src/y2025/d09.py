import itertools
from operator import attrgetter

from puzzle import Puzzle
from utils import Line2D
from utils import Point
from utils import Rectangle


class TileRectangle(Rectangle):
    @property
    def width(self) -> int:
        return super().width + 1

    @property
    def height(self) -> int:
        return super().height + 1


class Day9(Puzzle):
    def parse_data(self, data: str) -> list[Point]:
        parsed_lines = [[int(v) for v in line.split(",")] for line in self.get_input_lines(data)]
        red_tiles = {Point(*line): True for line in parsed_lines}
        return list(red_tiles.keys())


class Day9Part1(Day9):
    def solution(self, parsed_data: list[Point]) -> int:
        self.echo("\n".join(str(pt) for pt in parsed_data))
        self.echo_divider()

        largest_rect = None
        for anchor_a, anchor_b in itertools.combinations(parsed_data, 2):
            self.echo(anchor_a, anchor_b)
            rect = TileRectangle(anchor_a, anchor_b)
            if largest_rect is None or rect.area > largest_rect.area:
                largest_rect = rect

        self.echo_divider()
        return largest_rect.area


class Day9Part2(Day9):
    def solution(self, parsed_data: list[Point]) -> int:
        self.echo("\n".join(str(pt) for pt in parsed_data))
        self.echo_divider()

        # find max area (shoelace)
        # use picks theorem to file the tile area
        # cache all vertical edges sorted by x
        # ignore rects with area > max area
        # ignore rects that encapsulates a point in the input
        # finally determine if the rect is inside or outside the polygon formed by the points
        # first rect to satisfy all conditions is a solution

        geometric_area = 0
        # use shoelace formula to determine the max possible area
        # find all intersections by x-axis and y-axis
        vertical_edges: dict[int, list[Line2D]] = {}
        perimeter = 0
        for i, anchor in enumerate(parsed_data):
            next_anchor = parsed_data[(i + 1) % len(parsed_data)]
            edge = Line2D(anchor, next_anchor)
            if edge.is_vertical():
                vertical_edges.setdefault(anchor.x, []).append(edge)
            geometric_area += (anchor.x * next_anchor.y) - (anchor.y * next_anchor.x)
            perimeter += abs(anchor.x - next_anchor.x) + abs(anchor.y - next_anchor.y)
        geometric_area = abs(geometric_area // 2)
        # picks theorem
        max_possible_area = geometric_area + (perimeter // 2) + 1
        self.echo(f"{geometric_area=} | {perimeter=} | {max_possible_area=}")
        vertical_edges = {x: sorted(vertical_edges[x], key=attrgetter("min_y")) for x in sorted(vertical_edges.keys())}

        rects: list[TileRectangle] = sorted(
            (TileRectangle(a, b) for a, b in itertools.combinations(parsed_data, 2)),
            key=attrgetter("area"),
            reverse=True,
        )
        largest_rect = None
        for rect in rects:
            self.echo(f"Testing {rect}: {rect.area}")
            if rect.top == rect.bottom or rect.left == rect.right:
                self.echo("it's a line")
                largest_rect = rect
                break
            if rect.area > max_possible_area:
                self.echo("too big")
                continue
            if any(rect.encapsulates(pt) for pt in parsed_data):
                self.echo("overlaps")
                continue
            intersections = {
                "tl": 0,
                "bl": 0,
                "tr": 0,
                "br": 0,
            }
            for x, edges in vertical_edges.items():
                if x > rect.left:
                    break
                tl_test_pt = Point(x, rect.top + 0.5)
                bl_test_pt = Point(x, rect.bottom - 0.5)
                for edge in edges:
                    if edge.contains(tl_test_pt):
                        intersections["tl"] += 1
                    if edge.contains(bl_test_pt):
                        intersections["bl"] += 1
            for x, edges in reversed(vertical_edges.items()):
                if x < rect.right:
                    break
                tr_test_pt = Point(x, rect.top + 0.5)
                br_test_pt = Point(x, rect.bottom - 0.5)
                for edge in edges:
                    if edge.contains(tr_test_pt):
                        intersections["tr"] += 1
                    if edge.contains(br_test_pt):
                        intersections["br"] += 1
            self.echo(f"{intersections=}")
            if any(cnt % 2 == 0 for cnt in intersections.values()):
                self.echo("not inside polygon")
                continue
            largest_rect = rect
            break

        self.echo(largest_rect)
        self.echo(largest_rect.width, largest_rect.height)
        return largest_rect.area if largest_rect else 0

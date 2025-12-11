from dataclasses import dataclass

import click
from puzzle import Puzzle
from utils import concat_string_lists


class Day5Part1(Puzzle):
    def parse_data(self, data: str) -> tuple[list[tuple[int, int]], list[int]]:
        groups = self.get_input_groups(data)
        fresh_ids = []
        for id_range in groups[0]:
            parsed_range = tuple(int(bound) for bound in id_range.split("-"))
            fresh_ids.append(parsed_range)

        ids = [int(i) for i in groups[1]]

        return fresh_ids, ids

    def solution(self, parsed_data: tuple[list[tuple[int, int]], list[int]]) -> int:
        fresh_ids, ids = parsed_data
        self.echo(f"{fresh_ids=}")
        self.echo(f"{ids=}")

        certified_fresh = 0
        for ingredient_id in ids:
            if any(lb <= ingredient_id <= ub for lb, ub in fresh_ids):
                certified_fresh += 1
        return certified_fresh


@dataclass
class StyledRange:
    lower_bound: int
    upper_bound: int
    diff: str = "=="

    @staticmethod
    def style_bound(bound: int, diff: str = "=") -> str:
        if diff == "+":
            color = "green"
        elif diff == "-":
            color = "red"
        elif diff == "~":
            color = "yellow"
        else:
            color = None

        return click.style(bound, fg=color)

    def render(self, lb_width: int = 0, ub_width: int = 0, include_diff: bool = False) -> str:
        lb_width = lb_width or len(str(self.lower_bound))
        ub_width = ub_width or len(str(self.upper_bound))
        lb_diff = s if include_diff and (s := self.diff[0]) in "+~-" else ""
        ub_diff = s if include_diff and (s := self.diff[1]) in "+~-" else ""
        lb_space = " " * (lb_width - len(lb_diff) - len(str(self.lower_bound)))
        ub_space = " " * (ub_width - len(ub_diff) - len(str(self.upper_bound)))
        styled_lb = StyledRange.style_bound(self.lower_bound, self.diff[0])
        styled_ub = StyledRange.style_bound(self.upper_bound, self.diff[1])

        return f"{lb_diff}{lb_space}{styled_lb}-{styled_ub}{ub_space}{ub_diff}"


class Day5Part2(Puzzle):
    def parse_data(self, data: str) -> list[tuple[int, int]]:
        groups = self.get_input_groups(data)
        fresh_ids = []
        for id_range in groups[0]:
            parsed_range = tuple(int(bound) for bound in id_range.split("-"))
            assert len(parsed_range) == 2 and parsed_range[0] <= parsed_range[1], f"{parsed_range=}"
            fresh_ids.append(parsed_range)
        return fresh_ids

    def _pretty_range(self, lower_bound: int, upper_bound: int) -> str:
        return f"{lower_bound}-{upper_bound}"

    def _pretty_ranges(self, ranges: list[tuple[int, int]]) -> str:
        formatted_ranges = ", ".join(self._pretty_range(lb, ub) for lb, ub in ranges)
        return f"[{formatted_ranges}]"

    def _update_ranges(
        self,
        ranges: list[tuple[int, int]],
        parsed_lower_bound: int,
        parsed_upper_bound: int,
        start_index: int,
        end_index,
    ) -> None:
        SR = StyledRange
        old_size = len(ranges)
        old_ranges: list[StyledRange | str]
        new_ranges: list[StyledRange | str]
        if start_index == end_index:
            old_ranges = [SR(lb, ub) for lb, ub in ranges]

            new_ranges = [SR(lb, ub) for lb, ub in ranges[:start_index]]
            new_ranges.append(SR(parsed_lower_bound, parsed_upper_bound, "++"))
            new_ranges.extend([SR(lb, ub) for lb, ub in ranges[end_index:]])

            ranges.insert(start_index, (parsed_lower_bound, parsed_upper_bound))
        else:
            old_lower_bound = ranges[start_index][0]
            old_upper_bound = ranges[end_index - 1][1]
            lower_bound = min(parsed_lower_bound, old_lower_bound)
            upper_bound = max(parsed_upper_bound, old_upper_bound)
            if end_index - start_index == 1 and lower_bound == old_lower_bound and upper_bound == old_upper_bound:
                return

            old_ranges = [SR(lb, ub) for lb, ub in ranges[:start_index]]
            old_ranges.append("-")
            old_ranges.extend([SR(lb, ub, "--") for lb, ub in ranges[start_index:end_index]])
            old_ranges.append("-")
            old_ranges.extend([SR(lb, ub) for lb, ub in ranges[end_index:]])

            new_ranges = [SR(lb, ub) for lb, ub in ranges[:start_index]]
            lb_diff = "=" if lower_bound == old_lower_bound else "+"
            ub_diff = "=" if upper_bound == old_upper_bound else "+"
            new_ranges.append(SR(lower_bound, upper_bound, f"{lb_diff}{ub_diff}"))
            new_ranges.extend([SR(lb, ub) for lb, ub in ranges[end_index:]])

            ranges[start_index:end_index] = [(lower_bound, upper_bound)]
        new_size = len(ranges)

        formatted_ranges = []
        for size, range_list in [(old_size, old_ranges), (new_size, new_ranges)]:
            lines = []
            widths = [len(str(size)) // 2 + 1]
            for sr in range_list:
                if isinstance(sr, StyledRange):
                    widths.append(len(str(sr.lower_bound)))
                    widths.append(len(str(sr.upper_bound)))
            bound_width = max(widths) + 2
            line_width = bound_width * 2 + 1
            lines.append(f"{size: ^{line_width}}")
            lines.append("=" * line_width)
            for sr in range_list:
                if isinstance(sr, StyledRange):
                    lines.append(sr.render(bound_width, bound_width, True))
                else:
                    lines.append(sr * line_width)
            lines.append("=" * line_width)
            formatted_ranges.append(lines)

        size_diff = new_size - old_size
        sign = "+" if size_diff >= 0 else ""
        middle = [f"{sign}{size_diff}"]
        middle.append("-" * len(middle[0]) + ">")

        diff = concat_string_lists(formatted_ranges[0], middle, formatted_ranges[1])
        self.echo(diff)

    def solution(self, parsed_data: list[tuple[int, int]]) -> int:
        LOWER_BOUND = 0
        UPPER_BOUND = 1
        divider = click.style(" " * 100, bg="blue")
        self.echo(f"parsed_data={self._pretty_ranges(parsed_data)}")
        self.echo(divider)
        fresh_id_ranges = []
        for parsed_lb, parsed_ub in parsed_data:
            self.echo(f"{self._pretty_range(parsed_lb, parsed_ub)}\n")
            start_index = 0
            end_index = 0
            for i, (fresh_lb, fresh_ub) in enumerate(fresh_id_ranges):
                if parsed_ub < fresh_lb:
                    break
                if fresh_lb <= parsed_ub <= fresh_ub:
                    end_index = i + 1
                    break
                if parsed_lb > fresh_ub:
                    start_index = i + 1
                    end_index = start_index
                    continue
                end_index = i + 1

            if (prev_index := start_index - 1) >= 0 and fresh_id_ranges[prev_index][UPPER_BOUND] + 1 == parsed_lb:
                start_index = prev_index
            if end_index < len(fresh_id_ranges) and fresh_id_ranges[end_index][LOWER_BOUND] - 1 == parsed_ub:
                end_index += 1
            self._update_ranges(fresh_id_ranges, parsed_lb, parsed_ub, start_index, end_index)
            self.echo(divider)

        self.echo(f"{fresh_id_ranges=}")
        certified_fresh = 0
        for lower_bound, upper_bound in fresh_id_ranges:
            certified_fresh += upper_bound - lower_bound + 1
        return certified_fresh

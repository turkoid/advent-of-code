from puzzle import Puzzle


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
        self.log(f"{fresh_ids=}")
        self.log(f"{ids=}")

        certified_fresh = 0
        for ingredient_id in ids:
            if any(lb <= ingredient_id <= ub for lb, ub in fresh_ids):
                certified_fresh += 1
        return certified_fresh


class Day5Part2(Puzzle):
    def parse_data(self, data: str) -> None:
        pass

    def solution(self, parsed_data: None) -> None:
        pass

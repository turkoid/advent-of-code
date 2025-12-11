import functools
import itertools
import math
import operator

from puzzle import Puzzle


class Day2Part1(Puzzle):
    def parse_data(self, data: str) -> list[tuple[int, int]]:
        input_data = self.get_flat_input(data)
        ranges = input_data.split(",")
        parsed_ranges = []
        for _range in ranges:
            lower_bound, upper_bound = _range.split("-")
            parsed_range = (int(lower_bound.strip()), int(upper_bound.strip()))
            parsed_ranges.append(parsed_range)
        return parsed_ranges

    def solution(self, parsed_data: list[tuple[int, int]]) -> int:
        invalid_id_sum = 0
        for lower_bound, upper_bound in parsed_data:
            for id in range(lower_bound, upper_bound + 1):
                id_str = str(id)
                if len(id_str) % 2 != 0:
                    continue
                mid = int(len(id_str) / 2)
                left = id_str[:mid]
                right = id_str[mid:]
                if left == right:
                    invalid_id_sum += id
        return invalid_id_sum


class Day2Part2(Puzzle):
    def parse_data(self, data: str) -> list[tuple[str, str]]:
        input_data = self.get_flat_input(data)
        ranges = input_data.split(",")
        parsed_ranges = []
        for _range in ranges:
            lower_bound, upper_bound = _range.split("-")
            parsed_range = (lower_bound.strip(), upper_bound.strip())
            parsed_ranges.append(parsed_range)
        return parsed_ranges

    def _find_seq_bound(self, seq_size: int, id_size: int, bound: str, is_lower: bool) -> int:
        if id_size != len(bound):
            seq_bound = 10 ** (seq_size - 1) if is_lower else 10**seq_size - 1
            return seq_bound
        seq_bound = int(bound[:seq_size])
        for batch in itertools.batched(bound[seq_size:], seq_size):
            grp = int("".join(batch))
            if grp == seq_bound:
                continue
            if is_lower:
                if grp > seq_bound:
                    seq_bound += 1
                break
            else:
                if grp < seq_bound:
                    seq_bound -= 1
                break
        if len(str(seq_bound)) != seq_size:
            seq_bound = -1
        return seq_bound

    def solution(self, parsed_data: list[tuple[str, str]]) -> int:
        invalid_id_sum = 0
        for lower_bound, upper_bound in parsed_data:
            self.echo(f"### id_range=[{lower_bound}-{upper_bound}]")
            cache = {}
            min_id_size = len(lower_bound)
            max_id_size = len(upper_bound)
            max_seq_size = int(max_id_size / 2)

            for seq_size in range(1, max_seq_size + 1):
                min_group_count = max(math.ceil(min_id_size / seq_size), 2)
                max_group_count = int(max_id_size / seq_size)
                for group_count in range(min_group_count, max_group_count + 1):
                    id_size = seq_size * group_count
                    seq_start = self._find_seq_bound(seq_size, id_size, lower_bound, True)
                    seq_end = self._find_seq_bound(seq_size, id_size, upper_bound, False)
                    if seq_start > seq_end:
                        continue
                    self.echo(
                        f"{seq_size}x{group_count}: invalid_id_range=[{str(seq_start) * group_count}-{str(seq_end) * group_count}]"
                    )
                    for seq in range(seq_start, seq_end + 1):
                        invalid_id = int(str(seq) * group_count)
                        if invalid_id in cache:
                            self.echo(f"skipping cached id: {invalid_id}")
                        else:
                            cache[invalid_id] = True
                            self.echo(f"+{invalid_id=}")
                            invalid_id_sum += invalid_id
        return invalid_id_sum


def brute_force(lower_bound, upper_bound):
    invalid_ids = []
    for id in range(lower_bound, upper_bound + 1):
        id_str = str(id)
        mid = int(len(id_str) / 2)
        ub = id_str[:mid]
        for i in range(1, int(ub) + 1):
            i_str = str(i)
            invalid_id = i_str * int(len(id_str) / len(i_str))
            if id_str == invalid_id:
                invalid_ids.append(int(invalid_id))
                break
    print(f"invalid id count: {len(invalid_ids)}")
    print(f"invalid id sum: {functools.reduce(operator.add, invalid_ids)}")


if __name__ == "__main__":
    brute_force(12, 8080)

from templates.puzzle import Puzzle


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

    def _find_possible_sequence_sizes(self, bound: str) -> list[int]:
        sizes = [n for n in range(1, int(len(bound) / 2) + 1) if len(bound) % n == 0]
        return sizes

    def solution(self, parsed_data: list[tuple[str, str]]) -> int:
        pass


if __name__ == "__main__":
    lower_bound = 1010
    upper_bound = 808080
    invalid_id_count = 0
    for id in range(lower_bound, upper_bound + 1):
        id_str = str(id)
        mid = int(len(id_str) / 2)
        ub = id_str[:mid]
        for i in range(1, int(ub) + 1):
            i_str = str(i)
            invalid_id = i_str * int(len(id_str) / len(i_str))
            if id_str == invalid_id:
                print(id)
                invalid_id_count += 1
                break
    # for id in invalid_ids:
    #     print(id)
    print(invalid_id_count)

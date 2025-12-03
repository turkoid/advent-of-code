from templates.puzzle import Puzzle


class Day3Part1(Puzzle):
    def parse_data(self, data: str) -> list[list[int]]:
        banks = self.get_input_lines(data)
        return [[int(battery) for battery in bank] for bank in banks]

    def _find_highest_voltage(self, batteries: list[int]) -> tuple[int, int]:
        index = 0
        voltage = 0
        for i, battery in enumerate(batteries):
            if battery > voltage:
                index = i
                voltage = battery
            if voltage == 9:
                break
        return index, voltage

    def solution(self, parsed_data: list[list[int]]) -> int:
        total_voltage = 0
        for bank in parsed_data:
            first_index, first_voltage = self._find_highest_voltage(bank[:-1])
            _, second_voltage = self._find_highest_voltage(bank[:first_index:-1])
            bank_voltage = int(f"{first_voltage}{second_voltage}")
            total_voltage += bank_voltage
        return total_voltage


class Day3Part2(Day3Part1):
    def solution(self, parsed_data: list[str]) -> int:
        pass

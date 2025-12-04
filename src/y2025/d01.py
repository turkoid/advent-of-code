from puzzle import Puzzle


class Day1Part1(Puzzle[list[int], int]):
    def parse_data(self, data: str) -> list[int]:
        instructions = self.get_input_lines(data)
        rotations = []
        for instruction in instructions:
            direction = instruction[0]
            distance = int(instruction[1:])
            rotations.append(distance if direction == "R" else -distance)
        return rotations

    def solution(self, parsed_data: list[int]) -> int:
        dial = 50
        zero_click = 0
        for rotation in parsed_data:
            dial += rotation
            dial %= 100
            if dial == 0:
                zero_click += 1
        return zero_click


class Day1Part2(Day1Part1):
    def solution(self, parsed_data: list[int]) -> int:
        dial = 50
        zero_click = 0
        for rotation in parsed_data:
            full_rotations = int(rotation / 100)
            zero_click += abs(full_rotations)
            rotation -= full_rotations * 100
            if rotation == 0:
                continue
            dial += rotation
            if dial != rotation and (dial <= 0 or dial >= 100):
                zero_click += 1
            dial %= 100
        return zero_click

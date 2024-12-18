class Puzzle:
    def __init__(self, day: int):
        self.day = day

    def get_lines(self) -> list[str]:
        with open(f"../input/y2024/d{self.day:02}.in") as f:
            data = f.read()
        lines = [line.strip() for line in data.splitlines() if line]
        return lines

    def solve(self) -> None:
        lines = self.get_lines()
        left_list: list[int] = []
        right_list: list[int] = []
        for line in lines:
            left, right = line.split()
            left_list.append(int(left))
            right_list.append(int(right))
        left_list.sort()
        right_list.sort()
        total_distance = 0
        for left, right in zip(left_list, right_list):
            distance = abs(left - right)
            total_distance += distance
        print(total_distance)


if __name__ == "__main__":
    Puzzle(1).solve()

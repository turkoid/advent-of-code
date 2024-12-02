class Puzzle:
    def __init__(self, day: int):
        self.day = day

    def get_lines(self) -> list[str]:
        with open(f"inputs/d{self.day:02}.in") as f:
            data = f.read()
        lines = [line.strip() for line in data.splitlines() if line.strip()]
        return lines

    def solve(self) -> None:
        lines = self.get_lines()
        num_occurences: dict[int, dict[str, int]] = {}
        default = {"left": 0, "right": 0}
        for line in lines:
            left, right = line.split()
            num_occurences.setdefault(int(left), default.copy())["left"] += 1
            num_occurences.setdefault(int(right), default.copy())["right"] += 1
        total_score = 0
        for num, occurrences in num_occurences.items():
            left = occurrences["left"]
            right = occurrences["right"]
            similarity_score = num * right * left
            total_score += similarity_score
        print(total_score)


if __name__ == "__main__":
    Puzzle(1).solve()

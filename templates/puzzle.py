class Puzzle:
    def __init__(self, day: int):
        self.day = day

    def get_lines(self) -> list[str]:
        with open(f"inputs/d{self.day:02}.in") as f:
            data = f.read()
        lines = [line.strip() for line in data.splitlines() if line]
        return lines

    def solve(self) -> None:
        lines = self.get_lines()
        for line in lines:
            print(line)


if __name__ == "__main__":
    Puzzle(0).solve()

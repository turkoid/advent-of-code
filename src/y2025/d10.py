import operator
from dataclasses import dataclass
from functools import reduce
from itertools import combinations
from typing import Literal

from puzzle import Puzzle


@dataclass
class Machine:
    diagram: int
    size: int
    buttons: list[int]
    joltages: list[int]

    def visualize(self, style: Literal["binary", "int", "human"] = "binary") -> str:
        _joltages = ",".join(str(v) for v in self.joltages)

        if style == "int":
            _diagram = self.diagram
            _buttons = self.buttons
        else:
            _diagram = f"{self.diagram:0{self.size}b}"
            _buttons = [f"({btn:0{self.size}b})" for btn in self.buttons]
            if style == "human":
                _diagram = _diagram.replace("0", ".").replace("1", "#")
                _buttons = [b.replace("0", ".").replace("1", "#") for b in _buttons]

        _buttons = " ".join(f"{i}={b}" for i, b in enumerate(_buttons))
        return f"[{_diagram}] {_buttons} {{{_joltages}}}"

    def __repr__(self) -> str:
        return self.visualize()


class Day10(Puzzle):
    def parse_data(self, data: str) -> list[Machine]:
        lines: list[str] = self.get_input_lines(data)
        machines = []
        for line in lines:
            parts = line.split()
            diagram = parts[0][1:-1].replace(".", "0").replace("#", "1")
            size = len(diagram)
            buttons = []
            for button in parts[1:-1]:
                button_wiring = button[1:-1].split(",")
                button_flag = reduce(operator.add, (2 ** (size - int(b) - 1) for b in button_wiring))
                buttons.append(button_flag)
            joltages = [int(v) for v in parts[-1][1:-1].split(",")]
            machine = Machine(int(diagram, 2), size, buttons, joltages)
            machines.append(machine)
        return machines


class Day10Part1(Day10):
    def find_combo(self, machine: Machine) -> tuple[int, ...]:
        for size in range(1, len(machine.buttons) + 1):
            for buttons in combinations(machine.buttons, size):
                if machine.diagram == reduce(operator.xor, buttons):
                    return buttons
        raise ValueError(f"No combination found for {machine}")

    def solution(self, parsed_data: list[Machine]) -> int:
        self.echo("\n".join(m.visualize("binary") for m in parsed_data))

        button_seq = []
        for machine in parsed_data:
            buttons = self.find_combo(machine)
            indexed_buttons = [machine.buttons.index(btn) for btn in buttons]
            button_seq.append(buttons)
            self.echo(f"Press {indexed_buttons} for {machine}")
        return reduce(operator.add, [len(seq) for seq in button_seq])


class Day10Part2(Day10):
    def solution(self, parsed_data: None) -> None:
        raise NotImplementedError

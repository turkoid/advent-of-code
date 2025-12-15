from dataclasses import dataclass

import click
from puzzle import Puzzle


@dataclass
class Device:
    name: str
    outputs: list[str]


class Day11(Puzzle):
    def parse_data(self, data: str) -> dict[str, Device]:
        lines = self.get_input_lines(data)
        devices = {}
        for line in lines:
            name, outputs = line.split(":")
            devices[name] = Device(name, outputs.split())
        return devices


class Day11Part1(Day11):
    def solution(self, parsed_data: dict[str, Device]) -> int:
        self.echo_lines(list(parsed_data.values()))

        paths: list[list[str]] = []
        queue = [[output] for output in reversed(parsed_data["you"].outputs)]
        while queue:
            path = queue.pop()
            for output in reversed(parsed_data[path[-1]].outputs):
                if output == "you":
                    self.echo("feedback loop")
                    continue
                if output == "out":
                    paths.append(path)
                else:
                    branch = path[:]
                    branch.append(output)
                    queue.append(branch)
        self.echo_divider()
        self.echo(
            "\n".join(
                f"{click.style('you', fg='green')}--{'--'.join(path)}--{click.style('out', fg='red')}" for path in paths
            )
        )
        return len(paths)


class Day11Part2(Day11):
    def solution(self, parsed_data: None) -> None:
        raise NotImplementedError

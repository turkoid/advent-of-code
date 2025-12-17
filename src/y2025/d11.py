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
        # self.echo_lines(list(parsed_data.values()))

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
    def find_paths(
        self, device: str, devices: dict[str, Device], cache: dict[str, dict[str, int] | None]
    ) -> dict[str, int]:
        if device == "out":
            return {"out": 1}
        if device in cache:
            if cache[device] is None:
                raise ValueError("feedback loop")
            return cache[device]
        cache[device] = None
        device_paths = {
            "out": 0,
            "fft": 0,
            "dac": 0,
            "valid": 0,
        }
        for output in devices[device].outputs:
            output_paths = self.find_paths(output, devices, cache)
            for key in device_paths:
                device_paths[key] += output_paths.get(key, 0)
            for key, other_key in [("fft", "dac"), ("dac", "fft")]:
                if device == key:
                    device_paths[key] += output_paths["out"]
                    device_paths["valid"] += output_paths[other_key]
        cache[device] = device_paths
        return device_paths

    def solution(self, parsed_data: dict[str, Device]) -> int:
        self.echo_lines(list(parsed_data.values()))

        paths = self.find_paths("svr", parsed_data, {})
        return paths["valid"]

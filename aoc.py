import re
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

import click


def strip_code(code: str) -> str:
    code = code.strip(" ").strip("\n")
    lines = code.splitlines()
    left_margin = 0
    for i, c in enumerate(lines[0]):
        if c != " ":
            left_margin = i
            break
    if left_margin > 0:
        lines = [line[left_margin:] for line in lines]
        code = "\n".join(lines)
    return code


class AdventOfCode:
    def __init__(self, year: int, day: int | None, parts: int):
        self.year = year
        self.day = day
        self.parts = parts

    @staticmethod
    def formatted_year(year: int) -> str:
        return f"y{year:04}"

    @staticmethod
    def formatted_day(day: int) -> str:
        return f"d{day:02}"

    @staticmethod
    def formatted_part(part: int) -> str:
        return f"p{part:02}"

    @staticmethod
    def puzzle_class(day: int, part: int) -> str:
        return f"Day{day}Part{part}"

    @staticmethod
    def puzzle_module(year: int, day: int, part: int | None = None) -> str:
        module = [
            AdventOfCode.formatted_year(year),
            AdventOfCode.formatted_day(day),
        ]
        if part is not None:
            module.append(AdventOfCode.formatted_part(part))
        return ".".join(module)

    def generate_day_content(self) -> str:
        BASE_CLASS = "Puzzle"
        content = list()
        content.append(f"from puzzle import {BASE_CLASS}")
        content.append("")
        content.append("")
        for i in range(self.parts):
            part = i + 1
            day_code = f"""
                class {AdventOfCode.puzzle_class(self.day, part)}({BASE_CLASS}):
                    def parse_data(self, data: str) -> None:
                        pass

                    def solution(self, parsed_data: None) -> None:
                        pass
            """
            content.append(strip_code(day_code))
            content.append("")
            content.append("")
        return "\n".join(content)

    def generate_runner_content(self) -> str:
        runner_code = f"""
            from runner import Runner

            if __name__ == '__main__':
                data = '''

                '''

                runner= Runner({self.year}, {self.day}, {self.parts})
                runner.add_test(1, data, None)
                runner.run()
        """
        content = f"{strip_code(runner_code)}\n"
        return content

    def generate_file(self, path: Path, content_gen: Callable[[], str] | None = None) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        if content_gen:
            content = content_gen()
            path.write_text(content)
        else:
            path.touch()
        click.echo(f"Generated {path}")

    def sunrise(self) -> None:
        if self.year <= 0:
            raise click.ClickException("If you really think about it, Advent-of-Code could not exist before 1 AD")

        year_pkg = AdventOfCode.formatted_year(self.year)
        io_year = Path("io").joinpath(year_pkg)
        src_year = Path("src").joinpath(year_pkg)

        if self.day is None:
            for entry in reversed(sorted(list(src_year.iterdir()))):
                if entry.is_dir():
                    continue
                if match := re.match(r"d(\d+)\.py", entry.name):
                    self.day = int(match.group(1)) + 1
                    break
        self.day = self.day or 1
        if self.day < 1:
            raise click.ClickException("On the zeroth day, God created light, doesn't quite have the same ring to it")
        if self.day > 25:
            raise click.ClickException("Nothing can exist after December 25!")

        day_file_without_ext = AdventOfCode.formatted_day(self.day)
        input_path = io_year.joinpath("input", f"{day_file_without_ext}.in")
        day_path = src_year.joinpath(f"{day_file_without_ext}.py")
        runner_path = io_year.joinpath("runner", f"runner_{day_file_without_ext}.py")

        for path in [input_path, day_path, runner_path]:
            if path.exists():
                raise click.ClickException(f"{path} already exists!")

        click.echo(f"Generating Year {self.year}, Day {self.day}, {self.parts} Parts...")
        if click.confirm("Do you want to continue?", default=True):
            self.generate_file(input_path)
            self.generate_file(day_path, self.generate_day_content)
            self.generate_file(runner_path, self.generate_runner_content)
            click.echo("Have fun!")


@click.command()
@click.option("-y", "--year", "year", type=int, default=datetime.now().year)
@click.argument("day", required=False, default=None, type=int)
@click.option("-p", "--parts", "parts", type=int, default=2)
def cli(year: int, day: int | None, parts: int) -> None:
    new_day = AdventOfCode(year, day, parts)
    new_day.sunrise()


if __name__ == "__main__":
    cli()

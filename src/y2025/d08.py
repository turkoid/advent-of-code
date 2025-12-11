import math
import operator
from functools import reduce
from operator import itemgetter
from typing import NamedTuple
from typing import Self

from puzzle import Puzzle
from utils import Color


class Point3D(NamedTuple):
    x: int
    y: int
    z: int

    def __repr__(self) -> str:
        return f"[{self.x}, {self.y}, {self.z}]"

    def sort_distance(self, other_point: Self) -> int:
        x2 = (other_point.x - self.x) ** 2
        y2 = (other_point.y - self.y) ** 2
        z2 = (other_point.z - self.z) ** 2
        return x2 + y2 + z2

    def distance(self, other_point: Self) -> float:
        _distance = math.sqrt(self.sort_distance(other_point))
        return _distance


class Day8(Puzzle):
    def _styled_junctions(self, *junctions: Point3D) -> str:
        return "->".join(Color.cyan(j) for j in junctions)

    def _styled_circuit(self, circuit: dict[Point3D, bool]) -> str:
        return self._styled_junctions(*circuit.keys())

    def get_distances(self, points: list[Point3D]) -> list[tuple[int, tuple[Point3D, Point3D]]]:
        distances = []
        for i, junction_a in enumerate(points[:-1]):
            for junction_b in points[i + 1 :]:
                distance = junction_a.sort_distance(junction_b)
                distances.append((distance, (junction_a, junction_b)))
        return distances

    def make_connection(
        self,
        connection: int,
        connected_junctions: dict[Point3D, dict[Point3D, bool]],
        junction_a: Point3D,
        junction_b: Point3D,
    ):
        self.echo(f"Making connection {Color.highlight(connection)}: {self._styled_junctions(junction_a, junction_b)}")
        circuit_a = connected_junctions.get(junction_a, None)
        circuit_b = connected_junctions.get(junction_b, None)
        if circuit_a is None and circuit_b is None:
            self.echo("++ New circuit!")
            circuit = {junction_a: True, junction_b: True}
            connected_junctions[junction_a] = circuit
            connected_junctions[junction_b] = circuit
        elif circuit_a is circuit_b:
            self.echo("== Both junctions in same circuit")
        elif circuit_a and circuit_b:
            self.echo(f">< Merging 2 circuits: {self._styled_circuit(circuit_a)}+{self._styled_circuit(circuit_b)}")
            circuit_a.update(circuit_b)
            for junction in circuit_a:
                connected_junctions[junction] = circuit_a
        else:
            params = [
                (circuit_a, junction_b),
                (circuit_b, junction_a),
            ]
            for circuit, new_junction in params:
                if circuit:
                    self.echo(f">> Adding {Color.cyan(new_junction)} to {self._styled_circuit(circuit)}")
                    circuit[new_junction] = True
                    connected_junctions[new_junction] = circuit


class Day8Part1(Day8):
    def parse_data(self, data: str) -> tuple[list[Point3D], int]:
        raw_points, connections = self.get_input_groups(data)
        assert len(connections) == 1
        points = [Point3D(*[int(n) for n in coords.split(",")]) for coords in raw_points]
        return points, int(connections[0])

    def solution(self, parsed_data: tuple[list[Point3D], int]) -> int:
        points, max_connections = parsed_data
        self.echo("\n".join(str(pt) for pt in points))
        self.echo(f"{max_connections=}")
        self.echo_divider()

        distances = self.get_distances(points)

        connected_junctions: dict[Point3D, dict[Point3D, bool]] = {}
        for conn, (_, (junction_a, junction_b)) in enumerate(sorted(distances)[:max_connections], start=1):
            self.make_connection(conn, connected_junctions, junction_a, junction_b)
        self.echo_divider()

        circuits = []
        for circuit in connected_junctions.values():
            if circuit not in circuits:
                circuits.append(circuit)
        circuits = sorted(circuits, key=len, reverse=True)
        self.echo("\n".join(f"{len(c)}: {self._styled_circuit(c)}" for c in circuits))
        largest_three_circuits = [len(circuits[i]) if i < len(circuits) else 1 for i in range(3)]
        return reduce(operator.mul, largest_three_circuits)


class Day8Part2(Day8):
    def parse_data(self, data: str) -> list[Point3D]:
        raw_points, _ = self.get_input_groups(data)
        points = [Point3D(*[int(n) for n in coords.split(",")]) for coords in raw_points]
        return points

    def solution(self, parsed_data: list[Point3D]) -> int:
        self.echo("\n".join(str(pt) for pt in parsed_data))
        self.echo_divider()

        distances = self.get_distances(parsed_data)

        connected_junctions = {}
        for conn, (_, (junction_a, junction_b)) in enumerate(sorted(distances, key=itemgetter(0)), start=1):
            self.make_connection(conn, connected_junctions, junction_a, junction_b)
            if len(connected_junctions) == len(parsed_data) - 1:
                break

        self.echo_divider()
        free_junction = None
        for junction in parsed_data:
            if junction not in connected_junctions:
                free_junction = junction
                break
        final_distances = [(free_junction.sort_distance(junction), junction) for junction in connected_junctions]
        final_distances = sorted(final_distances, key=itemgetter(0))
        connect_junction = final_distances[0][1]
        self.echo(f"Final connection {self._styled_junctions(free_junction, connect_junction)}")

        return free_junction.x * connect_junction.x

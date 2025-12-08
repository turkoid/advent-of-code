import math
import operator
from functools import reduce
from typing import NamedTuple
from typing import Self

from puzzle import Puzzle


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


class Day8Part1(Puzzle):
    def parse_data(self, data: str) -> tuple[list[Point3D], int]:
        raw_points, connections = self.get_input_groups(data)
        assert len(connections) == 1
        points = [Point3D(*[int(n) for n in coords.split(",")]) for coords in raw_points]
        return points, int(connections[0])

    def _styled_junctions(self, *junctions: Point3D) -> str:
        return "->".join(self.cyan(j) for j in junctions)

    def _styled_circuit(self, circuit: dict[Point3D, bool]) -> str:
        return self._styled_junctions(*circuit.keys())

    def solution(self, parsed_data: tuple[list[Point3D], int]) -> int:
        points, max_connections = parsed_data
        self.log("\n".join(str(pt) for pt in points))
        self.log(f"{max_connections=}")
        self.print_divider()

        distances: list[tuple[int, tuple[Point3D, Point3D]]] = []
        for i, junction_a in enumerate(points[:-1]):
            for junction_b in points[i + 1 :]:
                distance = junction_a.sort_distance(junction_b)
                distances.append((distance, (junction_a, junction_b)))

        connected_junctions: dict[Point3D, dict[Point3D, bool]] = {}
        for conn, (_, (junction_a, junction_b)) in enumerate(sorted(distances)[:max_connections], start=1):
            self.log(f"Making connection {self.highlight(conn)}: {self._styled_junctions(junction_a, junction_b)}")
            circuit_a = connected_junctions.get(junction_a, None)
            circuit_b = connected_junctions.get(junction_b, None)
            if circuit_a is None and circuit_b is None:
                self.log("++ New circuit!")
                circuit = {junction_a: True, junction_b: True}
                connected_junctions[junction_a] = circuit
                connected_junctions[junction_b] = circuit
            elif circuit_a is circuit_b:
                self.log("== Both junctions in same circuit")
            elif circuit_a and circuit_b:
                self.log(f">< Merging 2 circuits: {self._styled_circuit(circuit_a)}+{self._styled_circuit(circuit_b)}")
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
                        self.log(f">> Adding {self.cyan(new_junction)} to {self._styled_circuit(circuit)}")
                        circuit[new_junction] = True
                        connected_junctions[new_junction] = circuit
        self.print_divider()

        circuits = []
        for circuit in connected_junctions.values():
            if circuit not in circuits:
                circuits.append(circuit)
        circuits = sorted(circuits, key=len, reverse=True)
        self.log("\n".join(f"{len(c)}: {self._styled_circuit(c)}" for c in circuits))
        largest_three_circuits = [len(circuits[i]) if i < len(circuits) else 1 for i in range(3)]
        return reduce(operator.mul, largest_three_circuits)


class Day8Part2(Day8Part1):
    pass

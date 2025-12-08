### Advent of Code

This repo contains solutions, utilities, and small helpers for Advent of Code puzzles

#### Stack
- Language: Python (>= 3.12)
- Package/config: `pyproject.toml`
- Package manager: `uv`

---

### Requirements
- Python 3.12 or newer
- uv — https://docs.astral.sh/uv/

---

### Installation

```
uv sync --dev
```

Add git submodule where test data and confirmed solutions are stored:
```
git submodule add <repository-url> io
```

---

### Project structure
```
.
├─ pyproject.toml            # Project metadata and dependencies
├─ aoc.py                    # CLI to generate ("sunrise") new day files
├─ src/
│  ├─ puzzle.py              # Base Puzzle class and helpers
│  ├─ runner.py              # Generic Runner to execute parts/tests
│  ├─ y{year}/               # {year} files (file per day or file per day-part)
├─ io/                       # git submodule pointing a another repo (preferrably private)
│  ├─ README.md
│  ├─ y{year}/
│     ├─ input/              # Inputs for {year} (dXX.in)
│     └─ runner/             # Small scripts to run specific days
```

Puzzle discovery layout:
- Module path for a puzzle: `src/yYYYY/dXX.py`
- Class names must be `Day{X}Part{P}` (e.g., `Day8Part1`) so the runner can import them.
- Inputs live under `io/yYYYY/input/` as `dXX.in` or `dXXpYY.in`.

---

### Usage

1) Generate a new day

All options/arguments default to current year, next available day, and 2 parts

The generator asks for confirmation before creating files.
```
uv run aoc.py                                       # generate next missing day with 2 parts for the current year
uv run python aoc.py --year 2025 --parts 3          # generate next missing day with 3 parts for year 2025
uv run python aoc.py --year 2025 8                  # generate a specific day and year
```

This creates:
- `io/yYYYY/input/dXX.in` (empty input file)
- `src/yYYYY/dXX.py` (class stubs: `Day{X}Part1`, `Day{X}Part2`)
- `io/yYYYY/runner/runner_dXX.py` (a tiny runner script)

2) Put your puzzle input in place
- Save your input to `io/yYYYY/input/dXX.in` (or `dXXpYY.in` if you keep separate inputs per part).

3) Implement solutions
- Edit `src/yYYYY/dXX.py`. Each class must implement:
  - `parse_data(self, data: str) -> Any`
  - `solution(self, parsed_data: Any) -> Any`

Helper methods available on `Puzzle`:
- `get_puzzle_input()` reads the correct `io/yYYYY/input/dXX[pxx].in` automatically.
- `get_input_lines`, `get_input_groups`, `get_flat_input`, `get_input_grid` to parse inputs.
- `log`, `echo`, `create_header`, and test helpers.

4) Run a day/part

Use the generated per-day runner script:
```
uv run python io/y2025/runner/runner_d08.py
```
---

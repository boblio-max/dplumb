# dplumb

dplumb is a small Python module that defines `Field`/`Int`/`Str`/`Pipe` data-validation primitives and a lazy streaming interface that can also materialize results into a Polars `DataFrame`. It is a one-file utility — a `Pipe` validates a dict-of-dicts payload through a schema of `Field` instances, gracefully handling case-insensitive key matching for messy source data.

## Build / Test / Lint Commands

- Install: `pip install polars` (only needed if you call `pipe.to_polars()`); the core module is pure stdlib
- Build: not applicable
- Test: no automated tests; verify by importing the module and exercising `Pipe.drain(...).to_list()`
- Lint: not configured
- Dev / run: `python -c "from main import Pipe, Int, Str; print(Pipe({'a': Int()}).drain([{'a':'1'}]).to_list())"`

## Code Style Rules

- Language/version: Python 3.10+
- Paradigm: simple class hierarchy (`Field` base, `Int`/`Str` subclasses, `Pipe` as the validator/streamer)
- Types: explicit — `typing.List`, `typing.Dict`, `typing.Any`, `typing.Generator`
- Formatting: PEP 8 (no formatter configured)
- Imports / module style: `from typing import ...` at the top; lazy `import polars as pl` inside `to_polars()` to keep the dependency optional
- Dependencies: standard library only unless `to_polars()` is exercised (then `polars`)

## Verification Criteria

Before claiming any task done, Claude MUST:
1. Run `python -c "import main"` to confirm the module imports cleanly.
2. Smoke-test `Pipe({'a': Int()}).drain([{'A': '7'}]).to_list()` and confirm the result is `[{'a': 7}]` (case-insensitive key resolution).
3. If `to_polars()` is exercised, ensure `polars` is installed and the import succeeds.
4. Report the exact commands run and their outcomes in the final message.

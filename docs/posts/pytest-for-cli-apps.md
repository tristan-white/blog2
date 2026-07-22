---
date: 2026-07-22
---

# Using pytest to Catch CLI Changes

When building CLI apps, it's important to update the major/minor version when the CLI changes (see the [semantic versioning](https://semver.org/) philosophy).

How can we ensure we catch these changes with [pytest](https://pytest.org/)?

[syrupy](https://syrupy-project.github.io/syrupy/) is a great solution.

Let's look at an example for a python CLI that uses [typer](https://typer.tiangolo.com/):

```python title="tests/test_cli.py"
import pytest
import typer
from tpyer.testing import CliRunner
from myapp.cli import app

runner = CliRunner()
commands = list(typer.main.get_group(app).commands.keys())

@pytest.mark.parametrize("cmd", commands)
def test_cli(snapshot, cmd: str):
result = runner.invoke(app, [cmd, "--help"], env={"COLUMNS": "120"})
assert result.exit_code == 0
assert result.stdout == snapshot
```

Now run `pytest --snapshot-update`.

This will automatically take whatever you compared `snapshot` to (in this case `result.stdout`) and create a copy of that in your `tests` directory. Now when you run `pytest`, it compares it to these snapshots.

Whever the CLI changes, it will fail this test until you run `pytest --snapshot-update` again.


*[CLI]: Command Line Interface 

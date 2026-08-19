"""The --version flag exists for the HEG-406 monthly dependency audit: an
installed CLI must be diffable against upstream, which needs a
machine-readable version on stdout."""

from typer.testing import CliRunner

from daiso_cli import __version__
from daiso_cli.main import app

runner = CliRunner()


def test_version_flag_prints_name_and_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.output.strip() == f"daiso-cli {__version__}"


def test_version_matches_pyproject() -> None:
    """__init__ and pyproject drift silently otherwise — one source of truth
    is pyproject, and __version__ must mirror it."""
    import pathlib
    import tomllib

    pyproject = tomllib.loads(
        (pathlib.Path(__file__).parent.parent / "pyproject.toml").read_text()
    )
    assert __version__ == pyproject["project"]["version"]


def test_bare_invocation_still_prints_the_banner() -> None:
    """The eager option must not swallow the no-subcommand banner path."""
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "Daiso CLI" in result.output

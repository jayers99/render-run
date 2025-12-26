"""CLI integration tests."""

import json
from pathlib import Path

from typer.testing import CliRunner

from render_run.cli import app


def test_help_shows_commands(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "hello" in result.output
    assert "expand" in result.output


def test_hello_default(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output


def test_expand_placeholder(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["expand", "a cozy cabin in snow"])
    assert result.exit_code == 0
    assert "cozy cabin" in result.output


def test_prepare_writes_manifest_and_expanded_prompts(cli_runner: CliRunner) -> None:
    with cli_runner.isolated_filesystem():
        prompts_path = Path("prompts.txt")
        prompts_path.write_text("# comment\n\nfirst idea\nsecond idea\n", encoding="utf-8")

        out_dir = Path("out")
        result = cli_runner.invoke(
            app,
            [
                "prepare",
                "--in",
                str(prompts_path),
                "--out",
                str(out_dir),
                "--providers",
                "dalle,gemini",
            ],
        )
        assert result.exit_code == 0

        manifest_path = out_dir / "manifest.json"
        expanded_path = out_dir / "expanded_prompts.txt"
        assert manifest_path.exists()
        assert expanded_path.exists()

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["schema_version"] == "0.1"
        assert manifest["expand_prompts"] is True
        assert len(manifest["items"]) == 2
        assert manifest["items"][0]["idea"] == "first idea"
        assert manifest["items"][0]["providers"] == ["dalle", "gemini"]

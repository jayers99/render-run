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
    assert "prepare" in result.output
    assert "generate" in result.output


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
                "--domain",
                "create",
                "--project",
                "xmas-cards-2025",
                "--run-id",
                "test-run",
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
        assert manifest["domain"] == "create"
        assert manifest["project"] == "xmas-cards-2025"
        assert manifest["run_id"] == "test-run"


def test_generate_requires_provider_env_template(cli_runner: CliRunner) -> None:
    with cli_runner.isolated_filesystem():
        out_dir = Path("run")
        out_dir.mkdir(parents=True)
        manifest = {
            "schema_version": "0.1",
            "created_at": "2025-01-01T00:00:00Z",
            "input_file": "prompts.txt",
            "out_dir": str(out_dir),
            "expand_prompts": True,
            "items": [{"id": 1, "idea": "a cat", "prompt": "a cat"}],
        }
        manifest_path = out_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        result = cli_runner.invoke(app, ["generate", "--manifest", str(manifest_path)])
        assert result.exit_code != 0
        assert result.exception is not None
        assert "RENDER_RUN_GCLOUD_IMAGE_COMMAND_TEMPLATE" in str(result.exception)

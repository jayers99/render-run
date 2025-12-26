"""Thin CLI layer - delegates to application services."""

from __future__ import annotations

from pathlib import Path

import typer

from render_run.application import batch_plan_service, prompt_expander_service

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.callback()
def callback() -> None:
    """Render Run - agent-driven batch image generation runner."""
    pass


@app.command()
def hello(name: str = typer.Argument(default="World")) -> None:
    """Smoke-test command."""
    typer.echo(f"Hello, {name}!")


@app.command()
def expand(idea: str) -> None:
    """Expand a short image idea into a more detailed prompt (placeholder)."""
    detailed = prompt_expander_service.expand(idea=idea)
    typer.echo(detailed)


@app.command()
def prepare(
    in_path: Path = typer.Option(
        ..., "--in", exists=True, dir_okay=False, readable=True, help="Input prompts file"
    ),
    out_dir: Path = typer.Option(
        ..., "--out", file_okay=False, help="Output run directory"
    ),
    expand_prompts: bool = typer.Option(
        True, "--expand/--no-expand", help="Expand short ideas into detailed prompts"
    ),
    providers: str = typer.Option(
        "dalle,gemini",
        "--providers",
        help="Comma-separated provider list to record in manifest (no calls yet)",
    ),
) -> None:
    """Create a run folder + manifest.json for a batch generation run.

    This command does not call image providers yet. It establishes a stable contract
    (inputs, outputs, naming) so Create projects can depend on Render Run.
    """

    provider_list = [p.strip() for p in providers.split(",") if p.strip()]
    if not provider_list:
        raise typer.BadParameter("--providers must include at least one provider")

    manifest_path = batch_plan_service.prepare_run(
        in_path=in_path,
        out_dir=out_dir,
        expand_prompts=expand_prompts,
        providers=provider_list,
    )
    typer.echo(str(manifest_path))

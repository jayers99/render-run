"""Thin CLI layer - delegates to application services."""

from __future__ import annotations

from pathlib import Path

import typer

from render_run.application import (
    batch_plan_service,
    generation_service,
    prompt_expander_service,
    run_directory_service,
    user_config_service,
)
from render_run.infrastructure.gcloud_cli_image_generation_provider import (
    GCloudCliImageGenerationProvider,
)

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
    out_dir: Path | None = typer.Option(
        None, "--out", file_okay=False, help="Output run directory (optional if domain+project provided)"
    ),
    domain: str | None = typer.Option(
        None, "--domain", help="Praxis domain (used to derive --out when omitted)"
    ),
    project: str | None = typer.Option(
        None, "--project", help="Project name (used to derive --out when omitted)"
    ),
    run_id: str | None = typer.Option(
        None,
        "--run-id",
        help="Run identifier for output folder name (defaults to UTC timestamp)",
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

    if out_dir is None:
        if not domain or not project:
            raise typer.BadParameter(
                "Provide either --out or both --domain and --project"
            )
        user_config = user_config_service.load_user_config()
        resolved_run_id = run_id or run_directory_service.default_run_id()
        out_dir = run_directory_service.derive_run_directory(
            generated_root=user_config.generated_content_root,
            domain=domain,
            project=project,
            run_id=resolved_run_id,
        ).path
        run_id = resolved_run_id

    provider_list = [p.strip() for p in providers.split(",") if p.strip()]
    if not provider_list:
        raise typer.BadParameter("--providers must include at least one provider")

    manifest_path = batch_plan_service.prepare_run(
        in_path=in_path,
        out_dir=out_dir,
        expand_prompts=expand_prompts,
        providers=provider_list,
        domain=domain,
        project=project,
        run_id=run_id,
    )
    typer.echo(str(manifest_path))


@app.command()
def generate(
    manifest_path: Path = typer.Option(
        ..., "--manifest", exists=True, dir_okay=False, readable=True, help="Path to manifest.json"
    ),
    provider: str = typer.Option(
        "gcloud",
        "--provider",
        help="Provider implementation (MVP: gcloud).",
    ),
) -> None:
    """Generate images for a prepared manifest.

    MVP: only `gcloud` provider is supported, configured via
    RENDER_RUN_GCLOUD_IMAGE_COMMAND_TEMPLATE.
    """

    if provider != "gcloud":
        raise typer.BadParameter("Only --provider gcloud is supported for MVP")

    gcloud_provider = GCloudCliImageGenerationProvider.from_env()
    generated = generation_service.generate_from_manifest(
        manifest_path=manifest_path, provider=gcloud_provider
    )
    for item in generated:
        typer.echo(str(item.path))

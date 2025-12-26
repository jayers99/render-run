"""Batch planning (no provider calls).

Create projects need a stable contract: given a prompts file, Render Run produces
an output folder with a manifest describing what would be generated.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from render_run.application import prompt_expander_service


@dataclass(frozen=True)
class ManifestItem:
    id: int
    idea: str
    prompt: str
    providers: list[str]


@dataclass(frozen=True)
class Manifest:
    schema_version: str
    created_at: str
    input_file: str
    out_dir: str
    expand_prompts: bool
    items: list[ManifestItem]


def prepare_run(
    *,
    in_path: Path,
    out_dir: Path,
    expand_prompts: bool,
    providers: list[str],
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)

    ideas = _read_ideas(in_path)
    items: list[ManifestItem] = []

    for index, idea in enumerate(ideas, start=1):
        prompt = (
            prompt_expander_service.expand(idea=idea) if expand_prompts else idea
        )
        items.append(
            ManifestItem(id=index, idea=idea, prompt=prompt, providers=providers)
        )

    manifest = Manifest(
        schema_version="0.1",
        created_at=datetime.now(timezone.utc).isoformat(),
        input_file=str(in_path),
        out_dir=str(out_dir),
        expand_prompts=expand_prompts,
        items=items,
    )

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(asdict(manifest), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    expanded_path = out_dir / "expanded_prompts.txt"
    expanded_path.write_text(
        "\n".join(item.prompt for item in items) + ("\n" if items else ""),
        encoding="utf-8",
    )

    return manifest_path


def _read_ideas(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    ideas: list[str] = []
    for line in lines:
        idea = line.strip()
        if not idea or idea.startswith("#"):
            continue
        ideas.append(idea)
    return ideas

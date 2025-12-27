"""Batch generation orchestration.

This is application-layer code: it coordinates manifest inputs, providers,
and output layout.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from render_run.domain.image_generation_provider import GeneratedImage, ImageGenerationProvider


@dataclass(frozen=True)
class ManifestItem:
    id: int
    idea: str
    prompt: str


@dataclass(frozen=True)
class Manifest:
    schema_version: str
    created_at: str
    input_file: str
    out_dir: str
    expand_prompts: bool
    items: list[ManifestItem]

    domain: str | None = None
    project: str | None = None
    run_id: str | None = None


def load_manifest(path: Path) -> Manifest:
    data = json.loads(path.read_text(encoding="utf-8"))
    items = [
        ManifestItem(id=int(i["id"]), idea=str(i["idea"]), prompt=str(i["prompt"]))
        for i in data.get("items", [])
    ]

    return Manifest(
        schema_version=str(data["schema_version"]),
        created_at=str(data["created_at"]),
        input_file=str(data["input_file"]),
        out_dir=str(data["out_dir"]),
        expand_prompts=bool(data["expand_prompts"]),
        items=items,
        domain=data.get("domain"),
        project=data.get("project"),
        run_id=data.get("run_id"),
    )


def generate_from_manifest(
    *,
    manifest_path: Path,
    provider: ImageGenerationProvider,
    images_dirname: str = "images",
) -> list[GeneratedImage]:
    manifest = load_manifest(manifest_path)
    out_dir = Path(manifest.out_dir)
    images_dir = out_dir / images_dirname
    images_dir.mkdir(parents=True, exist_ok=True)

    generated: list[GeneratedImage] = []
    for item in manifest.items:
        out_path = images_dir / f"item-{item.id:03d}.png"
        generated.append(provider.generate_image(prompt=item.prompt, out_path=out_path))

    return generated

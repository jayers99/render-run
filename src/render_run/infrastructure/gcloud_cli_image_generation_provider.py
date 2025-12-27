from __future__ import annotations

import os
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path

from render_run.domain.image_generation_provider import GeneratedImage


@dataclass(frozen=True)
class GCloudCliImageGenerationProvider:
    """MVP provider: shell out to a gcloud-driven command.

    This is intentionally a CLI wrapper (not a direct Python HTTP client).

    The configured command must write an image file to {out}.
    Placeholders:
      - {prompt}: the prompt text
      - {out}: output file path

    Config:
      - RENDER_RUN_GCLOUD_IMAGE_COMMAND_TEMPLATE (string)

    Example (illustrative):
      export RENDER_RUN_GCLOUD_IMAGE_COMMAND_TEMPLATE='bash -lc "..."'

    We keep this generic because the exact gcloud/Vertex invocation differs by
    model and environment.
    """

    command_template: str
    name: str = "gcloud"

    @staticmethod
    def from_env() -> "GCloudCliImageGenerationProvider":
        template = os.environ.get("RENDER_RUN_GCLOUD_IMAGE_COMMAND_TEMPLATE")
        if not template:
            raise RuntimeError(
                "Missing RENDER_RUN_GCLOUD_IMAGE_COMMAND_TEMPLATE. "
                "Set a command that writes an image to {out}."
            )
        return GCloudCliImageGenerationProvider(command_template=template)

    def generate_image(self, *, prompt: str, out_path: Path) -> GeneratedImage:
        out_path.parent.mkdir(parents=True, exist_ok=True)

        cmd_str = self.command_template.format(prompt=prompt, out=str(out_path))
        cmd = shlex.split(cmd_str)

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                "gcloud CLI provider command failed. "
                f"exit={result.returncode} stderr={result.stderr.strip()}"
            )

        if not out_path.exists():
            raise RuntimeError(
                "gcloud CLI provider did not produce expected output file: "
                f"{out_path}"
            )

        return GeneratedImage(provider=self.name, prompt=prompt, path=out_path)

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class GeneratedImage:
    provider: str
    prompt: str
    path: Path


class ImageGenerationProvider(Protocol):
    """Port for image generation.

    Implementations live in infrastructure (CLI wrappers, HTTP APIs, etc.).
    """

    name: str

    def generate_image(self, *, prompt: str, out_path: Path) -> GeneratedImage: ...

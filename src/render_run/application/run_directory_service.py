"""Derive deterministic run directories.

Convention:
  <generated_root>/<domain>/<project>/runs/<run_id>

Example:
  ~/icloud/praxis-generated-content/create/xmas-cards-2025/runs/20251226-235959
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class RunDirectory:
    path: Path
    run_id: str


def default_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def derive_run_directory(*, generated_root: Path, domain: str, project: str, run_id: str) -> RunDirectory:
    if not domain.strip():
        raise ValueError("domain is required")
    if not project.strip():
        raise ValueError("project is required")
    if not run_id.strip():
        raise ValueError("run_id is required")

    path = generated_root / domain / project / "runs" / run_id
    return RunDirectory(path=path, run_id=run_id)

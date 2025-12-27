"""User-level config discovery.

Render Run is a Code-domain utility, but it needs a stable place to resolve
user defaults (e.g., where to store generated artifacts).

This intentionally avoids any interactive UX: config can be provided via
environment variables or a small file in ~/.config.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


_CONFIG_DIR = Path.home() / ".config" / "praxis"
_CONFIG_FILE = _CONFIG_DIR / "config.json"


@dataclass(frozen=True)
class UserConfig:
    generated_content_root: Path


def load_user_config() -> UserConfig:
    """Load user defaults.

    Precedence:
    1) PRAXIS_GENERATED_CONTENT_ROOT env var
    2) ~/.config/praxis/config.json (key: generated_content_root)
    3) ~/icloud/praxis-generated-content
    """

    env_root = os.environ.get("PRAXIS_GENERATED_CONTENT_ROOT")
    if env_root:
        return UserConfig(generated_content_root=Path(env_root).expanduser())

    if _CONFIG_FILE.exists():
        data = json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
        root = data.get("generated_content_root")
        if isinstance(root, str) and root.strip():
            return UserConfig(generated_content_root=Path(root).expanduser())

    return UserConfig(
        generated_content_root=(Path.home() / "icloud" / "praxis-generated-content")
    )


def config_file_path() -> Path:
    return _CONFIG_FILE

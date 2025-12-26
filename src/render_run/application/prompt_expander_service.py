"""Prompt expansion service.

This is a placeholder implementation to keep the scaffold runnable.
"""


def expand(*, idea: str) -> str:
    idea_clean = idea.strip()
    if not idea_clean:
        raise ValueError("idea must be non-empty")

    return (
        "A high-quality, visually rich illustration based on this concept: "
        f"{idea_clean}. "
        "Specify clear subject, setting, lighting, composition, and mood. "
        "Avoid text overlays, watermarks, and logos."
    )

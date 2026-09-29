"""Access the skill catalog shipped with this SDK release."""

from __future__ import annotations

from pathlib import Path


def directory() -> Path:
    """Return the directory containing one folder per skill."""
    return Path(__file__).parent

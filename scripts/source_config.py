"""Resolve the optional local YUBUS source checkout without executing dotenv files."""

from __future__ import annotations

import os
from pathlib import Path


def dotenv_source_dir(path: Path) -> str | None:
    """Read only an exact YUBUS_SOURCE_DIR assignment from a local dotenv file."""
    if not path.is_file():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.lstrip().startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if separator and key.strip() == "YUBUS_SOURCE_DIR":
            return value.strip()
    return None


def source_dir(root: Path, environ: dict[str, str] | None = None) -> Path | None:
    """Prefer the environment, then .env; accept only an existing absolute directory."""
    environ = os.environ if environ is None else environ
    value = environ.get("YUBUS_SOURCE_DIR") or dotenv_source_dir(root / ".env")
    if not value:
        return None
    candidate = Path(value).expanduser()
    if not candidate.is_absolute() or not candidate.is_dir():
        return None
    return candidate.resolve()

#!/usr/bin/env python3
"""Build a production-prefixed MkDocs site without changing the checked-in config."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import yaml


def production_url(value: str) -> str:
    parsed = urlparse(value)
    try:
        port = parsed.port
    except ValueError as error:
        raise ValueError("site URL must use a valid HTTPS authority") from error
    if (
        parsed.scheme != "https"
        or not parsed.netloc
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or (port is not None and not 1 <= port <= 65535)
    ):
        raise ValueError("site URL must be an absolute HTTPS URL without credentials, query, or fragment")
    if parsed.netloc != "yubus.puyu.pe" or parsed.path not in {"/manual", "/manual/"} or "%" in parsed.path:
        raise ValueError("site URL must point exactly to https://yubus.puyu.pe/manual/")
    return "https://yubus.puyu.pe/manual/"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-url", required=True, type=production_url)
    parser.add_argument("--site-dir", default="site-production", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    config = yaml.safe_load((root / "mkdocs.yml").read_text(encoding="utf-8"))
    config["site_url"] = args.site_url
    config["docs_dir"] = str((root / "docs").resolve())
    config["site_dir"] = str((root / args.site_dir).resolve())

    with tempfile.NamedTemporaryFile("w", suffix=".yml", dir=root, encoding="utf-8") as temporary:
        yaml.safe_dump(config, temporary, allow_unicode=True, sort_keys=False)
        temporary.flush()
        subprocess.run(
            [sys.executable, "-m", "mkdocs", "build", "--strict", "--clean", "--config-file", temporary.name],
            check=True,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

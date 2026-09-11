#!/usr/bin/env python3
"""Validate the published MkDocs navigation, inventory, and local image references."""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml
from jsonschema import Draft202012Validator

MARKDOWN_TARGET = re.compile(r"!?\[[^]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
HTML_IMAGE_TARGET = re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
INVENTORY_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
INVENTORY_PATH = re.compile(r"^(?!/)(?!.*(?:^|/)\.\.(?:/|$))[^/].*\.md$")
INVENTORY_STATUSES = {"registered", "source_traced"}
INVENTORY_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "documentation/inventory.schema.json"


def nav_paths(entries: list[object]) -> list[str]:
    paths: list[str] = []
    for entry in entries:
        if isinstance(entry, str):
            paths.append(entry)
        elif isinstance(entry, dict):
            for value in entry.values():
                if isinstance(value, str):
                    paths.append(value)
                elif isinstance(value, list):
                    paths.extend(nav_paths(value))
                else:
                    raise ValueError(f"Unsupported navigation value: {value!r}")
        else:
            raise ValueError(f"Unsupported navigation entry: {entry!r}")
    return paths


def local_targets(markdown: str) -> list[str]:
    targets = MARKDOWN_TARGET.findall(markdown) + HTML_IMAGE_TARGET.findall(markdown)
    return [target for target in targets if not urlparse(target).scheme and not target.startswith("#")]


def anchors(markdown: str) -> set[str]:
    values: set[str] = set()
    for heading in HEADING.findall(markdown):
        normalized = unicodedata.normalize("NFKD", heading).encode("ascii", "ignore").decode().lower()
        values.add(re.sub(r"[^a-z0-9]+", "-", normalized).strip("-"))
    return values


def validate_inventory(inventory: object) -> list[str]:
    """Apply repository-specific inventory checks not expressed by the schema."""
    if not isinstance(inventory, dict):
        return ["inventory must be a mapping"]

    errors: list[str] = []
    required_top_level = {"version", "review_status", "review_note", "pages"}
    if set(inventory) != required_top_level:
        errors.append("inventory must contain only version, review_status, review_note, and pages")
    if type(inventory.get("version")) is not int or inventory.get("version") != 1:
        errors.append("inventory version must be integer 1")
    if inventory.get("review_status") not in {"inventory_only", "semantically_reviewed"}:
        errors.append("inventory review_status is invalid")
    if not isinstance(inventory.get("review_note"), str) or not inventory.get("review_note").strip():
        errors.append("inventory review_note must be a non-empty string")

    pages = inventory.get("pages")
    if not isinstance(pages, list) or not pages:
        return errors + ["inventory pages must be a non-empty list"]

    ids: list[str] = []
    paths: list[str] = []
    required_page_fields = {"id", "path", "status", "reviewed"}
    for index, page in enumerate(pages, start=1):
        prefix = f"inventory page {index}"
        if not isinstance(page, dict):
            errors.append(f"{prefix} must be a mapping")
            continue
        if set(page) != required_page_fields:
            errors.append(f"{prefix} must contain only id, path, status, and reviewed")
        page_id = page.get("id")
        path = page.get("path")
        if not isinstance(page_id, str) or not INVENTORY_ID.fullmatch(page_id):
            errors.append(f"{prefix} id must be a lowercase kebab-case string")
        else:
            ids.append(page_id)
        if not isinstance(path, str) or not INVENTORY_PATH.fullmatch(path):
            errors.append(f"{prefix} path must be a safe relative Markdown path")
        else:
            paths.append(path)
        if page.get("status") not in INVENTORY_STATUSES:
            errors.append(f"{prefix} status is invalid")
        if type(page.get("reviewed")) is not bool:
            errors.append(f"{prefix} reviewed must be a boolean")
    if len(ids) != len(set(ids)):
        errors.append("inventory contains duplicate page ids")
    if len(paths) != len(set(paths)):
        errors.append("inventory contains duplicate page paths")
    return errors


def validate_inventory_schema(inventory: object) -> list[str]:
    """Validate inventory structure against the checked-in JSON Schema."""
    schema = json.loads(INVENTORY_SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    return [
        f"inventory schema: {error.message}"
        for error in sorted(validator.iter_errors(inventory), key=str)
    ]


def check(root: Path) -> list[str]:
    errors: list[str] = []
    config = yaml.safe_load((root / "mkdocs.yml").read_text(encoding="utf-8"))
    inventory = yaml.safe_load((root / "documentation/inventory.yml").read_text(encoding="utf-8"))
    errors.extend(validate_inventory_schema(inventory))
    errors.extend(validate_inventory(inventory))
    if not isinstance(config, dict):
        return errors + ["mkdocs configuration must be a mapping"]
    if not isinstance(inventory, dict) or not isinstance(inventory.get("pages"), list):
        return errors
    navigation = config.get("nav", [])
    if not isinstance(navigation, list):
        return errors + ["mkdocs navigation must be a list"]
    try:
        nav = nav_paths(navigation)
    except ValueError as error:
        return errors + [str(error)]
    registered = [page["path"] for page in inventory["pages"] if isinstance(page, dict) and isinstance(page.get("path"), str)]
    documentation_pages = sorted(
        path.relative_to(root / "docs").as_posix()
        for path in (root / "docs").rglob("*.md")
    )

    if len(nav) != len(set(nav)):
        errors.append("mkdocs navigation contains duplicate page paths")
    if set(nav) != set(registered):
        errors.append("inventory pages must exactly match published navigation")
    if set(nav) != set(documentation_pages):
        errors.append("published navigation must exactly match Markdown pages in docs")

    for path in nav:
        page = root / "docs" / path
        if not page.is_file():
            errors.append(f"navigation target does not exist: {path}")
            continue
        markdown = page.read_text(encoding="utf-8")
        for target in local_targets(markdown):
            parsed = urlparse(target)
            target_path = (page.parent / unquote(parsed.path)).resolve()
            docs_root = (root / "docs").resolve()
            if not target_path.is_relative_to(docs_root):
                errors.append(f"{path} links outside docs: {target}")
            elif not target_path.is_file():
                errors.append(f"{path} has a missing local reference: {target}")
        for target in MARKDOWN_TARGET.findall(markdown):
            parsed = urlparse(target)
            if parsed.scheme or not parsed.fragment:
                continue
            target_path = page if not parsed.path else (page.parent / unquote(parsed.path)).resolve()
            if target_path.is_file() and parsed.fragment not in anchors(target_path.read_text(encoding="utf-8")):
                errors.append(f"{path} has a missing local anchor: {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = check(args.root.resolve())
    if errors:
        print("Inventory check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Inventory check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

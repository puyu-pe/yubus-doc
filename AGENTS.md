# YUBUS Documentation Instructions

## Scope

This repository publishes end-user guides in Spanish. Technical artifacts,
evidence records, automation, and agent instructions are in English.

## Source-backed fichas

- Resolve `YUBUS_SOURCE_DIR` from the environment first, then from an untracked
  local `.env`; parse that file as data and never source it in a shell.
- Before authoring, apply the similarity gate: same objective updates the existing
  guide; partial overlap extends or links it; a distinct flow may create a guide;
  an ambiguous boundary requires a human decision.
- Use CodeGraph for indexed application source. Trace UI or view, JavaScript
  event, route, controller, service or model, and tests where available.
- Record internal evidence under `documentation/evidence/`. Classify claims as
  proven, conditional, operational advice, or uncertainty. Do not add internal
  source citations to end-user guides.

## Screenshots

- Preserve existing image paths and bytes. Never bulk rename, recompress, or
  restructure screenshots.
- New captures require metadata under `documentation/captures/`, demonstrative
  data, and redaction of sensitive identifiers.
- No capture automation exists in this repository; do not claim a live capture
  was validated without a human browser check.

## Inventory and validation

- Register published pages in `documentation/inventory.yml`. Registration tracks
  inventory coverage; it is not semantic verification of every guide.
- Run `python scripts/check_inventory.py` and `mkdocs build --strict --clean`
  before delivery.

## Project skills

- `.agents/skills/yubus-source-backed-ficha/SKILL.md` applies the source-backed
  ficha contract for YUBUS work.

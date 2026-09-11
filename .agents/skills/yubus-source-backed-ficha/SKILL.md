---
name: yubus-source-backed-ficha
description: "Trigger: YUBUS ficha, source-backed ficha, document YUBUS behavior. Investigate YUBUS source and author evidence-backed fichas."
license: Apache-2.0
metadata:
  author: "Puyu PE"
  version: "1.0"
---

## Activation Contract

Use for a new or revised YUBUS user guide whose behavior must be supported by
the application source.

## Hard Rules

- Resolve `YUBUS_SOURCE_DIR` from the environment, then untracked `.env`; parse
  it as data and never source it.
- Apply the similarity gate before writing: same objective updates; partial
  overlap extends or links; distinct flow creates; ambiguity requires a human.
- Use CodeGraph first for indexed source. Trace view/UI, JavaScript event, route,
  controller, service/model, and tests when they exist.
- Classify statements as proven, conditional, operational advice, or uncertainty.
  Keep evidence internal and write user-facing guides in Spanish.
- Preserve screenshot bytes and paths. New captures require metadata and redaction.

## Decision Gates

| Finding | Required action |
| --- | --- |
| Same objective | Update the existing guide. |
| Partial overlap | Extend or cross-link the existing guide. |
| Distinct flow | Create a guide. |
| Ambiguous boundary | Ask a human before writing. |

## Execution Steps

1. Inspect matching published guides, `mkdocs.yml`, and inventory records.
2. Trace the narrow source flow and record concrete file/symbol evidence in
   `documentation/evidence/`.
3. Update only the necessary guide, navigation, and inventory records.
4. Run the inventory checker and strict MkDocs build.

## Output Contract

Report the similarity decision, source evidence, claim classifications, capture
status, limitations, changed files, and validation results.

## References

- `../../../AGENTS.md`
- `../../../documentation/inventory.yml`
- `../../../documentation/capture-protocol.md`

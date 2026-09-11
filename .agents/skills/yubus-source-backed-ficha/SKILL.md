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
the application source, or for a manual incremental documentation sync.

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

## Manual Sync

1. Read `documentation/yubus-sync.yml`. Resolve `YUBUS_SOURCE_DIR` from the
   environment, then the untracked `.env`, and read `VERSION` from the fixed
   target commit on `main`, not from the worktree.
2. Compare `completed.source_commit` to the target, including added, modified,
   deleted, and renamed paths. The baseline is only as broad as its recorded
   scope; never present it as a historical comprehensive audit.
3. Classify each affected path as documented, no documentation impact, or
   pending. Do not inherit exclusions from YURES; any YUBUS exclusion requires
   explicit user approval.
4. Trace user-facing changes and write source-backed evidence. Use CodeGraph
   only when its indexed bytes match the target; otherwise inspect immutable
   target bytes with `git show <target>:<path>`.
5. Keep `target` and `pending` current. Advance `completed` only after every
   affected path is resolved and the required documentation validation passes.
6. Do not fetch, checkout, mutate, or claim remote or deployed synchronization
   for the source repository. This is a manual process; do not add automation,
   parsers, CI, or schemas for it.

## Output Contract

Report the similarity decision, source evidence, claim classifications, capture
status, limitations, changed files, and validation results.

## References

- `../../../AGENTS.md`
- `../../../documentation/inventory.yml`
- `../../../documentation/capture-protocol.md`

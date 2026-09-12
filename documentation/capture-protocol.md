# Screenshot Capture Protocol

Use this protocol only for new screenshots. Existing assets, paths, and bytes
are preserved; never overwrite an image silently or create root-level artifacts.

## Decide and prepare

- Reuse a valid image when it supports the instruction. Capture before and after
  a meaningful state change only when both states clarify the flow.
- Use demonstrative data. Sanitize names, document numbers, phones, emails,
  fares, tenant identifiers, credentials, private guard URLs, and session tokens.
- Do not commit or emit a transaction, or save a configuration change, without
  explicit authorization. Blur selection without changing values.
- Use a stable viewport. Wait for meaningful UI readiness, never arbitrary
  sleeps. Capture a full modal or section with its title, relevant controls, and
  visible result; place the image next to its guide step.
- If a screenshot or prototype cannot be accessed, say so. Do not claim it was
  observed or validated.

## Annotate in the browser

Use thin coral (`#ff5b70`) frames and arrows only when they clarify the action.
Do not cover text or values. Choose a whitespace anchor element and a clear path,
then inspect the resulting overlay for intervening text before capture. Load the
helper with `page.addScriptTag({ path: '<absolute helper path>' })` (or evaluate
its file content), then use its small browser API immediately before capture:

```js
const result = window.YubusCaptureAnnotations.render({
  root: '[role="dialog"]',
  highlights: ['[data-testid="confirm"]'],
  arrows: [{ from: '[data-testid="amount"]', to: '[data-testid="confirm"]' }],
})
if (!result.ok) throw new Error(result.errors.join(' '))
try {
  // capture the root
} finally {
  window.YubusCaptureAnnotations.clear()
}
```

`render` recomputes geometry for the current layout and returns `{ ok, errors }`.
If a root or target is missing, hidden, outside the root, or outside the viewport,
or arrow endpoints overlap, do not make a screenshot claim. The overlay does not
change UI values, listeners, forms, layout, or network state. Clear it before
leaving the browser context.

## Finalize and record

1. Sanitize or crop the image, write it directly to its final repository path,
   then visually read the actual file back before registering it. Avoid deliberate
   throwaway snapshots.
2. Create `documentation/captures/<slug>.yml` using actual repository paths and
   observed values only. Keep unknown values null; do not infer an application
   version from source.

```yaml
guide_path: docs/operations/example.md
asset_path: docs/img/operations/example.png
capture_date: 2026-09-11
application_version: null
source_commit: null
redaction_status: complete
browser_observed: true
human_validation: pending
```

3. `browser_observed` means the browser displayed the stated UI during capture;
   it is not human validation. Keep `human_validation: pending` until a human
   approves the rendered image.
4. Keep the approved asset path stable after publication. This repository has no
   unattended capture runner; an agent uses Playwright MCP and this annotation
   helper. A generated or copied image is not evidence of live UI validation.

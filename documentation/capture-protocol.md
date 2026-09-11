# Screenshot Capture Protocol

Use this protocol only for new screenshots. Existing assets are preserved as-is.

## Before capture

- Use demonstrative or disposable data.
- Remove or obscure names, document numbers, phones, emails, fares, and tenant identifiers.
- Confirm the guide needs a new capture; do not replace a working image for style alone.

## Record metadata

Create `documentation/captures/<slug>.yml` with the guide path, asset path,
capture date, application version or commit when known, redaction status, and
human validation status. Do not record credentials or real identifiers.

## Publish safely

- Keep the approved asset path stable after publication.
- State `human_validation: pending` until a browser check has occurred.
- This repository has no capture automation. A generated or copied image is not
  evidence of live UI validation.

# Production Publication Runbook

## Purpose

`.github/workflows/publish.yml` builds the manual only and synchronizes it to
`/var/www/yubus.puyu.pe/shared/manual/`. It does not change Laravel,
`public/storage`, the web server, or application data.

## Prerequisites

- The application release must first create the real
  `/var/www/yubus.puyu.pe/shared/manual/` directory and the current-release
  `public/manual` symlink resolving exactly to it. The documentation workflow
  never creates either path and exits before synchronization when either check
  fails.
- `shared/manual` and its ancestors must be writable by the deployment identity
  and readable by the web-server user. The application release that provisions
  this directory has not been executed as part of this change, so it may not yet
  exist in production.
- GitHub Environment `production` contains these secrets:

| Secret | Purpose |
| --- | --- |
| `DEPLOY_HOST` | SSH host. |
| `DEPLOY_USER` | SSH user name. |
| `DEPLOY_SSH_PRIVATE_KEY` | Deploy private key. |
| `DEPLOY_KNOWN_HOSTS` | Pinned, verified host key entries. |

- GitHub Environment `production` contains these variables:

| Variable | Required value |
| --- | --- |
| `DEPLOY_PORT` | SSH port, or leave unset for `22`. |

## Activation checklist

- Run the local inventory checker, tests, and strict build.
- Release the application first so it provisions `shared/manual` and
  `public/manual -> shared/manual`.
- Configure the GitHub `production` environment secrets and optional
  `DEPLOY_PORT` variable, then publish the documentation.
- Review the PR validation workflow before merging.
- After the first publication, verify `https://yubus.puyu.pe/manual` redirects
  to `https://yubus.puyu.pe/manual/`, then check internal pages, assets, and
  search. Nginx symlink and redirect behavior still requires this live check.

## Rollback

Use **Publish manual** with `workflow_dispatch` and provide the previously known
good Git ref in `ref`. The workflow explicitly checks out that ref before it
builds. It replaces only the dedicated `shared/manual/` directory with
`rsync --delete`. Do not use it until the application-release prerequisite has
been provisioned and verified.

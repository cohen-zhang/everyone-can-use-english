# AGENTS.md

## Cursor Cloud specific instructions

This is a Yarn 4 (Corepack) workspaces monorepo plus separate Python tooling. Node >= 20 and Python 3.12 are available on the VM. The update script already runs `yarn install` and installs the MkDocs Python deps, so you normally only need to start services.

### Services / how to run (dev mode)

Commands are defined in the root `package.json` scripts and each workspace's `package.json`; use those rather than reinventing them.

| Service | Location | Dev command | Notes |
| --- | --- | --- | --- |
| Enjoy (Electron desktop app — primary product) | `enjoy/` | `yarn enjoy:dev` | GUI app; see caveats below. |
| 1000-hours (VitePress docs) | `1000-hours/` | `yarn docs:dev` | Static docs SSG, no backend. Add `--port <n>` if 5173 is taken. |
| 1000h-portal (Nuxt 3 site) | `1000h-portal/` | `yarn workspace 1000h-portal dev` (or `cd 1000h-portal && yarn dev`) | Static marketing site, no backend. |
| learning-notes (MkDocs Material) | built from repo root via `mkdocs.yml` | `python3 -m mkdocs serve` | Python, not Node. See PATH note below. |

### Non-obvious gotchas

- **Corepack download prompt:** the first `yarn` invocation on a fresh VM prompts to download Yarn 4.6.0 and blocks. Always prefix yarn commands with `COREPACK_ENABLE_DOWNLOAD_PROMPT=0` (e.g. `COREPACK_ENABLE_DOWNLOAD_PROMPT=0 yarn ...`) in non-interactive contexts. The update script already does this.
- **`mkdocs` is not on PATH:** pip installs it to `~/.local/bin`. Run it as `python3 -m mkdocs serve` / `python3 -m mkdocs build`. The MkDocs "unrecognized relative link" INFO lines during build are pre-existing content issues, not setup failures.
- **Enjoy lint uses legacy ESLint config:** `enjoy/.eslintrc.json` is an eslintrc file but ESLint 9 is installed (defaults to flat config). Run lint with `ESLINT_USE_FLAT_CONFIG=false` set, e.g. `cd enjoy && ESLINT_USE_FLAT_CONFIG=false yarn eslint --ext .ts,.tsx .`. Lint currently reports many pre-existing errors/warnings in the repo; that is the code's state, not an environment problem.
- **Enjoy needs a display:** the VM has `Xvfb`/`xvfb-run` and a live `DISPLAY=:1`. `yarn enjoy:dev` renders fine there. In CI (`.github/workflows/test-enjoy-app.yml`), tests run under `xvfb-run`.
- **Enjoy startup noise is harmless:** `Failed to connect to the bus` (dbus), `Electron sandboxed_renderer.bundle.js script failed to run`, `TypeError: object null is not iterable`, and `Error: Db path is not ready` all appear even on successful launches. The app still renders the welcome screen. Do NOT treat these as fatal, and do NOT add `--no-sandbox` workarounds — the UI works.
- **Enjoy has no bundled backend:** `yarn enjoy:dev` points the app at `WEB_API_URL=http://localhost:3000` / `ws://localhost:3000`, which is a separate backend NOT in this repo. You can reach the welcome + login screens without it, but completing login/sync requires that external backend (or the remote `https://enjoy.bot`) plus an account. `yarn enjoy:dev` runs `predev`/`download` which fetches a dictionary over the network on first run.
- When manually testing Enjoy, don't close the auto-opened DevTools pane or kill the Electron process mid-session unless you intend to restart it — just screenshot/interact with the app window.

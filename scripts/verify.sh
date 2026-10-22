#!/usr/bin/env bash
# Mandatory verification (see AGENTS.md) / Verificación obligatoria
set -euo pipefail
root="$(git rev-parse --show-toplevel)"

if [ -d "$root/backend" ]; then
  cd "$root/backend"
  uv run ruff check .
  uv run ruff format --check .
  uv run pytest --cov --cov-fail-under=80
fi
if [ -d "$root/frontend" ]; then
  cd "$root/frontend"
  bun run lint
  bun run test
  bun run build
fi

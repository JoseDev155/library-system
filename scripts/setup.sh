#!/usr/bin/env bash
# Install backend and frontend dependencies / Instala las dependencias
set -euo pipefail
root="$(git rev-parse --show-toplevel)"

if [ -d "$root/backend" ]; then
  (cd "$root/backend" && uv python pin 3.15 && uv sync)
fi
if [ -d "$root/frontend" ]; then
  (cd "$root/frontend" && vp install)
fi

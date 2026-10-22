#!/usr/bin/env bash
# Inicialización del proyecto desde el IDE Antigravity
set -e
raiz="$(git rev-parse --show-toplevel)"
echo "Inicializando library-system. Lee AGENTS.md y spec/spec.md antes de empezar."
if [ -d "$raiz/backend" ]; then
  (cd "$raiz/backend" && uv python pin 3.15 && uv sync)
fi
if [ -d "$raiz/frontend" ]; then
  (cd "$raiz/frontend" && vp install)
fi

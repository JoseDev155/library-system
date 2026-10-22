#!/usr/bin/env bash
# Verificación obligatoria de bd-agente (ver instrucciones.md)
set -e
cd "$(git rev-parse --show-toplevel)/backend"
uv run ruff check .
uv run pytest

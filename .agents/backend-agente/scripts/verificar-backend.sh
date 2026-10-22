#!/usr/bin/env bash
# Verificación obligatoria de backend-agente (ver instrucciones.md)
set -e
cd "$(git rev-parse --show-toplevel)/backend"
uv run ruff check .
uv run ruff format --check .
uv run pytest --cov=app --cov-fail-under=80

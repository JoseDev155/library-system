#!/usr/bin/env bash
# Verificación obligatoria de pruebas-agente (ver instrucciones.md)
set -e
cd "$(git rev-parse --show-toplevel)/backend"
uv run pytest --cov=app --cov-fail-under=80

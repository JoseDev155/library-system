#!/usr/bin/env bash
# Verificación obligatoria de frontend-agente (ver instrucciones.md)
set -e
cd "$(git rev-parse --show-toplevel)/frontend"
vp check
vp test
vp build

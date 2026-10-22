#!/usr/bin/env bash
# Verificación obligatoria de documentacion-agente (ver instrucciones.md)
set -e
git diff --check
echo "Revisa a mano que spec/spec.md refleje el comportamiento real."

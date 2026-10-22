#!/usr/bin/env bash
# Enable the versioned Git hooks in this clone / Activa los hooks de Git versionados en este clon
set -euo pipefail
root="$(git rev-parse --show-toplevel)"
git -C "$root" config core.hooksPath scripts/hooks
chmod +x "$root"/scripts/hooks/* 2>/dev/null || true
echo "Hooks enabled: core.hooksPath = scripts/hooks"

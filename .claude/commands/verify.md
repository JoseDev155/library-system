---
description: Ejecuta la verificación obligatoria del proyecto
allowed-tools: Bash(scripts/verify.sh)
---

Ejecuta `scripts/verify.sh` y reporta el resultado de cada paso (Ruff, pytest con cobertura de al menos 80 %, y `bun run lint`, `bun run test` y `bun run build`). Si un paso falla o no se pudo ejecutar, dilo explícitamente y no des la tarea por terminada.

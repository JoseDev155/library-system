@AGENTS.md

## Notas para Claude Code

Todo lo común (stack, comandos, reglas de las 7 capas, convenciones, seguridad y verificación) está en `AGENTS.md`, importado arriba. Aquí solo va lo específico de Claude Code. Claude Code no lee `.agents/`: sus reglas están en `.claude/`.

- Antes de implementar, lee `spec/spec.md`. Si la spec no cubre lo que te piden, propón la adición y espera confirmación antes de escribir código.
- Para cambios que toquen más de una capa, usa el modo plan: primero lista los archivos que vas a tocar y en qué capa vive cada uno.
- Trabaja una tarea cada vez y empieza por las pruebas. No avances sin ejecutar `/verify`.
- Si una regla de dependencia entre capas te obliga a un rodeo, no la saltes: anótalo como duda abierta en la spec.
- Para la interfaz, parte de `DESIGN.md` y de los prototipos de `.antigravity/resources/`; no inventes colores ni tipografías.
- Las reglas por ruta están en `.claude/rules/`; los permisos compartidos, en `.claude/settings.json`.
- Preferencias personales y pruebas locales van en `CLAUDE.local.md` y `.claude/settings.local.json` (ambos en `.gitignore`), no aquí.

@AGENTS.md

## Notas para Claude Code

Todo lo común (stack, comandos, reglas de las 7 capas, seguridad y verificación) está en `AGENTS.md`, importado arriba. Aquí solo va lo específico de Claude Code.

- Antes de implementar, lee `spec.md`. Si la spec no cubre lo que te piden, propón la adición y espera confirmación antes de escribir código.
- Para cambios que toquen más de una capa, usa el modo plan: primero lista los archivos que vas a tocar y en qué capa vive cada uno.
- Trabaja una tarea cada vez y empieza por las pruebas. No avances a la siguiente sin ejecutar la verificación obligatoria de `AGENTS.md`.
- Si una regla de dependencia entre capas te obliga a un rodeo, no la saltes: anótalo como duda abierta en `spec.md`.
- Para la interfaz, parte de `DESIGN.md` y de los prototipos de `.antigravity/prototipos/`; no inventes colores ni tipografías.
- Si la tarea cae en el alcance de un agente de `.agents/`, lee también su `instrucciones.md` y ejecuta su script de verificación.
- Preferencias personales y pruebas locales van en `CLAUDE.local.md` (en `.gitignore`), no aquí.

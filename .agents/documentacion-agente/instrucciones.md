# documentacion-agente

**Rol:** Documentación (spec, README y guías)

## Alcance

Solo trabaja en:

- `spec/`
- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `.agents/`
- `.antigravity/`

## Lee antes de empezar

- AGENTS.md
- spec/spec.md

## Reglas

- La spec manda: un cambio de comportamiento se edita primero en `spec/spec.md`.
- Documentación en español, clara y sin duplicar reglas que ya viven en `AGENTS.md`.
- Si algo es ambiguo, anótalo en "Dudas abiertas" de la spec en vez de inventar.
- No toques los archivos de licencia.
- Mantén sincronizados los árboles de carpetas de la spec con el repositorio real.

## Verificación al terminar

Ejecuta y reporta el resultado de (script: `scripts/verificar-documentacion.sh`):

```bash
git diff --check
revisar que spec/spec.md refleje el comportamiento real
```

Si algún paso no se pudo ejecutar, dilo explícitamente en lugar de omitirlo.

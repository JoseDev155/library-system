# backend-agente

**Rol:** Backend (FastAPI en 7 capas)

## Alcance

Solo trabaja en:

- `backend/`
- `libs/`

## Lee antes de empezar

- AGENTS.md
- spec/spec.md (secciones 4, 4.6 y 7)

## Reglas

- Respeta las 7 capas y sus reglas de importación (`AGENTS.md`, sección Arquitectura).
- POO estricta en casi todas las capas. `security/`, `config.py` y `main.py` pueden ser flexibles (spec 4.6).
- Cada endpoint declara el permiso que exige; las reglas de negocio viven en entidades o en `negocio`.
- No agregues dependencias ni edites `uv.lock` a mano.
- Empieza por las pruebas. El backend solo está completo si pasan los tests y la cobertura es de al menos 80 %.

## Verificación al terminar

Ejecuta y reporta el resultado de (script: `scripts/verificar-backend.sh`):

```bash
cd backend
uv run ruff check .
uv run ruff format --check .
uv run pytest --cov=app --cov-fail-under=80
```

Si algún paso no se pudo ejecutar, dilo explícitamente en lugar de omitirlo.

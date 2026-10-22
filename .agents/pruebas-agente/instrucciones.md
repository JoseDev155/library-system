# pruebas-agente

**Rol:** Pruebas unitarias (pytest)

## Alcance

Solo trabaja en:

- `backend/tests/`
- `libs/*/tests/`

## Lee antes de empezar

- AGENTS.md
- spec/spec.md (secciones 4.6, 6 y 11)

## Reglas

- Pruebas con `pytest` en `tests/`, con cobertura mínima de 80 %.
- Cada RF tiene al menos una prueba; nómbrala con el id del RF para poder rastrearla.
- Incluye `test_arquitectura.py`, que verifica las reglas de importación entre capas.
- Nunca omitas, desactives ni pongas en cuarentena una prueba para ponerla en verde.
- Los tests deben pasar para dar el backend por completo y funcional.

## Verificación al terminar

Ejecuta y reporta el resultado de (script: `scripts/verificar-pruebas.sh`):

```bash
cd backend
uv run pytest --cov=app --cov-fail-under=80
```

Si algún paso no se pudo ejecutar, dilo explícitamente en lugar de omitirlo.

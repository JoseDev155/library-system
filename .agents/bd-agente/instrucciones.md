# bd-agente

**Rol:** Base de datos y ORM (SQLAlchemy 2.1 y Alembic)

## Alcance

Solo trabaja en:

- `backend/app/repository/`
- `backend/app/repositories/`

## Lee antes de empezar

- AGENTS.md
- spec/spec.md (sección 4.5)

## Reglas

- Motores: PostgreSQL (principal), MySQL y MariaDB (secundarios). El motor se elige con `DATABASE_URL`.
- Los modelos de tablas viven en la capa de repositorio y no son entidades; las entidades no conocen el ORM.
- Sin SQL crudo ni tipos exclusivos de un motor (spec 4.5, reglas de portabilidad).
- Toda migración pasa por Alembic. Revisa a mano las migraciones autogeneradas.
- Fechas en UTC (RNF-7). Solo `negocio` llama al repositorio.

## Verificación al terminar

Ejecuta y reporta el resultado de (script: `scripts/verificar-bd.sh`):

```bash
cd backend
uv run ruff check .
uv run pytest
```

Si algún paso no se pudo ejecutar, dilo explícitamente en lugar de omitirlo.

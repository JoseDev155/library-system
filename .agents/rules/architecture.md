# Arquitectura en 7 capas

Aplica a `backend/app/` y `libs/`. Las reglas completas están en `AGENTS.md` y `spec/spec.md`.

- Dependencias permitidas: `interface` → `dto`, `services`, `security`; `services` → `dto`, `library_entities`, `business`; `business` → `library_entities`, `repositories`, `security`; `repositories` → `library_entities`.
- Solo `business` llama a `repositories`.
- Las entidades no importan SQLAlchemy, FastAPI ni Pydantic.
- Una clase principal por archivo, con inyección de dependencias por constructor.
- Cada endpoint declara el permiso que exige.

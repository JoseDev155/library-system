---
paths:
  - "backend/app/**"
  - "libs/**"
---

# Arquitectura en 7 capas

- Respeta la tabla de dependencias de `AGENTS.md`: `interface` → `dto`, `services`, `security`; `services` → `dto`, `library_entities`, `domain`; `domain` → `library_entities`, `repositories`, `security`; `repositories` → `library_entities`.
- Solo `domain` llama a `repositories`. Los endpoints y los adapters no.
- Las entidades de `library_entities` no importan SQLAlchemy, FastAPI ni Pydantic.
- Una clase principal por archivo, con inyección de dependencias por constructor; `main.py` es el punto de composición.
- Cada endpoint declara el permiso que exige.
- `tests/test_architecture.py` debe seguir pasando.

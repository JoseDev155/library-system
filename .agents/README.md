# Carpeta `.agents/`

Instrucciones y configuración para agentes de IA, un subdirectorio por agente. Las reglas comunes viven en `AGENTS.md` y el comportamiento del sistema en `spec/spec.md`; aquí solo va lo específico de cada agente.

| Carpeta | Agente | Alcance |
|---|---|---|
| `backend-agente/` | Backend en 7 capas | `backend/`, `libs/` |
| `frontend-agente/` | Frontend React | `frontend/`, `.antigravity/prototipos/` |
| `bd-agente/` | Base de datos y ORM | capa de repositorio |
| `pruebas-agente/` | Pruebas con pytest | `tests/` |
| `documentacion-agente/` | Documentación | `spec/`, README, guías |
| `templates/` | Plantillas de `AGENTS.md`, `CLAUDE.md`, `DESIGN.md` y `spec.md` | — |

Cada carpeta de agente contiene:

- `instrucciones.md`: rol, alcance, reglas y verificación.
- `config.json`: metadatos legibles por herramientas.
- `scripts/`: script de verificación obligatoria al terminar.

Ante un conflicto, manda la spec, luego `AGENTS.md` y por último estos archivos.

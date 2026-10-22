# Espacio de trabajo de Antigravity

Notas para quien abre el proyecto en el IDE Antigravity. Esta carpeta no contiene reglas del sistema ni instrucciones de agentes: esas viven en `AGENTS.md`, `spec/spec.md` y `.agents/`.

## Abrir el proyecto

Abre la raíz del repositorio como espacio de trabajo y ejecuta `scripts/setup.sh` desde la terminal integrada.

## Contenido

| Carpeta | Uso |
|---|---|
| `context/` | Material de referencia para el IDE (documentos de contexto del proyecto) |
| `commands/` | Comandos propios del IDE |
| `resources/` | Prototipos del frontend (exportaciones de Stitch o Claude Design). Referencia visual; no es código de producción |

Los colores y la tipografía de los prototipos salen de `DESIGN.md`.

## Comandos habituales

| Acción | Comando | Carpeta |
|---|---|---|
| Instalar dependencias | `scripts/setup.sh` | raíz |
| Verificación completa | `scripts/verify.sh` | raíz |
| Pruebas del backend | `uv run pytest --cov --cov-fail-under=80` | `backend/` |
| Lint del backend | `uv run ruff check .` | `backend/` |
| Crear migración | `alembic revision --autogenerate -m "msg"` | `backend/` |
| Aplicar migraciones | `alembic upgrade head` | `backend/` |
| Frontend | `bun run dev`, `bun run lint`, `bun run test`, `bun run build` | `frontend/` |

## Qué no hacer desde el IDE

- No edites `.env`, `uv.lock` ni `bun.lock`.
- No toques los archivos de licencia.
- No cambies `libs/library_entities/` sin actualizar antes la spec.

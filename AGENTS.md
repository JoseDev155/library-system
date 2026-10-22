# AGENTS.md

Instrucciones comunes para los agentes de IA que trabajan en este repositorio. La fuente de verdad del comportamiento del sistema es `spec/spec.md`. Este archivo explica **cómo trabajar** en el repo. Cada herramienta tiene además su propia carpeta (ver "Carpetas de agentes").

## Proyecto

Sistema de biblioteca universitaria (proyecto académico, pensado para crecer). API en FastAPI organizada en **7 capas** y frontend en React. Cubre catálogo, préstamos, reservas y multas, con roles y permisos.

- Especificación: `spec/spec.md` (requisitos RF-x en notación EARS). Si el código y la spec difieren, **la spec manda**. Si la spec calla, propón la adición antes de escribir código.
- Identidad visual: `DESIGN.md`. Prototipos exportados: `.antigravity/resources/`.
- El backend **no se expone públicamente**: solo es alcanzable a través del proxy inverso. En producción no se publican `/docs`, `/redoc` ni `/openapi.json`.

## Stack

| Área | Herramienta |
|---|---|
| Backend | FastAPI, Python 3.15, gestor `uv` |
| Base de datos | PostgreSQL (principal), MySQL y MariaDB; SQLAlchemy 2.1 y Alembic |
| Contraseñas | `pwdlib[argon2]` (Argon2id) |
| Autenticación | JWT (PyJWT) con rate limit |
| Lint y formato Python | Ruff (>= 0.15.6, entiende `lazy import`), PEP 8 |
| Pruebas backend | pytest y pytest-cov (cobertura mínima de 80 %) |
| Frontend | React (JavaScript, JSX), Vite+ (`vp`), Bun como gestor de paquetes |
| Estándar JS | ES2026, módulos ES (nada de CommonJS) |

Node.js sigue siendo el runtime de Vite+. Bun se usa como gestor de paquetes, no como runtime de las herramientas.

## Comandos

Todo junto: `scripts/setup.sh` instala dependencias y `scripts/verify.sh` ejecuta la verificación completa.

Backend (desde `backend/`):

```bash
uv python pin 3.15              # una sola vez; crea .python-version
uv sync                         # instala dependencias
uv run fastapi dev app/main.py  # desarrollo (requiere fastapi[standard])
uv run pytest --cov --cov-fail-under=80   # pruebas y cobertura
uv run ruff check .             # lint
uv run ruff format .            # formato
```

Frontend (desde `frontend/`):

```bash
vp install   # instala con Bun
vp dev       # desarrollo
vp check     # formato y lint
vp test      # pruebas
vp build     # build de producción
```

Los subcomandos de `vp` evolucionan rápido: confirma con `vp --help` antes de asumir uno.

## Arquitectura: 7 capas

La estructura completa de carpetas está en `spec/spec.md`, sección 4. Reglas de dependencia (una capa solo importa lo que su fila permite):

| Capa | Carpeta | Puede importar |
|---|---|---|
| 1. Presentación | `frontend/` | nada de Python; usa el contrato HTTP |
| 2. Interfaz de servicio | `backend/app/interface/` | `dto`, `services`, `security` |
| 3. Implementación del servicio | `backend/app/services/` | `dto`, `library_entities`, `domain` |
| 4. Tipos de datos | `backend/app/dto/` | nada |
| 5. Dominio (lógica del negocio) | `backend/app/domain/` | `library_entities`, `repositories`, `security` |
| 6. Entidades del negocio | `libs/library_entities/` | nada |
| 7. Repositorio de datos | `backend/app/repositories/` | `library_entities` |
| Transversal | `backend/app/security/` | nada de las capas |

Reglas que no se rompen:

- La presentación solo conoce **mensajes y tipos de datos**, nunca entidades.
- `domain` solo maneja **entidades**, nunca DTOs ni objetos de FastAPI.
- El **translator** convierte entidades en DTOs y viceversa; el **adapter** orquesta cada caso de uso.
- Solo `domain` llama al repositorio. Los endpoints y los adapters no lo tocan.
- Las entidades son clases puras (sin SQL, sin FastAPI, sin ORM). Los modelos de tablas viven en `repositories/orm_models/`.
- Las reglas de negocio (límites, multas, transiciones de estado) viven en entidades o en `domain`, nunca en endpoints.
- POO estricta en casi todas las capas; `security/`, `config.py` y `main.py` son flexibles (spec, sección 6).
- Cada carpeta de `backend/app/` lleva su `__init__.py`.

## Convenciones

- **Inglés** en variables, clases, funciones, archivos, carpetas y mensajes de commit (imperativo, asunto corto: `Add loan renewal rule`).
- **Español** solo en la prosa de los documentos y archivos de agentes, y en lo que ve el usuario final (interfaz y mensajes de error).
- **Comentarios bilingües**, solo los necesarios: primero en inglés y luego en español, como dos comentarios seguidos (`# EN:` y `# ES:`). No comentes lo que el código ya dice.
- PEP 8 aplicado con Ruff y anotaciones de tipo en funciones públicas. JavaScript con ES2026, módulos ES y componentes de función en archivos `.jsx`.
- Los tokens de color y tipografía salen de `DESIGN.md`; no pongas colores sueltos en los componentes.
- **Lazy imports (PEP 810)**: solo a nivel de módulo y para dependencias pesadas o poco usadas; nunca para nombres de firmas de endpoints o modelos Pydantic. Mide con `python -X importtime` antes de dejarlos.

## Seguridad

- Las contraseñas solo se guardan como hash Argon2id con `pwdlib`. Nunca en claro, nunca en logs.
- JWT de acceso de vida corta y refresh con rotación (detalle en la spec, RNF-2). El rol viaja en el token, pero los **permisos se resuelven en el servidor** a partir del rol.
- Cada endpoint declara el permiso que exige. Un endpoint sin permiso declarado es un error.
- Rate limit en login y en el resto de la API (RNF-3).
- Secretos solo en variables de entorno. `.env` nunca se versiona; `.env.example` sí.
- No registres datos personales ni tokens en logs.

## Carpetas de agentes

Lo común vive aquí y en la spec; cada carpeta solo concreta lo propio de su herramienta y no redefine reglas.

| Ruta | Herramienta | Contenido |
|---|---|---|
| `CLAUDE.md`, `.claude/` | Claude Code | Notas, permisos (`settings.json`), reglas por ruta (`rules/`) y comandos (`commands/`) |
| `.agents/` | Antigravity | `rules/` y `workflows/`; `templates/` guarda archivos base para tareas futuras |
| `.antigravity/` | Espacio de trabajo del IDE | `README.md`, `context/`, `commands/` y `resources/` (prototipos del frontend) |
| `scripts/` | Todos | `setup.sh` y `verify.sh` |

Los archivos personales (`CLAUDE.local.md`, `.claude/settings.local.json`) no se versionan.

## Reglas de trabajo

- Spec primero: un cambio de comportamiento tiene tres partes: edición de `spec/spec.md`, edición del código y pruebas.
- Una tarea cada vez, con las pruebas primero. El backend solo está completo cuando **todas** las pruebas unitarias pasan con al menos 80 % de cobertura.
- No añadas dependencias sin pedirlo. No edites a mano `uv.lock` ni el lockfile de Bun.
- No toques `.env`, `libs/` sin actualizar antes la spec, ni los archivos de licencia.
- Si algo es ambiguo, pregunta o anótalo en "Dudas abiertas" de la spec en lugar de inventar.

## Verificación obligatoria al terminar

Ejecuta `scripts/verify.sh` (o los pasos por separado) y reporta el resultado de:

1. `uv run ruff check .` y `uv run ruff format --check .` (en `backend/`)
2. `uv run pytest --cov --cov-fail-under=80` (incluye `test_architecture.py`)
3. `vp check`, `vp test` y `vp build` (en `frontend/`)
4. Que cada RF tocado tenga al menos una prueba, y que `spec/spec.md` esté actualizada si el comportamiento cambió.

Si algún paso no se pudo ejecutar, dilo explícitamente en lugar de omitirlo.

# Especificación: Sistema de Biblioteca

- **Estado:** borrador v0.3 (2026-10-22)
- **Documento vivo:** cualquier cambio de comportamiento se edita aquí primero, luego en el código.
- **Estructura:** sigue la plantilla del curso Hello SDD (contexto, usuarios, historias, requisitos en notación EARS, casos límite, fuera de alcance, criterios de finalización y dudas abiertas), con secciones añadidas para arquitectura, base de datos, reglas del backend, convenciones y carpetas de agentes.
- **Idioma:** la prosa de este documento está en español. Los nombres de carpetas, archivos, clases, variables y permisos están en inglés (ver sección 7).

## 1. Contexto

Sistema de biblioteca para una universidad: catálogo, préstamos, reservas y multas, con roles diferenciados (administración, desarrollo, bibliotecarios, caja, docentes y estudiantes).

Nace como ejemplo de arquitectura en **7 capas** para la exposición del tema 4 ("Implementación de librerías de entidades en una aplicación de software"), pero se diseña para crecer.

Referencias y restricciones:

- Existe una biblioteca digital institucional (acceso a recursos electrónicos con inicio de sesión por correo institucional). Este proyecto **no la reemplaza** y se usa solo como referencia de estilo (ver `DESIGN.md`).
- El backend (FastAPI) **no se expone públicamente**: solo es alcanzable a través de un proxy inverso, y su documentación técnica solo está disponible para el equipo de IT (ver RNF-1 y RF-8).
- Los logos y la marca de la universidad son propiedad de la institución y no forman parte de la licencia del código.

## 2. Usuarios, roles y permisos

### 2.1 Roles

| Rol (`id`) | Quién es | Descripción |
|---|---|---|
| `admin` | IT / administración del sistema | Control total: usuarios, roles, configuración, condonación de multas |
| `dev` | Desarrollo (IT) | Rol técnico: documentación de la API, logs técnicos y métricas. **Sin acceso a datos personales** |
| `librarian` | Personal de biblioteca (bibliotecario) | Gestiona catálogo, préstamos, devoluciones y reservas |
| `cashier` | Personal de caja | Cobra multas y emite comprobantes |
| `teacher` | Docentes | Como estudiante, con límites de préstamo más altos |
| `student` | Estudiantes | Consulta el catálogo, ve sus préstamos y multas, reserva y renueva |

### 2.2 Jerarquía

Orden de privilegios sobre los datos de negocio: `admin` > `librarian` > `cashier` > `teacher` > `student`.

`dev` queda **fuera** de esa escala: es un rol técnico paralelo con acceso mínimo, para que quien desarrolla no lea datos personales en producción (mínimo privilegio).

### 2.3 Matriz de permisos

Los permisos se resuelven en el servidor a partir del rol (`security/permissions.py`). El token solo lleva el rol.

| Permiso | admin | dev | librarian | cashier | teacher | student |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| `catalog:read` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| `catalog:manage` | ✔ | — | ✔ | — | — | — |
| `loan:create` | ✔ | — | ✔ | — | — | — |
| `loan:return` | ✔ | — | ✔ | — | — | — |
| `loan:view_own` | — | — | — | — | ✔ | ✔ |
| `loan:view_all` | ✔ | — | ✔ | — | — | — |
| `loan:renew_own` | — | — | — | — | ✔ | ✔ |
| `reservation:create_own` | — | — | — | — | ✔ | ✔ |
| `reservation:manage` | ✔ | — | ✔ | — | — | — |
| `fine:view_own` | — | — | — | — | ✔ | ✔ |
| `fine:view_all` | ✔ | — | ✔ | ✔ | — | — |
| `fine:collect` | ✔ | — | — | ✔ | — | — |
| `fine:waive` | ✔ | — | — | — | — | — |
| `user:manage` | ✔ | — | — | — | — | — |
| `system:docs` | ✔ | ✔ | — | — | — | — |
| `system:audit_read` | ✔ | ✔ (técnica) | — | — | — | — |
| `report:view` | ✔ | — | ✔ | ✔ (solo caja) | — | — |

Decisión de diseño: quien registra el préstamo (`librarian`) no cobra la multa (`cashier`), para separar funciones.

## 3. Historias de usuario

- **HU-1** Como estudiante, quiero buscar un libro y ver cuántos ejemplares están disponibles, para saber si puedo ir a pedirlo.
- **HU-2** Como estudiante o docente, quiero ver mis préstamos y multas y renovar un préstamo, para no tener que ir a la biblioteca solo por eso.
- **HU-3** Como estudiante o docente, quiero reservar un libro sin ejemplares disponibles, para que me lo aparten cuando lo devuelvan.
- **HU-4** Como bibliotecario, quiero registrar préstamos y devoluciones con pocos pasos, para atender rápido en el mostrador.
- **HU-5** Como bibliotecario, quiero gestionar libros y ejemplares, para mantener el catálogo al día.
- **HU-6** Como cajero, quiero cobrar una multa y entregar un comprobante, para cerrar el pago sin errores.
- **HU-7** Como administrador, quiero crear usuarios y asignar roles, para controlar quién hace qué.
- **HU-8** Como desarrollador, quiero consultar la documentación de la API y los logs técnicos en un entorno controlado, para mantener el sistema sin ver datos personales.

## 4. Arquitectura: 7 capas

### 4.1 Capas

| # | Capa | Responsabilidad | Ubicación |
|---|---|---|---|
| 1 | Presentación | Pantallas en el navegador. Conoce los tipos de datos y mensajes del servicio | `frontend/` |
| 2 | Interfaz de servicio | Lo que se expone: endpoints y tipos de mensajes (Request/Response) | `backend/app/interface/` |
| 3 | Implementación del servicio | **Adapter** (orquesta cada caso de uso) y **translator** (entidades ↔ tipos de datos) | `backend/app/services/` |
| 4 | Tipos de datos | Colección de tipos de datos que viajan hasta la implementación del servicio | `backend/app/dto/` |
| 5 | Dominio (lógica del negocio) | Reglas del sistema; maneja solo entidades | `backend/app/domain/` |
| 6 | Entidades del negocio | Objetos del dominio, como **librería independiente** | `libs/library_entities/` |
| 7 | Repositorio de datos | Inserción y extracción en la BD; habla solo con la BD y con la lógica de negocio | `backend/app/repositories/` |

Transversal: `backend/app/security/` (JWT, hashing, mapa de permisos y limitador). No depende de ninguna capa.

### 4.2 Estructura de carpetas

```plaintext
library-system/
├── AGENTS.md                           # common rules for every agent
├── CLAUDE.md                           # Claude Code: imports AGENTS.md
├── DESIGN.md                           # visual identity and tokens
├── LICENSE
├── NOTICE
├── README.md
├── .gitignore                          # ignores .env, CLAUDE.local.md and .claude/settings.local.json
├── .claude/                            # Claude Code (reads CLAUDE.md, never .agents/)
│   ├── settings.json                   # shared permissions
│   ├── rules/                          # rules scoped by path
│   │   ├── architecture.md
│   │   └── conventions.md
│   └── commands/
│       └── verify.md                   # /verify runs scripts/verify.sh
├── .agents/                            # Antigravity: rules and workflows
│   ├── rules/
│   │   ├── architecture.md
│   │   └── conventions.md
│   ├── workflows/
│   │   └── verify.md
│   └── templates/                      # base files for later tasks
├── .antigravity/                       # Antigravity workspace (not read automatically)
│   ├── README.md
│   ├── context/                        # reference material for the IDE
│   ├── commands/
│   └── resources/                      # frontend prototypes (Stitch / Claude Design exports)
├── .github/
├── .gitlab/
├── prompts/                            # task prompts, one per task
├── spec/
│   └── spec.md                         # this document
├── scripts/
│   ├── setup.sh                        # install dependencies
│   └── verify.sh                       # lint + tests + coverage + build
│
├── libs/
│   └── library_entities/               # 6. BUSINESS ENTITIES (standalone library)
│       ├── pyproject.toml
│       ├── tests/
│       └── library_entities/
│           ├── __init__.py             # exports the entities
│           ├── user.py
│           ├── book.py
│           ├── book_copy.py
│           ├── loan.py
│           ├── reservation.py
│           ├── fine.py
│           ├── payment.py
│           └── audit_log.py
│
├── backend/
│   ├── pyproject.toml                  # uv; requires-python >= 3.15
│   ├── uv.lock
│   ├── .python-version                 # 3.15
│   ├── .env.example
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                     # composition root (flexible)
│   │   ├── config.py                   # settings (flexible)
│   │   │
│   │   ├── security/                   # cross-cutting (flexible)
│   │   │   ├── __init__.py
│   │   │   ├── jwt.py                  # JWT (PyJWT)
│   │   │   ├── hashing.py              # pwdlib[argon2]
│   │   │   ├── permissions.py          # role -> permissions map
│   │   │   └── rate_limiter.py
│   │   │
│   │   ├── interface/                  # 2. SERVICE INTERFACE
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth_endpoint.py
│   │   │   │   ├── catalog_endpoint.py
│   │   │   │   ├── loan_endpoint.py
│   │   │   │   ├── reservation_endpoint.py
│   │   │   │   ├── fine_endpoint.py
│   │   │   │   └── user_endpoint.py
│   │   │   └── messages/               # Request / Response
│   │   │       ├── __init__.py
│   │   │       ├── auth_messages.py
│   │   │       ├── loan_messages.py
│   │   │       └── fine_messages.py
│   │   │
│   │   ├── services/                   # 3. SERVICE IMPLEMENTATION
│   │   │   ├── __init__.py
│   │   │   ├── adapters/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── loan_adapter.py
│   │   │   │   └── fine_adapter.py
│   │   │   └── translators/
│   │   │       ├── __init__.py
│   │   │       ├── book_translator.py
│   │   │       ├── loan_translator.py
│   │   │       └── fine_translator.py
│   │   │
│   │   ├── dto/                        # 4. DATA TYPES (DTOs)
│   │   │   ├── __init__.py
│   │   │   ├── book_dto.py
│   │   │   ├── loan_dto.py
│   │   │   └── fine_dto.py
│   │   │
│   │   ├── domain/                    # 5. DOMAIN (business logic)
│   │   │   ├── __init__.py
│   │   │   ├── auth_domain.py
│   │   │   ├── catalog_domain.py
│   │   │   ├── loan_domain.py
│   │   │   ├── reservation_domain.py
│   │   │   └── fine_domain.py
│   │   │
│   │   └── repositories/               # 7. DATA REPOSITORY
│   │       ├── __init__.py
│   │       ├── db/
│   │       │   ├── __init__.py
│   │       │   └── connection.py       # generic connection class
│   │       ├── base_repository.py      # abstract contract used by domain and test fakes
│   │       ├── orm_models/             # table mappings; they are not entities
│   │       ├── migrations/             # Alembic
│   │       ├── book_repository.py
│   │       ├── loan_repository.py
│   │       └── fine_repository.py      # one repository per aggregate
│   └── tests/
│       ├── conftest.py
│       ├── fakes/                      # in-memory repositories
│       ├── test_architecture.py        # checks the import rules between layers
│       └── unit/
│           ├── domain/
│           ├── services/
│           ├── interface/
│           ├── repositories/
│           └── security/
│
└── frontend/                           # 1. PRESENTATION
    ├── package.json                    # devEngines: bun
    ├── bunfig.toml                     # Bun settings (equivalent of .npmrc)
    ├── .node-version                   # Node, runtime of Vite+
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── api/                        # calls to the service interface
        ├── components/
        ├── pages/
        ├── hooks/
        ├── styles/                     # tokens from DESIGN.md
        └── main.jsx
```

### 4.3 Reglas de dependencia

| Capa | Puede importar |
|---|---|
| `interface` | `dto`, `services`, `security` |
| `services` | `dto`, `library_entities`, `domain` |
| `dto` | nada |
| `domain` | `library_entities`, `repositories`, `security` |
| `library_entities` | nada |
| `repositories` | `library_entities` |
| `security` | nada de las capas |

`tests/test_architecture.py` recorre los imports (con `ast`) y falla si alguna capa importa algo fuera de su fila.

### 4.4 Flujo de una petición (préstamo)

```plaintext
Frontend (pages -> api)
   │  RegisterLoanRequest (message) with data types
   ▼
interface/endpoints      checks the permission, receives the message
   ▼
services/adapters  orchestrates the use case
   │  translators: DTO -> Entity
   ▼
domain                   applies the rules (RF-11 to RF-13)
   ▼
repositories -> db/connection -> DB   persists
   ▲
   │  Entity -> DTO (translator) -> Response -> Frontend
```

## 5. Base de datos y ORM

### 5.1 Motores soportados

| Motor | Rol | Driver |
|---|---|---|
| PostgreSQL | Principal | `psycopg[binary]` (`postgresql+psycopg://`) |
| MySQL | Secundario | `PyMySQL` (`mysql+pymysql://`) |
| MariaDB | Secundario | `PyMySQL` (`mariadb+pymysql://`) |

SQLite en memoria se usa **solo en pruebas unitarias** del repositorio; no es un motor soportado en producción.

### 5.2 ORM elegido: SQLAlchemy 2.1 + Alembic

Dependencia: `sqlalchemy>=2.1,<2.2`, con **Alembic** para migraciones.

Por qué SQLAlchemy:

- **Cubre los tres motores** con dialectos propios (PostgreSQL, MySQL y MariaDB), de modo que un solo repositorio sirve para todos y la conexión sigue siendo una clase genérica que solo cambia de URL.
- **Soporte de Python 3.15:** la versión 2.1.5 publica ruedas para CPython 3.15, incluida Windows x86-64, y `psycopg-binary` 3.3.6 también.
- **Mapeo imperativo:** permite mapear clases simples a tablas sin que hereden de una base del ORM. Así las entidades de `library_entities` siguen siendo puras (sin importar SQLAlchemy) y el mapeo vive en `repositories/orm_models/`. Es lo que pide el tema 4.
- Es el ORM más extendido del ecosistema Python, con documentación extensa y mantenimiento activo.

Alternativas descartadas:

- **SQLModel:** une entidad, tabla y modelo Pydantic en una sola clase, que es lo contrario de separar entidades y repositorio.
- **Tortoise ORM, Peewee, Piccolo:** ecosistemas más pequeños o con menos soporte de migraciones y de mapeo imperativo; Piccolo además se centra en PostgreSQL y SQLite.
- **Django ORM:** acoplado a Django.

Drivers: `PyMySQL` es Python puro, así que no depende de ruedas compiladas para 3.15. Se evita `mysqlclient` y el conector oficial de MariaDB porque exigen compilación o bibliotecas del sistema.

### 5.3 Reglas de portabilidad

- `DatabaseConnection` (en `repositories/db/connection.py`) recibe la URL desde `config.py`, crea el `Engine` y entrega sesiones. No hay código específico de un motor fuera de `connection.py` y de `orm_models/`.
- Solo tipos genéricos de SQLAlchemy (`Uuid`, `Numeric(10, 2)` para dinero, `DateTime`). Las fechas se guardan en UTC; MySQL y MariaDB no guardan zona horaria, por lo que se guarda UTC "ingenuo" y se convierte en la capa de implementación.
- MySQL y MariaDB con InnoDB y `utf8mb4`.
- **Sin índices parciales:** MySQL y MariaDB no los soportan. La regla "un ejemplar no se presta dos veces" se aplica con bloqueo de fila (`with_for_update()`) sobre el ejemplar dentro de la transacción, que funciona en los tres motores.
- Las migraciones se prueban en los tres motores antes de una versión.

## 6. Reglas del backend

### 6.1 POO estricta

- Todo comportamiento vive en clases. No hay lógica de negocio en funciones sueltas de módulo.
- Una clase principal por archivo, con el nombre del archivo en `snake_case` (`LoanDomain` → `loan_domain.py`).
- Dependencias por constructor (inyección). El punto de composición es `main.py`, donde se arman repositorios, lógica de negocio, adapters y endpoints.
- Los endpoints son clases que exponen un `APIRouter`; cada manejador es un método.
- Las entidades son ricas: contienen sus reglas y transiciones de estado, y protegen sus invariantes (atributos privados con prefijo `_` y métodos públicos para cambiarlos).
- Los repositorios implementan un contrato abstracto (`BaseRepository`, con `abc.ABC`), de modo que las pruebas usan repositorios en memoria que respetan el mismo contrato.
- Composición antes que herencia. Los mensajes y DTOs son modelos Pydantic sin comportamiento (solo datos).
- Anotaciones de tipo en toda la API pública.

### 6.2 Zonas flexibles

`security/`, `config.py` y `main.py` pueden usar funciones y objetos de módulo cuando FastAPI lo pide (por ejemplo, dependencias `Depends`, un objeto de configuración o una fábrica de aplicación). Fuera de ahí, aplica 6.1.

### 6.3 Pruebas unitarias con pytest

- Todas las pruebas unitarias se escriben en `backend/tests/`, con la estructura de `tests/unit/` reflejando las capas. La librería de entidades tiene sus propias pruebas en `libs/library_entities/tests/`.
- Herramienta: `pytest` con `pytest-cov`.
- **Cobertura mínima: 80%** del código, tanto en `app/` como en `library_entities/`. Si baja del umbral, la ejecución falla (`--cov-fail-under=80`).
- Las pruebas unitarias no usan red ni un motor de BD real: la lógica de negocio se prueba con repositorios en memoria (`tests/fakes/`) y los repositorios con SQLite en memoria.
- Las pruebas de integración contra PostgreSQL, MySQL y MariaDB van marcadas con `@pytest.mark.integration` y no cuentan para el umbral.
- Ciclo de trabajo: implementar, ejecutar `uv run pytest`, corregir y repetir hasta que todo pase y la cobertura sea de al menos 80%.

## 7. Convenciones

- **Inglés** en variables, clases, funciones, archivos, carpetas y mensajes de commit. Los mensajes de commit van en modo imperativo y con un asunto corto (`Add loan renewal rule`).
- **Español** solo en la prosa de los documentos (`spec.md`, `AGENTS.md`, `DESIGN.md`, reglas y flujos de los agentes) y en los textos que ve el usuario final en la interfaz.
- **Comentarios bilingües:** primero en inglés y luego en español, como dos comentarios seguidos, y solo cuando son necesarios para entender el código (una regla no obvia, una decisión o un riesgo). No se comenta lo que el código ya dice.

```python
# EN: The fine uses the rate in force on the return date, not on the loan date.
# ES: La multa usa la tarifa vigente el día de la devolución, no el del préstamo.
```

```javascript
// EN: The token is refreshed only once per request burst.
// ES: El token se renueva solo una vez por ráfaga de peticiones.
```

- PEP 8 en Python (Ruff) y ES2026 en JavaScript.
- Lazy imports (PEP 810) a nivel de módulo y solo para dependencias pesadas; reglas en `AGENTS.md`.

## 8. Modelo de dominio

Las entidades son clases puras en `libs/library_entities/`: sin SQL, sin FastAPI, sin ORM. Los modelos de tablas viven en `repositories/orm_models/` y el repositorio convierte entre ambos con mapeo imperativo.

| Entidad | Atributos principales | Reglas propias |
|---|---|---|
| `User` | id, institutional_email (único), name, role, active | Un usuario inactivo no inicia sesión ni pide préstamos |
| `Book` | id, isbn (único, opcional), title, authors, category, publisher, year | El ISBN, si existe, es único |
| `BookCopy` | id, book_id, inventory_code (único), status | Estados: `AVAILABLE`, `LOANED`, `RESERVED`, `UNDER_REPAIR`, `WITHDRAWN`. Un ejemplar prestado no se vuelve a prestar |
| `Loan` | id, copy_id, user_id, loaned_at, due_at, returned_at, renewals, status | `renew()` respeta el máximo de renovaciones; `days_late(today)` |
| `Reservation` | id, book_id, user_id, created_at, status, held_until | Estados: `QUEUED`, `HELD`, `FULFILLED`, `CANCELLED`, `EXPIRED` |
| `Fine` | id, loan_id, user_id, days_late, amount, status, waiver_reason | Estados: `PENDING`, `PAID`, `WAIVED`. `pay()` y `waive(reason)` |
| `Payment` | id, fine_id, cashier_id, amount, receipt_number (único), paid_at | Un número de comprobante no se repite |
| `AuditLog` | id, user_id, action, entity, entity_id, created_at | Solo se agrega; nunca se edita |

### 8.1 Parámetros configurables

Valores por defecto **supuestos**: se validan con la biblioteca antes de usarlos y viven en configuración, no en el código.

| Parámetro | `student` | `teacher` |
|---|---|---|
| `max_active_loans` | 3 | 5 |
| `loan_days` | 7 | 15 |
| `max_renewals` | 1 | 2 |
| `reservation_hold_hours` | 48 | 48 |
| `fine_per_day` | definir | definir |

## 9. Requisitos funcionales (EARS)

Patrones: *El sistema deberá…* (siempre) · *Cuando…* (evento) · *Mientras…* (estado) · *Si…, entonces…* (situación no deseada) · *Donde…* (opción activada).

### Autenticación y sesión

- **RF-1** Cuando un usuario envíe credenciales válidas, el sistema deberá emitir un token de acceso de 15 minutos y un token de refresco de 7 días.
- **RF-2** Si las credenciales son inválidas, entonces el sistema deberá responder 401 con un mensaje genérico que no revele si el usuario existe.
- **RF-3** Si una misma combinación de IP y usuario supera 5 intentos de inicio de sesión en un minuto, entonces el sistema deberá responder 429 y rechazar nuevos intentos durante 15 minutos.
- **RF-4** Mientras un token esté expirado, revocado o tenga firma inválida, el sistema deberá rechazar la solicitud con 401.
- **RF-5** Cuando un usuario cierre sesión, el sistema deberá revocar su token de refresco.
- **RF-6** El sistema deberá guardar las contraseñas solo como hash Argon2id (`pwdlib`) y volver a hashear en el siguiente inicio de sesión si los parámetros cambiaron.

### Autorización

- **RF-7** Cuando llegue una solicitud autenticada, el sistema deberá comprobar el permiso que exige el endpoint según el rol del usuario, y si no lo tiene, deberá responder 403.
- **RF-8** Mientras el entorno sea producción, el sistema no deberá publicar `/docs`, `/redoc` ni `/openapi.json`. Donde el entorno sea de desarrollo, solo deberán ser accesibles con el permiso `system:docs`.

### Catálogo

- **RF-9** Cuando un usuario autenticado busque por título, autor, ISBN o categoría, el sistema deberá devolver resultados paginados con el número de ejemplares disponibles.
- **RF-10** Cuando un bibliotecario cree un libro, el sistema deberá validar que el ISBN, si se informa, no exista y deberá permitir registrar uno o más ejemplares con código de inventario único.

### Préstamos

- **RF-11** Cuando un bibliotecario registre un préstamo, el sistema deberá verificar que el usuario esté activo, que no tenga multas pendientes, que no supere el límite de préstamos de su rol y que el ejemplar esté disponible, y deberá fijar la fecha de vencimiento según el rol.
- **RF-12** Si el usuario tiene multas pendientes, entonces el sistema deberá rechazar el préstamo e indicar el motivo en un mensaje claro.
- **RF-13** Cuando se registre una devolución, el sistema deberá dejar el ejemplar disponible y, si hubo retraso, deberá generar una multa igual a los días de retraso por la tarifa vigente.
- **RF-14** Cuando un usuario solicite renovar un préstamo, el sistema deberá extender el vencimiento solo si no superó las renovaciones máximas y no existe una reserva en cola sobre ese libro.

### Reservas

- **RF-15** Cuando todos los ejemplares de un libro estén prestados y un usuario reserve ese libro, el sistema deberá encolar la reserva por orden de llegada.
- **RF-16** Cuando se devuelva un ejemplar con reservas en cola, el sistema deberá apartarlo para la primera reserva durante el tiempo configurado y deberá expirar la reserva si no se retira a tiempo.

### Multas y pagos

- **RF-17** Cuando caja registre el pago de una multa, el sistema deberá marcarla como pagada y emitir un comprobante con número único.
- **RF-18** Cuando un administrador condone una multa, el sistema deberá exigir un motivo y registrar quién la condonó.

### Usuarios y auditoría

- **RF-19** Cuando un administrador cambie el rol o desactive a un usuario, el sistema deberá revocar todos los tokens de refresco de ese usuario.
- **RF-20** El sistema deberá registrar en auditoría toda operación de escritura (quién, qué y cuándo), sin guardar contraseñas ni tokens.

## 10. Requisitos no funcionales y seguridad

- **RNF-1 Exposición.** El backend no es accesible directamente desde internet: escucha en red interna (o en `127.0.0.1` en desarrollo) detrás de un proxy inverso, y la base de datos no tiene exposición externa.
- **RNF-2 JWT.** Algoritmo HS256 con un secreto aleatorio de al menos 32 bytes en variable de entorno. Claims: `sub`, `role`, `iat`, `exp`, `jti`. Acceso de 15 minutos. Refresco de 7 días con rotación en cada uso, guardado como hash en la BD; si se reutiliza uno ya rotado, se revoca toda la sesión.
- **RNF-3 Rate limit.** Login: 5 intentos por minuto por IP y usuario. Resto de la API: 120 solicitudes por minuto por usuario autenticado. Respuesta 429 con `Retry-After`.
- **RNF-4 Contraseñas.** Argon2id con `pwdlib[argon2]` con parámetros iguales o superiores al mínimo de OWASP (19 MiB de memoria, 2 iteraciones, paralelismo 1), ajustados midiendo en el servidor.
- **RNF-5 Datos personales.** Los logs no contienen contraseñas, tokens ni datos personales. El rol `dev` no accede a datos personales.
- **RNF-6 CORS.** Orígenes permitidos explícitos; nunca `*`.
- **RNF-7 Fechas.** Se guardan en UTC y se muestran en `America/El_Salvador`.
- **RNF-8 Calidad.** Python con PEP 8 (Ruff) y JavaScript con ES2026. Cobertura mínima de 80% en el backend y en la librería de entidades (sección 6.3). Cada RF tiene al menos una prueba.
- **RNF-9 Accesibilidad.** WCAG 2.2 AA. En las pantallas de caja: texto de al menos 18 px, botones de al menos 48 px y el flujo de cobro en 3 pantallas o menos (supuesto a validar con los cajeros).
- **RNF-10 Portabilidad de BD.** Mismo código para PostgreSQL, MySQL y MariaDB (sección 5.3).

## 11. Interfaz y diseño

Identidad visual y tokens en `DESIGN.md`. Los prototipos exportados van en `.antigravity/resources/`.

Pantallas del alcance v1:

1. Inicio de sesión
2. Búsqueda de catálogo y detalle de libro
3. Mis préstamos, reservas y multas (estudiante y docente)
4. Mostrador del bibliotecario: préstamo y devolución
5. Gestión de catálogo (libros y ejemplares)
6. Caja: cobro de multas
7. Administración de usuarios y roles

Principio de diseño: pocas decisiones por pantalla, botones grandes y mensajes claros en español, pensados para personal de caja de mayor edad.

## 12. Carpetas de agentes

Cada herramienta lee su propia carpeta. Lo común está en `AGENTS.md` y `spec/spec.md`; las carpetas de agentes solo concretan lo específico de cada herramienta y no redefinen reglas.

| Carpeta o archivo | Quién lo lee | Contenido |
|---|---|---|
| `AGENTS.md` | Varias herramientas, incluida Antigravity | Instrucciones comunes del repo |
| `CLAUDE.md` | Claude Code | Importa `AGENTS.md` y añade notas específicas |
| `.claude/` | Claude Code | `settings.json` (permisos), `rules/` (reglas por ruta) y `commands/` (como `/verify`) |
| `.agents/` | Antigravity (Claude Code **no** la lee) | `rules/`, `workflows/` y `templates/` (archivos base para tareas futuras) |
| `.antigravity/` | Nadie la lee de forma automática: es una carpeta de trabajo del repo | `README.md` con las notas del IDE, `context/`, `commands/` y `resources/` con los prototipos del frontend (exportaciones de Stitch o Claude Design) |
| `scripts/` | Todos | `setup.sh` y `verify.sh`, que ejecutan las mismas comprobaciones |

Los archivos personales de cada herramienta (`CLAUDE.local.md`, `.claude/settings.local.json`) no se versionan.

## 13. Casos límite

- Dos bibliotecarios prestan el mismo ejemplar a la vez: el bloqueo de fila sobre el ejemplar dentro de la transacción deja que gane solo uno.
- Devolución de un ejemplar que no está prestado: se rechaza sin cambiar estados.
- Vencimiento que cae en día no hábil: se define en las dudas abiertas (D-4).
- El rol de un usuario cambia con un token de acceso todavía vigente: el token solo vive 15 minutos y RF-19 revoca los refrescos.
- La tarifa de multa cambia después de un retraso: la multa conserva la tarifa vigente al momento de la devolución.
- Usuario desactivado con préstamos activos: los préstamos siguen su curso y no puede pedir nuevos.
- El mismo usuario reserva dos veces el mismo libro: se rechaza la segunda.
- ISBN duplicado o con formato inválido: se rechaza con un mensaje que indique cuál es el problema.
- Cambio de motor de BD con datos existentes: no está soportado en caliente; requiere exportar e importar.

## 14. Fuera de alcance (v1)

- Lectura de recursos digitales (PDF o libros electrónicos).
- Pagos en línea.
- Integración con el catálogo, la renovación o la solvencia ya existentes de la universidad.
- Aplicación móvil.
- Notificaciones por correo o mensajería.
- Importación masiva de catálogo.

## 15. Criterios de finalización

- Cada RF tiene al menos una prueba que pasa.
- `uv run pytest` pasa con una cobertura de al menos 80% (incluida `test_architecture.py`), y lo mismo para `libs/library_entities`.
- `uv run ruff check .` y `uv run ruff format --check .` pasan.
- `vp check`, `vp test` y `vp build` pasan.
- En producción, `/docs`, `/redoc` y `/openapi.json` no responden (verificado con una prueba).
- No hay secretos en el repositorio y `.env.example` está al día.
- Esta especificación refleja el comportamiento real.

## 16. Dudas abiertas

- **D-1 (resuelta)** Base de datos y ORM: SQLAlchemy 2.1 con Alembic; PostgreSQL principal y MySQL/MariaDB secundarias (sección 5).
- **D-2 "Sin exposición pública".** Interpretado así: el backend no es accesible directamente y solo recibe tráfico del proxy inverso; el frontend sí es público. Falta aclarar si los usuarios deben llegar al sistema desde fuera del campus (internet o solo red interna o VPN).
- **D-3 Librería de rate limit.** Candidatos: `slowapi` (memoria, un solo proceso) o un limitador con Redis (varios procesos). Verificar mantenimiento antes de elegir.
- **D-4 Calendario.** ¿Los vencimientos se corren si caen en día no hábil o feriado?
- **D-5 Valores de negocio.** Límites, plazos y tarifa de multa (sección 8.1): validar con la biblioteca.
- **D-6 Navegadores soportados.** ES2026 puro puede excluir navegadores antiguos; definir el `build.target` según los dispositivos reales de los usuarios.
- **D-7 Compatibilidad con Python 3.15.** SQLAlchemy 2.1.5 y `psycopg-binary` 3.3.6 ya publican ruedas para 3.15. Falta confirmar el resto (Pydantic, Argon2, PyMySQL y las herramientas de prueba) con `uv sync`; si algo falla, usar 3.14 y subir después.
- **D-8 Inicio de sesión.** ¿Cuentas propias del sistema o integración con la identidad institucional (correo institucional, SSO)? Dominio del correo por confirmar.
- **D-9 Licencia y propiedad intelectual.** Elegir licencia (ver `LICENSE.md`) y confirmar con la universidad si hay una política de propiedad intelectual sobre proyectos de curso.
- **D-13 Cambios previos en el backend.** Esta especificación aún no refleja las modificaciones que ya hiciste en el backend; falta alinear nombres y estructura con tu código actual.
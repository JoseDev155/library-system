# Especificación: Sistema de Biblioteca

- **Estado:** borrador v0.1 (2026-10-21)
- **Documento vivo:** cualquier cambio de comportamiento se edita aquí primero, luego en el código.
- **Estructura:** sigue la plantilla del curso Hello SDD (contexto, usuarios, historias, requisitos en notación EARS, casos límite, fuera de alcance, criterios de finalización y dudas abiertas), con secciones añadidas para arquitectura, dominio, seguridad y diseño.

## 1. Contexto

Sistema de biblioteca para una universidad: catálogo, préstamos, reservas y multas, con roles diferenciados (administración, desarrollo, bibliotecarios, caja, docentes y estudiantes).

Nace como ejemplo de arquitectura en **7 capas** para la exposición del tema 4 ("Implementación de librerías de entidades en una aplicación de software"), pero se diseña para crecer.

Referencias y restricciones:

- Existe una biblioteca digital institucional (acceso a recursos electrónicos con inicio de sesión por correo institucional). Este proyecto **no la reemplaza** y se usa solo como referencia de estilo (ver `DESIGN.md`).
- El backend (FastAPI) **no se expone públicamente**: solo es alcanzable a través de un proxy inverso, y su documentación técnica solo está disponible para el equipo de IT (ver RNF-1 y RF-8).
- Los logos y la marca de la universidad son propiedad de la institución y no forman parte de la licencia del código.

## 2. Usuarios, roles y permisos

### 2.1 Roles

| Rol | Quién es | Descripción |
|---|---|---|
| `admin` | IT / administración del sistema | Control total: usuarios, roles, configuración, condonación de multas |
| `dev` | Desarrollo (IT) | Rol técnico: documentación de la API, logs técnicos y métricas. **Sin acceso a datos personales** |
| `bibliotecario` | Personal de biblioteca | Gestiona catálogo, préstamos, devoluciones y reservas |
| `caja` | Personal de caja | Cobra multas y emite comprobantes |
| `docente` | Docentes | Como estudiante, con límites de préstamo más altos |
| `estudiante` | Estudiantes | Consulta el catálogo, ve sus préstamos y multas, reserva y renueva |

### 2.2 Jerarquía

Orden de privilegios sobre los datos de negocio: `admin` > `bibliotecario` > `caja` > `docente` > `estudiante`.

`dev` queda **fuera** de esa escala: es un rol técnico paralelo con acceso mínimo, para que quien desarrolla no lea datos personales en producción (mínimo privilegio).

### 2.3 Matriz de permisos

Los permisos se resuelven en el servidor a partir del rol (`seguridad/permisos.py`). El token solo lleva el rol.

| Permiso | admin | dev | bibliotecario | caja | docente | estudiante |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| `catalogo:leer` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| `catalogo:gestionar` | ✔ | — | ✔ | — | — | — |
| `prestamo:crear` | ✔ | — | ✔ | — | — | — |
| `prestamo:devolver` | ✔ | — | ✔ | — | — | — |
| `prestamo:ver_propios` | — | — | — | — | ✔ | ✔ |
| `prestamo:ver_todos` | ✔ | — | ✔ | — | — | — |
| `prestamo:renovar_propio` | — | — | — | — | ✔ | ✔ |
| `reserva:crear_propia` | — | — | — | — | ✔ | ✔ |
| `reserva:gestionar` | ✔ | — | ✔ | — | — | — |
| `multa:ver_propias` | — | — | — | — | ✔ | ✔ |
| `multa:ver_todas` | ✔ | — | ✔ | ✔ | — | — |
| `multa:cobrar` | ✔ | — | — | ✔ | — | — |
| `multa:condonar` | ✔ | — | — | — | — | — |
| `usuario:gestionar` | ✔ | — | — | — | — | — |
| `sistema:docs` | ✔ | ✔ | — | — | — | — |
| `sistema:auditoria_leer` | ✔ | ✔ (técnica) | — | — | — | — |
| `reporte:ver` | ✔ | — | ✔ | ✔ (solo caja) | — | — |

Decisión de diseño: quien registra el préstamo (`bibliotecario`) no cobra la multa (`caja`), para separar funciones.

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
| 2 | Interfaz de servicio | Lo que se expone: endpoints y tipos de mensajes (Request/Response) | `backend/app/interfaz_servicio/` |
| 3 | Implementación del servicio | **Adapter** (orquesta cada caso de uso) y **translator** (entidades ↔ tipos de datos) | `backend/app/implementacion_servicio/` |
| 4 | Tipos de datos | Colección de tipos de datos que viajan hasta la implementación del servicio | `backend/app/tipos_datos/` |
| 5 | Lógica del negocio | Reglas del sistema; maneja solo entidades | `backend/app/negocio/` |
| 6 | Entidades del negocio | Objetos del dominio, como **librería independiente** | `libs/biblioteca_entidades/` |
| 7 | Repositorio de datos | Inserción y extracción en la BD; habla solo con la BD y con `negocio` | `backend/app/repositorio/` |

Transversal: `backend/app/seguridad/` (JWT, hashing, mapa de permisos y limitador). No depende de ninguna capa.

### 4.2 Estructura de carpetas

```plaintext
biblioteca/
├── AGENTS.md
├── CLAUDE.md
├── DESIGN.md
├── LICENSE.md
├── NOTICE.md
├── README.md
├── spec.md
├── .gitignore                         # incluye CLAUDE.local.md y .claude/settings.local.json
├── .claude/                           # Claude Code
│   ├── settings.json
│   └── rules/
├── .agents/                           # Antigravity (opcional)
├── prototipos/                        # exportaciones de Claude Design / Stitch
│
├── libs/
│   └── biblioteca_entidades/          # 6. ENTIDADES DEL NEGOCIO (librería)
│       ├── pyproject.toml
│       ├── tests/
│       └── biblioteca_entidades/
│           ├── __init__.py            # expone las entidades
│           ├── usuario.py
│           ├── libro.py
│           ├── ejemplar.py
│           ├── prestamo.py
│           ├── reserva.py
│           ├── multa.py
│           └── pago.py
│
├── backend/
│   ├── pyproject.toml                 # uv; requires-python >= 3.15
│   ├── uv.lock
│   ├── .python-version                # 3.15
│   ├── .env.example
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   │
│   │   ├── seguridad/                 # transversal
│   │   │   ├── __init__.py
│   │   │   ├── jwt.py
│   │   │   ├── hashing.py             # pwdlib[argon2]
│   │   │   ├── permisos.py            # mapa rol -> permisos
│   │   │   └── limitador.py           # rate limit
│   │   │
│   │   ├── interfaz_servicio/         # 2. INTERFAZ DE SERVICIO
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth_endpoint.py
│   │   │   │   ├── catalogo_endpoint.py
│   │   │   │   ├── prestamos_endpoint.py
│   │   │   │   ├── reservas_endpoint.py
│   │   │   │   ├── multas_endpoint.py
│   │   │   │   └── usuarios_endpoint.py
│   │   │   └── mensajes/              # Request / Response
│   │   │       ├── __init__.py
│   │   │       ├── auth_mensajes.py
│   │   │       ├── prestamos_mensajes.py
│   │   │       └── multas_mensajes.py
│   │   │
│   │   ├── implementacion_servicio/   # 3. IMPLEMENTACIÓN DEL SERVICIO
│   │   │   ├── __init__.py
│   │   │   ├── adapters/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── prestamos_adapter.py
│   │   │   │   └── multas_adapter.py
│   │   │   └── translators/
│   │   │       ├── __init__.py
│   │   │       ├── libro_translator.py
│   │   │       ├── prestamo_translator.py
│   │   │       └── multa_translator.py
│   │   │
│   │   ├── tipos_datos/               # 4. TIPOS DE DATOS (DTOs)
│   │   │   ├── __init__.py
│   │   │   ├── libro_dto.py
│   │   │   ├── prestamo_dto.py
│   │   │   └── multa_dto.py
│   │   │
│   │   ├── negocio/                   # 5. LÓGICA DEL NEGOCIO
│   │   │   ├── __init__.py
│   │   │   ├── auth_negocio.py
│   │   │   ├── catalogo_negocio.py
│   │   │   ├── prestamos_negocio.py
│   │   │   ├── reservas_negocio.py
│   │   │   └── multas_negocio.py
│   │   │
│   │   └── repositorio/               # 7. REPOSITORIO DE DATOS
│   │       ├── __init__.py
│   │       ├── conexion.py            # clase genérica de conexión
│   │       ├── modelos_orm/           # tablas (mapeo); no son entidades
│   │       ├── migraciones/
│   │       ├── libro_repositorio.py
│   │       ├── prestamo_repositorio.py
│   │       └── multa_repositorio.py
│   └── tests/
│       ├── test_arquitectura.py       # verifica las reglas de importación entre capas
│       └── ...
│
└── frontend/                          # 1. PRESENTACIÓN
    ├── package.json                   # devEngines: bun
    ├── bunfig.toml                    # equivalente de .npmrc
    ├── .node-version                  # Node para Vite+
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── api/                       # llamadas a la interfaz de servicio
        ├── components/
        ├── pages/
        ├── hooks/
        ├── styles/                    # tokens de DESIGN.md
        └── main.jsx
```

### 4.3 Reglas de dependencia

| Capa | Puede importar |
|---|---|
| `interfaz_servicio` | `tipos_datos`, `implementacion_servicio`, `seguridad` |
| `implementacion_servicio` | `tipos_datos`, `biblioteca_entidades`, `negocio` |
| `tipos_datos` | nada |
| `negocio` | `biblioteca_entidades`, `repositorio`, `seguridad` |
| `biblioteca_entidades` | nada |
| `repositorio` | `biblioteca_entidades` |
| `seguridad` | nada de las capas |

`tests/test_arquitectura.py` recorre los imports (con `ast`) y falla si alguna capa importa algo fuera de su fila.

### 4.4 Flujo de una petición (préstamo)

```plaintext
Frontend (pages -> api)
   │  RegistrarPrestamoRequest (mensaje) con tipos de datos
   ▼
interfaz_servicio/endpoints      valida el permiso, recibe el mensaje
   ▼
implementacion_servicio/adapters orquesta el caso de uso
   │  translators: DTO -> Entidad
   ▼
negocio                          aplica las reglas (RF-11 a RF-13)
   ▼
repositorio -> conexion -> BD    guarda
   ▲
   │  Entidad -> DTO (translator) -> Response -> Frontend
```

## 5. Modelo de dominio

Las entidades son clases puras en `libs/biblioteca_entidades/`: sin SQL, sin FastAPI, sin ORM. Los modelos de tablas viven en `repositorio/modelos_orm/` y el repositorio convierte entre ambos.

| Entidad | Atributos principales | Reglas propias |
|---|---|---|
| `Usuario` | id, correo_institucional (único), nombre, rol, activo | Un usuario inactivo no inicia sesión ni pide préstamos |
| `Libro` | id, isbn (único, opcional), titulo, autores, categoria, editorial, anio | El ISBN, si existe, es único |
| `Ejemplar` | id, libro_id, codigo_inventario (único), estado | Transiciones: disponible → prestado → disponible; disponible → reservado; cualquiera → en_reparacion o baja. Un ejemplar prestado no se vuelve a prestar |
| `Prestamo` | id, ejemplar_id, usuario_id, fecha_prestamo, fecha_vencimiento, fecha_devolucion, renovaciones, estado | `renovar()` respeta el máximo de renovaciones; `dias_de_retraso(hoy)` |
| `Reserva` | id, libro_id, usuario_id, creada_en, estado, apartada_hasta | Estados: en_cola, apartada, cumplida, cancelada, expirada |
| `Multa` | id, prestamo_id, usuario_id, dias_retraso, monto, estado, motivo_condonacion | Estados: pendiente, pagada, condonada. `pagar()` y `condonar(motivo)` |
| `Pago` | id, multa_id, cajero_id, monto, folio (único), fecha | Un folio no se repite |
| `RegistroAuditoria` | id, usuario_id, accion, entidad, entidad_id, fecha | Solo se agrega; nunca se edita |

### 5.1 Parámetros configurables

Valores por defecto **supuestos**: se validan con la biblioteca antes de usarlos y viven en configuración, no en el código.

| Parámetro | Estudiante | Docente |
|---|---|---|
| Préstamos simultáneos máximos | 3 | 5 |
| Plazo de préstamo (días) | 7 | 15 |
| Renovaciones máximas | 1 | 2 |
| Horas que se aparta una reserva | 48 | 48 |
| Multa por día de retraso | definir | definir |

## 6. Requisitos funcionales (EARS)

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
- **RF-8** Mientras el entorno sea producción, el sistema no deberá publicar `/docs`, `/redoc` ni `/openapi.json`. Donde el entorno sea de desarrollo, solo deberán ser accesibles con el permiso `sistema:docs`.

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

- **RF-17** Cuando caja registre el pago de una multa, el sistema deberá marcarla como pagada y emitir un comprobante con folio único.
- **RF-18** Cuando un administrador condone una multa, el sistema deberá exigir un motivo y registrar quién la condonó.

### Usuarios y auditoría

- **RF-19** Cuando un administrador cambie el rol o desactive a un usuario, el sistema deberá revocar todos los tokens de refresco de ese usuario.
- **RF-20** El sistema deberá registrar en auditoría toda operación de escritura (quién, qué y cuándo), sin guardar contraseñas ni tokens.

## 7. Requisitos no funcionales y seguridad

- **RNF-1 Exposición.** El backend no es accesible directamente desde internet: escucha en red interna detrás de un proxy inverso, y la base de datos no tiene exposición externa.
- **RNF-2 JWT.** Algoritmo HS256 con un secreto aleatorio de al menos 32 bytes en variable de entorno. Claims: `sub`, `rol`, `iat`, `exp`, `jti`. Acceso de 15 minutos. Refresco de 7 días con rotación en cada uso, guardado como hash en la BD; si se reutiliza uno ya rotado, se revoca toda la sesión.
- **RNF-3 Rate limit.** Login: 5 intentos por minuto por IP y usuario. Resto de la API: 120 solicitudes por minuto por usuario autenticado. Respuesta 429 con `Retry-After`.
- **RNF-4 Contraseñas.** Argon2id con `pwdlib[argon2]` con parámetros iguales o superiores al mínimo de OWASP (19 MiB de memoria, 2 iteraciones, paralelismo 1), ajustados midiendo en el servidor.
- **RNF-5 Datos personales.** Los logs no contienen contraseñas, tokens ni datos personales. El rol `dev` no accede a datos personales.
- **RNF-6 CORS.** Orígenes permitidos explícitos; nunca `*`.
- **RNF-7 Fechas.** Se guardan en UTC y se muestran en `America/El_Salvador`.
- **RNF-8 Calidad.** Python con PEP 8 (Ruff) y JavaScript con ES2026. Cada RF tiene al menos una prueba.
- **RNF-9 Accesibilidad.** WCAG 2.2 AA. En las pantallas de caja: texto de al menos 18 px, botones de al menos 48 px y el flujo de cobro en 3 pantallas o menos (supuesto a validar con los cajeros).

## 8. Interfaz y diseño

Identidad visual y tokens en `DESIGN.md`. Prototipos exportados en `prototipos/`.

Pantallas del alcance v1:

1. Inicio de sesión
2. Búsqueda de catálogo y detalle de libro
3. Mis préstamos, reservas y multas (estudiante y docente)
4. Mostrador del bibliotecario: préstamo y devolución
5. Gestión de catálogo (libros y ejemplares)
6. Caja: cobro de multas
7. Administración de usuarios y roles

Principio de diseño: pocas decisiones por pantalla, botones grandes y mensajes claros en español, pensados para personal de caja de mayor edad.

## 9. Casos límite

- Dos bibliotecarios prestan el mismo ejemplar a la vez: la transacción y una restricción en la BD deben dejar que gane solo uno.
- Devolución de un ejemplar que no está prestado: se rechaza sin cambiar estados.
- Vencimiento que cae en día no hábil: se define en la dudas abiertas D-4.
- El rol de un usuario cambia con un token de acceso todavía vigente: el token solo vive 15 minutos y RF-19 revoca los refrescos.
- La tarifa de multa cambia después de un retraso: la multa conserva la tarifa vigente al momento de la devolución.
- Usuario desactivado con préstamos activos: los préstamos siguen su curso y no puede pedir nuevos.
- El mismo usuario reserva dos veces el mismo libro: se rechaza la segunda.
- ISBN duplicado o con formato inválido: se rechaza con un mensaje que indique cuál es el problema.

## 10. Fuera de alcance (v1)

- Lectura de recursos digitales (PDF o libros electrónicos).
- Pagos en línea.
- Integración con el catálogo, la renovación o la solvencia ya existentes de la universidad.
- Aplicación móvil.
- Notificaciones por correo o mensajería.
- Importación masiva de catálogo.

## 11. Criterios de finalización

- Cada RF tiene al menos una prueba que pasa.
- `uv run ruff check .`, `uv run ruff format --check .` y `uv run pytest` pasan, incluida `test_arquitectura.py`.
- `vp check`, `vp test` y `vp build` pasan.
- En producción, `/docs`, `/redoc` y `/openapi.json` no responden (verificado con una prueba).
- No hay secretos en el repositorio y `.env.example` está al día.
- Esta especificación refleja el comportamiento real.

## 12. Dudas abiertas

- **D-1 Base de datos y ORM.** Propuesta: PostgreSQL, SQLAlchemy 2.x y Alembic. Falta confirmar.
- **D-2 "Sin exposición pública".** Interpretado así: el backend no es accesible directamente y solo recibe tráfico del proxy inverso; el frontend sí es público. Falta aclarar si los usuarios deben llegar al sistema desde fuera del campus (internet o solo red interna o VPN).
- **D-3 Librería de rate limit.** Candidatos: `slowapi` (memoria, un solo proceso) o un limitador con Redis (varios procesos). Verificar mantenimiento antes de elegir.
- **D-4 Calendario.** ¿Los vencimientos se corren si caen en día no hábil o feriado?
- **D-5 Valores de negocio.** Límites, plazos y tarifa de multa (sección 5.1): validar con la biblioteca.
- **D-6 Navegadores soportados.** ES2026 puro puede excluir navegadores antiguos; definir el `build.target` según los dispositivos reales de los usuarios.
- **D-7 Compatibilidad con Python 3.15.** Python 3.15 es muy reciente: confirmar que todas las dependencias con extensiones en C (por ejemplo, las de Pydantic y Argon2) tengan ruedas para 3.15 antes de fijarlo; si no, usar 3.14 y subir después.
- **D-8 Inicio de sesión.** ¿Cuentas propias del sistema o integración con la identidad institucional (correo institucional, SSO)? Dominio del correo por confirmar.
- **D-9 Licencia y propiedad intelectual.** Elegir licencia (ver `LICENSE.md`) y confirmar con la universidad si hay una política de propiedad intelectual sobre proyectos de curso.

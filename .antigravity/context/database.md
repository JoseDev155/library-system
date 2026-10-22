# Base de datos: estructura y SQL

Borrador de la estructura de la base de datos y del SQL para crear las tablas. Parte de `spec/spec.md` (sección 5 "Base de datos y ORM" y sección 8 "Modelo de dominio", que ya incluye los campos que salen de los prototipos de `.antigravity/resources/`). **La spec manda**: si algo difiere, se corrige este archivo.

**Probado:** el SQL de PostgreSQL se ejecutó en PostgreSQL 16 y el de MySQL/MariaDB en MariaDB 10.11, con inserciones que comprueban el formato del carnet, un solo préstamo activo por ejemplar, una sola reserva viva por usuario y libro, y el motivo obligatorio al condonar una multa. **No se probó en MySQL 8.** Una trampa de MariaDB: no admite columnas generadas que devuelvan texto (como el id del ejemplar), por eso la columna generada es numérica.

El SQL es la referencia para diseñar los modelos de `backend/app/repositories/orm_models/` y las migraciones de Alembic. No se ejecuta a mano: las tablas reales las crean las migraciones.

## Motores y reglas de portabilidad

| Motor | Rol | Driver |
|---|---|---|
| PostgreSQL | Principal | `psycopg` (`postgresql+psycopg://`) |
| MySQL | Secundario | `PyMySQL` (`mysql+pymysql://`) |
| MariaDB | Secundario | `PyMySQL` (`mariadb+pymysql://`) |

- Mismo diseño en los tres motores. Solo cambian los tipos de columna (tabla de abajo).
- Estados como `VARCHAR` con `CHECK`, no como `ENUM` nativo: se comporta igual en los tres. `CHECK` se aplica desde MySQL 8.0.16 y MariaDB 10.2.1.
- Dinero con `NUMERIC(10, 2)` (`DECIMAL(10, 2)` en MySQL y MariaDB).
- Fechas en UTC "ingenuo" (sin zona). La aplicación pone todas las fechas, así que no hay `DEFAULT` de fecha en la base. La conversión a `America/El_Salvador` se hace en la capa de servicios (RNF-7).
- MySQL y MariaDB con InnoDB y `utf8mb4`.
- **Sin índices parciales** (MySQL y MariaDB no los soportan). Las reglas "un ejemplar no tiene dos préstamos activos" y "no hay dos reservas activas del mismo libro y usuario" se garantizan con una columna generada numérica (`active_flag`, que vale 1 mientras el registro está vivo y `NULL` después) y un índice único normal que la incluye; los `NULL` no cuentan como duplicados; además, el préstamo toma un bloqueo de fila (`with_for_update()`) sobre el ejemplar (spec, sección 5.3).
- Contraseñas solo como hash Argon2id; los tokens de refresco solo como hash (RNF-2, RF-6).

| Concepto | PostgreSQL | MySQL / MariaDB |
|---|---|---|
| Id de usuario (carnet) | `VARCHAR(20)` | `VARCHAR(20)` |
| Id de las demás tablas (UUID) | `UUID` | `CHAR(36)` |
| Id autoincremental | `BIGINT GENERATED ALWAYS AS IDENTITY` | `BIGINT AUTO_INCREMENT` |
| Fecha y hora | `TIMESTAMP` | `DATETIME(6)` |
| Booleano | `BOOLEAN` | `BOOLEAN` (alias de `TINYINT(1)`) |
| Texto largo | `TEXT` | `TEXT` |

## Diagrama de relaciones

```plaintext
faculties 1───* users
faculties 1───* books
users 1───* refresh_tokens
users 1───* loans *───1 book_copies *───1 books
users 1───* reservations *───1 books
loans 1───0..1 fines *───1 users
fines 1───0..1 payments
users 1───* audit_logs
```

| Tabla | Entidad | Notas |
|---|---|---|
| `faculties` | `Faculty` | Códigos de facultad y unidad (spec, sección 8.3) |
| `users` | `User` | `id` es el carnet `AAAA-II-FFF` (spec, sección 8.2). Roles: `admin`, `dev`, `librarian`, `cashier`, `teacher`, `student` |
| `refresh_tokens` | (seguridad) | Rotación y detección de reutilización (RNF-2, RF-5, RF-19) |
| `books` | `Book` | El ISBN, si existe, es único |
| `book_copies` | `BookCopy` | Estados: `AVAILABLE`, `LOANED`, `RESERVED`, `UNDER_REPAIR`, `WITHDRAWN` |
| `loans` | `Loan` | Estados: `ACTIVE`, `RETURNED`. El retraso se calcula, no se guarda |
| `reservations` | `Reservation` | Estados: `QUEUED`, `HELD`, `FULFILLED`, `CANCELLED`, `EXPIRED` |
| `fines` | `Fine` | Estados: `PENDING`, `PAID`, `WAIVED`. Guarda la tarifa vigente (spec, casos límite) |
| `payments` | `Payment` | Comprobante con número único (RF-17) |
| `audit_logs` | `AuditLog` | Solo se agrega; nunca se edita (RF-20) |

Los parámetros de préstamo (`max_active_loans`, `loan_days`, `max_renewals`, `reservation_hold_hours`, `fine_per_day`) viven en configuración, no en tablas (spec, sección 8.1).

## SQL para PostgreSQL (motor principal)

```sql
CREATE TABLE faculties (
    code VARCHAR(3)   PRIMARY KEY,                           -- 101, 201, 900...
    name VARCHAR(120) NOT NULL UNIQUE
);

INSERT INTO faculties (code, name) VALUES
    ('101', 'Ingeniería y Tecnología'),
    ('102', 'Ciencias Exactas'),
    ('201', 'Ciencias de la Salud'),
    ('301', 'Ciencias Económicas y Administrativas'),
    ('302', 'Ciencias Jurídicas'),
    ('401', 'Ciencias Sociales'),
    ('402', 'Humanidades y Artes'),
    ('403', 'Ciencias de la Educación'),
    ('501', 'Arquitectura y Diseño'),
    ('601', 'Ciencias Agropecuarias y Ambientales'),
    ('900', 'Personal administrativo y de servicios');

CREATE TABLE users (
    id                  VARCHAR(20) PRIMARY KEY,           -- carnet: 2024-PM-101
    institutional_email VARCHAR(255) NOT NULL UNIQUE,
    name                VARCHAR(200) NOT NULL,
    role                VARCHAR(20)  NOT NULL,
    faculty_code        VARCHAR(3)   NOT NULL REFERENCES faculties (code),
    password_hash       VARCHAR(255) NOT NULL,                -- Argon2id (pwdlib)
    active              BOOLEAN      NOT NULL,
    created_at          TIMESTAMP    NOT NULL,
    updated_at          TIMESTAMP    NOT NULL,
    CONSTRAINT ck_users_role CHECK (role IN
        ('admin', 'dev', 'librarian', 'cashier', 'teacher', 'student')),
    CONSTRAINT ck_users_id CHECK (id ~ '^[0-9]{4}-[A-Z]{2}-[0-9]{3}(-[0-9]{2})?$')
);
CREATE INDEX ix_users_faculty ON users (faculty_code);

CREATE TABLE refresh_tokens (
    id          UUID PRIMARY KEY,
    user_id     VARCHAR(20)         NOT NULL REFERENCES users (id),
    session_id  UUID         NOT NULL,                       -- agrupa los tokens de una sesión
    token_hash  VARCHAR(128) NOT NULL UNIQUE,                -- hash, nunca el token
    issued_at   TIMESTAMP    NOT NULL,
    expires_at  TIMESTAMP    NOT NULL,
    rotated_at  TIMESTAMP,                                   -- si se reutiliza, se revoca la sesión
    revoked_at  TIMESTAMP
);
CREATE INDEX ix_refresh_tokens_user ON refresh_tokens (user_id);
CREATE INDEX ix_refresh_tokens_session ON refresh_tokens (session_id);

CREATE TABLE books (
    id          UUID PRIMARY KEY,
    isbn        VARCHAR(17)  UNIQUE,                         -- opcional; varios NULL permitidos
    title       VARCHAR(300) NOT NULL,
    authors     VARCHAR(500) NOT NULL,
    category    VARCHAR(120),                                -- materia o tema
    faculty_code VARCHAR(3)  REFERENCES faculties (code),    -- área del libro
    publisher   VARCHAR(200),
    edition     VARCHAR(40),                                 -- p. ej. 8ª Edición
    year        SMALLINT,
    call_number VARCHAR(60),                                 -- signatura, p. ej. MAT-510.4-STE
    created_at  TIMESTAMP    NOT NULL,
    updated_at  TIMESTAMP    NOT NULL
);
CREATE INDEX ix_books_title ON books (title);
CREATE INDEX ix_books_category ON books (category);
CREATE INDEX ix_books_faculty ON books (faculty_code);
CREATE INDEX ix_books_call_number ON books (call_number);

CREATE TABLE book_copies (
    id             UUID PRIMARY KEY,
    book_id        UUID        NOT NULL REFERENCES books (id),
    inventory_code VARCHAR(40) NOT NULL UNIQUE,              -- p. ej. BC-09241
    status         VARCHAR(20) NOT NULL,
    circulation    VARCHAR(20) NOT NULL,                     -- LOANABLE o REFERENCE_ONLY
    location_floor VARCHAR(20),                              -- p. ej. Piso 2
    location_shelf VARCHAR(40),                              -- p. ej. Estantería 4B
    created_at     TIMESTAMP   NOT NULL,
    updated_at     TIMESTAMP   NOT NULL,
    CONSTRAINT ck_book_copies_status CHECK (status IN
        ('AVAILABLE', 'LOANED', 'RESERVED', 'UNDER_REPAIR', 'WITHDRAWN')),
    CONSTRAINT ck_book_copies_circulation CHECK (circulation IN ('LOANABLE', 'REFERENCE_ONLY'))
);
CREATE INDEX ix_book_copies_book_status ON book_copies (book_id, status);

CREATE TABLE loans (
    id          UUID PRIMARY KEY,
    copy_id     UUID        NOT NULL REFERENCES book_copies (id),
    user_id     VARCHAR(20)        NOT NULL REFERENCES users (id),
    loaned_by   VARCHAR(20)        NOT NULL REFERENCES users (id),  -- bibliotecario que lo registró
    loaned_at   TIMESTAMP   NOT NULL,
    due_at      TIMESTAMP   NOT NULL,
    returned_at TIMESTAMP,
    renewals    SMALLINT    NOT NULL,
    status      VARCHAR(20) NOT NULL,
    -- Un ejemplar no puede tener dos préstamos activos (sin índice parcial):
    active_flag SMALLINT GENERATED ALWAYS AS
        (CASE WHEN status = 'ACTIVE' THEN 1 END) STORED,
    CONSTRAINT uq_loans_active_copy UNIQUE (copy_id, active_flag),
    CONSTRAINT ck_loans_status CHECK (status IN ('ACTIVE', 'RETURNED')),
    CONSTRAINT ck_loans_renewals CHECK (renewals >= 0)
);
CREATE INDEX ix_loans_user_status ON loans (user_id, status);
CREATE INDEX ix_loans_due_at ON loans (due_at);

CREATE TABLE reservations (
    id         UUID PRIMARY KEY,
    book_id    UUID        NOT NULL REFERENCES books (id),
    user_id    VARCHAR(20)        NOT NULL REFERENCES users (id),
    copy_id    UUID        REFERENCES book_copies (id),      -- ejemplar apartado, si ya hay
    created_at TIMESTAMP   NOT NULL,                         -- define el orden de la cola
    held_until TIMESTAMP,
    status     VARCHAR(20) NOT NULL,
    -- Un usuario no reserva dos veces el mismo libro mientras la reserva siga viva:
    active_flag SMALLINT GENERATED ALWAYS AS
        (CASE WHEN status IN ('QUEUED', 'HELD') THEN 1 END) STORED,
    CONSTRAINT uq_reservations_active UNIQUE (user_id, book_id, active_flag),
    CONSTRAINT ck_reservations_status CHECK (status IN
        ('QUEUED', 'HELD', 'FULFILLED', 'CANCELLED', 'EXPIRED'))
);
CREATE INDEX ix_reservations_queue ON reservations (book_id, status, created_at);

CREATE TABLE fines (
    id            UUID PRIMARY KEY,
    loan_id       UUID          NOT NULL REFERENCES loans (id),
    user_id       VARCHAR(20)          NOT NULL REFERENCES users (id),
    days_late     INTEGER       NOT NULL,
    rate_per_day  NUMERIC(10, 2) NOT NULL,                   -- tarifa vigente al devolver
    amount        NUMERIC(10, 2) NOT NULL,
    status        VARCHAR(20)   NOT NULL,
    waiver_reason TEXT,
    waived_by     VARCHAR(20)          REFERENCES users (id),
    created_at    TIMESTAMP     NOT NULL,
    CONSTRAINT uq_fines_loan UNIQUE (loan_id),               -- una multa por préstamo
    CONSTRAINT ck_fines_status CHECK (status IN ('PENDING', 'PAID', 'WAIVED')),
    CONSTRAINT ck_fines_days CHECK (days_late > 0),
    CONSTRAINT ck_fines_amount CHECK (amount >= 0),
    -- RF-18: condonar exige motivo y quién lo hizo
    CONSTRAINT ck_fines_waiver CHECK
        (status <> 'WAIVED' OR (waiver_reason IS NOT NULL AND waived_by IS NOT NULL))
);
CREATE INDEX ix_fines_user_status ON fines (user_id, status);

CREATE TABLE payments (
    id             UUID PRIMARY KEY,
    fine_id        UUID           NOT NULL UNIQUE REFERENCES fines (id),
    cashier_id     VARCHAR(20)           NOT NULL REFERENCES users (id),
    amount         NUMERIC(10, 2) NOT NULL,
    method         VARCHAR(20)    NOT NULL,                  -- efectivo, tarjeta (POS) o transferencia
    receipt_number VARCHAR(30)    NOT NULL UNIQUE,
    paid_at        TIMESTAMP      NOT NULL,
    CONSTRAINT ck_payments_method CHECK (method IN ('CASH', 'CARD', 'TRANSFER')),
    CONSTRAINT ck_payments_amount CHECK (amount > 0)
);

CREATE TABLE audit_logs (
    id         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id    VARCHAR(20)         REFERENCES users (id),           -- NULL en eventos sin sesión
    action     VARCHAR(60)  NOT NULL,
    entity     VARCHAR(60)  NOT NULL,
    entity_id  VARCHAR(64)  NOT NULL,
    created_at TIMESTAMP    NOT NULL                         -- sin contraseñas ni tokens (RF-20)
);
CREATE INDEX ix_audit_logs_entity ON audit_logs (entity, entity_id);
CREATE INDEX ix_audit_logs_user_date ON audit_logs (user_id, created_at);
```

## SQL para MySQL y MariaDB

Mismo diseño. Cambian los tipos de id y de fecha, y cada tabla lleva `ENGINE=InnoDB` y `utf8mb4`.

```sql
CREATE TABLE faculties (
    code VARCHAR(3)   PRIMARY KEY,                           -- 101, 201, 900...
    name VARCHAR(120) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO faculties (code, name) VALUES
    ('101', 'Ingeniería y Tecnología'),
    ('102', 'Ciencias Exactas'),
    ('201', 'Ciencias de la Salud'),
    ('301', 'Ciencias Económicas y Administrativas'),
    ('302', 'Ciencias Jurídicas'),
    ('401', 'Ciencias Sociales'),
    ('402', 'Humanidades y Artes'),
    ('403', 'Ciencias de la Educación'),
    ('501', 'Arquitectura y Diseño'),
    ('601', 'Ciencias Agropecuarias y Ambientales'),
    ('900', 'Personal administrativo y de servicios');

CREATE TABLE users (
    id                  VARCHAR(20) PRIMARY KEY,
    institutional_email VARCHAR(255) NOT NULL UNIQUE,
    name                VARCHAR(200) NOT NULL,
    role                VARCHAR(20)  NOT NULL,
    faculty_code        VARCHAR(3)   NOT NULL,
    password_hash       VARCHAR(255) NOT NULL,
    active              BOOLEAN      NOT NULL,
    created_at          DATETIME(6)  NOT NULL,
    updated_at          DATETIME(6)  NOT NULL,
    CONSTRAINT fk_users_faculty FOREIGN KEY (faculty_code) REFERENCES faculties (code),
    CONSTRAINT ck_users_role CHECK (role IN
        ('admin', 'dev', 'librarian', 'cashier', 'teacher', 'student')),
    CONSTRAINT ck_users_id CHECK (id REGEXP '^[0-9]{4}-[A-Z]{2}-[0-9]{3}(-[0-9]{2})?$'),
    INDEX ix_users_faculty (faculty_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE refresh_tokens (
    id          CHAR(36) PRIMARY KEY,
    user_id     VARCHAR(20)     NOT NULL,
    session_id  CHAR(36)     NOT NULL,
    token_hash  VARCHAR(128) NOT NULL UNIQUE,
    issued_at   DATETIME(6)  NOT NULL,
    expires_at  DATETIME(6)  NOT NULL,
    rotated_at  DATETIME(6),
    revoked_at  DATETIME(6),
    CONSTRAINT fk_refresh_tokens_user FOREIGN KEY (user_id) REFERENCES users (id),
    INDEX ix_refresh_tokens_user (user_id),
    INDEX ix_refresh_tokens_session (session_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE books (
    id          CHAR(36) PRIMARY KEY,
    isbn        VARCHAR(17)  UNIQUE,
    title       VARCHAR(300) NOT NULL,
    authors     VARCHAR(500) NOT NULL,
    category    VARCHAR(120),
    faculty_code VARCHAR(3),
    publisher   VARCHAR(200),
    edition     VARCHAR(40),
    year        SMALLINT,
    call_number VARCHAR(60),
    created_at  DATETIME(6)  NOT NULL,
    updated_at  DATETIME(6)  NOT NULL,
    CONSTRAINT fk_books_faculty FOREIGN KEY (faculty_code) REFERENCES faculties (code),
    INDEX ix_books_faculty (faculty_code),
    INDEX ix_books_title (title),
    INDEX ix_books_category (category),
    INDEX ix_books_call_number (call_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE book_copies (
    id             CHAR(36) PRIMARY KEY,
    book_id        CHAR(36)    NOT NULL,
    inventory_code VARCHAR(40) NOT NULL UNIQUE,
    status         VARCHAR(20) NOT NULL,
    circulation    VARCHAR(20) NOT NULL,
    location_floor VARCHAR(20),
    location_shelf VARCHAR(40),
    created_at     DATETIME(6) NOT NULL,
    updated_at     DATETIME(6) NOT NULL,
    CONSTRAINT fk_book_copies_book FOREIGN KEY (book_id) REFERENCES books (id),
    CONSTRAINT ck_book_copies_status CHECK (status IN
        ('AVAILABLE', 'LOANED', 'RESERVED', 'UNDER_REPAIR', 'WITHDRAWN')),
    CONSTRAINT ck_book_copies_circulation CHECK (circulation IN ('LOANABLE', 'REFERENCE_ONLY')),
    INDEX ix_book_copies_book_status (book_id, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE loans (
    id          CHAR(36) PRIMARY KEY,
    copy_id     CHAR(36)    NOT NULL,
    user_id     VARCHAR(20)    NOT NULL,
    loaned_by   VARCHAR(20)    NOT NULL,
    loaned_at   DATETIME(6) NOT NULL,
    due_at      DATETIME(6) NOT NULL,
    returned_at DATETIME(6),
    renewals    SMALLINT    NOT NULL,
    status      VARCHAR(20) NOT NULL,
    active_flag SMALLINT GENERATED ALWAYS AS
        (CASE WHEN status = 'ACTIVE' THEN 1 END) STORED,
    CONSTRAINT uq_loans_active_copy UNIQUE (copy_id, active_flag),
    CONSTRAINT fk_loans_copy FOREIGN KEY (copy_id) REFERENCES book_copies (id),
    CONSTRAINT fk_loans_user FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT fk_loans_loaned_by FOREIGN KEY (loaned_by) REFERENCES users (id),
    CONSTRAINT ck_loans_status CHECK (status IN ('ACTIVE', 'RETURNED')),
    CONSTRAINT ck_loans_renewals CHECK (renewals >= 0),
    INDEX ix_loans_user_status (user_id, status),
    INDEX ix_loans_due_at (due_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE reservations (
    id         CHAR(36) PRIMARY KEY,
    book_id    CHAR(36)    NOT NULL,
    user_id    VARCHAR(20)    NOT NULL,
    copy_id    CHAR(36),
    created_at DATETIME(6) NOT NULL,
    held_until DATETIME(6),
    status     VARCHAR(20) NOT NULL,
    active_flag SMALLINT GENERATED ALWAYS AS
        (CASE WHEN status IN ('QUEUED', 'HELD') THEN 1 END) STORED,
    CONSTRAINT uq_reservations_active UNIQUE (user_id, book_id, active_flag),
    CONSTRAINT fk_reservations_book FOREIGN KEY (book_id) REFERENCES books (id),
    CONSTRAINT fk_reservations_user FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT fk_reservations_copy FOREIGN KEY (copy_id) REFERENCES book_copies (id),
    CONSTRAINT ck_reservations_status CHECK (status IN
        ('QUEUED', 'HELD', 'FULFILLED', 'CANCELLED', 'EXPIRED')),
    INDEX ix_reservations_queue (book_id, status, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE fines (
    id            CHAR(36) PRIMARY KEY,
    loan_id       CHAR(36)       NOT NULL,
    user_id       VARCHAR(20)       NOT NULL,
    days_late     INT            NOT NULL,
    rate_per_day  DECIMAL(10, 2) NOT NULL,
    amount        DECIMAL(10, 2) NOT NULL,
    status        VARCHAR(20)    NOT NULL,
    waiver_reason TEXT,
    waived_by     VARCHAR(20),
    created_at    DATETIME(6)    NOT NULL,
    CONSTRAINT uq_fines_loan UNIQUE (loan_id),
    CONSTRAINT fk_fines_loan FOREIGN KEY (loan_id) REFERENCES loans (id),
    CONSTRAINT fk_fines_user FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT fk_fines_waived_by FOREIGN KEY (waived_by) REFERENCES users (id),
    CONSTRAINT ck_fines_status CHECK (status IN ('PENDING', 'PAID', 'WAIVED')),
    CONSTRAINT ck_fines_days CHECK (days_late > 0),
    CONSTRAINT ck_fines_amount CHECK (amount >= 0),
    CONSTRAINT ck_fines_waiver CHECK
        (status <> 'WAIVED' OR (waiver_reason IS NOT NULL AND waived_by IS NOT NULL)),
    INDEX ix_fines_user_status (user_id, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE payments (
    id             CHAR(36) PRIMARY KEY,
    fine_id        CHAR(36)       NOT NULL UNIQUE,
    cashier_id     VARCHAR(20)       NOT NULL,
    amount         DECIMAL(10, 2) NOT NULL,
    method         VARCHAR(20)    NOT NULL,
    receipt_number VARCHAR(30)    NOT NULL UNIQUE,
    paid_at        DATETIME(6)    NOT NULL,
    CONSTRAINT fk_payments_fine FOREIGN KEY (fine_id) REFERENCES fines (id),
    CONSTRAINT fk_payments_cashier FOREIGN KEY (cashier_id) REFERENCES users (id),
    CONSTRAINT ck_payments_method CHECK (method IN ('CASH', 'CARD', 'TRANSFER')),
    CONSTRAINT ck_payments_amount CHECK (amount > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE audit_logs (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id    VARCHAR(20),
    action     VARCHAR(60) NOT NULL,
    entity     VARCHAR(60) NOT NULL,
    entity_id  VARCHAR(64) NOT NULL,
    created_at DATETIME(6) NOT NULL,
    CONSTRAINT fk_audit_logs_user FOREIGN KEY (user_id) REFERENCES users (id),
    INDEX ix_audit_logs_entity (entity, entity_id),
    INDEX ix_audit_logs_user_date (user_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## Identificador de usuario

`users.id` es el carnet universitario `AAAA-II-FFF` (año de ingreso, iniciales de los apellidos y código de facultad), por ejemplo `2024-PM-101`. Si se repite la combinación, la regla propuesta añade un correlativo (`2024-PM-101-02`); ver spec, secciones 8.2 y D-13. Una restricción `CHECK` valida el formato y todas las claves foráneas a usuarios usan `VARCHAR(20)`. `faculties` guarda los códigos de la spec, sección 8.3.

## Qué viene de los prototipos

Los campos que salen de los prototipos ya están en la spec, sección 8 (y la 12.1 explica qué se descarta): carnet y facultad en `users`; edición, signatura y área en `books`; tipo de circulación y ubicación física en `book_copies`; `rate_per_day` en `fines`; `loaned_by` en `loans`; `method` en `payments`.

## Decisiones pendientes

- **Varias multas en un solo cobro** (D-14). Con la spec actual, `payments.fine_id` es único y cada pago tiene su comprobante, así que un cobro múltiple crea un pago por multa. Si se quiere un solo comprobante, hace falta una tabla `receipts` y que `payments` apunte a ella.
- **Colisiones del carnet** (D-13). Confirmar la regla del correlativo.
- **Límite de préstamos.** El mostrador muestra un máximo de 5 libros para un estudiante y la spec dice 3 (D-5).
- **Tarifa por "día hábil".** Los prototipos hablan de días hábiles; la spec no define calendario (D-4). `fines.days_late` guarda el número ya calculado.
- **Estadísticas de los prototipos** (totales de usuarios, ejemplares por estado) se calculan con consultas, no con columnas.
- **Borrado:** todas las claves foráneas son `RESTRICT` (sin `ON DELETE`). Los usuarios y libros se desactivan (`active`, `WITHDRAWN`), no se borran, para conservar la auditoría.

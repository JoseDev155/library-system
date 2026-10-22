# Base de datos: estructura y SQL

Borrador de la estructura de la base de datos y del SQL para crear las tablas. Parte de `spec/spec.md` (sección 5 "Base de datos y ORM" y sección 8 "Modelo de dominio") y de los campos que muestran los prototipos de `.antigravity/resources/`. **La spec manda**: los campos marcados con (P) salen de los prototipos y no están todavía en la spec (ver "Campos nuevos").

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
- **Sin índices parciales** (MySQL y MariaDB no los soportan). Las reglas "un ejemplar no tiene dos préstamos activos" y "no hay dos reservas activas del mismo libro y usuario" se garantizan con una columna generada y un índice único normal; además, el préstamo toma un bloqueo de fila (`with_for_update()`) sobre el ejemplar (spec, sección 5.3).
- Contraseñas solo como hash Argon2id; los tokens de refresco solo como hash (RNF-2, RF-6).

| Concepto | PostgreSQL | MySQL / MariaDB |
|---|---|---|
| Id (UUID) | `UUID` | `CHAR(36)` |
| Id autoincremental | `BIGINT GENERATED ALWAYS AS IDENTITY` | `BIGINT AUTO_INCREMENT` |
| Fecha y hora | `TIMESTAMP` | `DATETIME(6)` |
| Booleano | `BOOLEAN` | `BOOLEAN` (alias de `TINYINT(1)`) |
| Texto largo | `TEXT` | `TEXT` |

## Diagrama de relaciones

```plaintext
users 1───* refresh_tokens
users 1───* loans *───1 book_copies *───1 books
users 1───* reservations *───1 books
loans 1───0..1 fines *───1 users
fines 1───0..1 payments
users 1───* audit_logs
```

| Tabla | Entidad | Notas |
|---|---|---|
| `users` | `User` | Roles: `admin`, `dev`, `librarian`, `cashier`, `teacher`, `student` |
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
CREATE TABLE users (
    id                  UUID PRIMARY KEY,
    institutional_email VARCHAR(255) NOT NULL UNIQUE,
    student_code        VARCHAR(20)  UNIQUE,                 -- (P) carnet, p. ej. U-20210894
    name                VARCHAR(200) NOT NULL,
    role                VARCHAR(20)  NOT NULL,
    faculty             VARCHAR(120),                         -- (P) facultad o unidad
    password_hash       VARCHAR(255) NOT NULL,                -- Argon2id (pwdlib)
    active              BOOLEAN      NOT NULL,
    created_at          TIMESTAMP    NOT NULL,
    updated_at          TIMESTAMP    NOT NULL,
    CONSTRAINT ck_users_role CHECK (role IN
        ('admin', 'dev', 'librarian', 'cashier', 'teacher', 'student'))
);

CREATE TABLE refresh_tokens (
    id          UUID PRIMARY KEY,
    user_id     UUID         NOT NULL REFERENCES users (id),
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
    category    VARCHAR(120),
    publisher   VARCHAR(200),
    edition     VARCHAR(40),                                 -- (P) p. ej. 8ª Edición
    year        SMALLINT,
    call_number VARCHAR(60),                                 -- (P) signatura, p. ej. 515.15 S849c
    created_at  TIMESTAMP    NOT NULL,
    updated_at  TIMESTAMP    NOT NULL
);
CREATE INDEX ix_books_title ON books (title);
CREATE INDEX ix_books_category ON books (category);
CREATE INDEX ix_books_call_number ON books (call_number);

CREATE TABLE book_copies (
    id             UUID PRIMARY KEY,
    book_id        UUID        NOT NULL REFERENCES books (id),
    inventory_code VARCHAR(40) NOT NULL UNIQUE,              -- p. ej. BC-09241
    status         VARCHAR(20) NOT NULL,
    location_floor VARCHAR(20),                              -- (P) p. ej. Piso 2
    location_shelf VARCHAR(40),                              -- (P) p. ej. Estantería 4B
    created_at     TIMESTAMP   NOT NULL,
    updated_at     TIMESTAMP   NOT NULL,
    CONSTRAINT ck_book_copies_status CHECK (status IN
        ('AVAILABLE', 'LOANED', 'RESERVED', 'UNDER_REPAIR', 'WITHDRAWN'))
);
CREATE INDEX ix_book_copies_book_status ON book_copies (book_id, status);

CREATE TABLE loans (
    id          UUID PRIMARY KEY,
    copy_id     UUID        NOT NULL REFERENCES book_copies (id),
    user_id     UUID        NOT NULL REFERENCES users (id),
    loaned_by   UUID        NOT NULL REFERENCES users (id),  -- bibliotecario que lo registró
    loaned_at   TIMESTAMP   NOT NULL,
    due_at      TIMESTAMP   NOT NULL,
    returned_at TIMESTAMP,
    renewals    SMALLINT    NOT NULL,
    status      VARCHAR(20) NOT NULL,
    -- Un ejemplar no puede tener dos préstamos activos (sin índice parcial):
    active_copy_id UUID GENERATED ALWAYS AS
        (CASE WHEN status = 'ACTIVE' THEN copy_id END) STORED,
    CONSTRAINT uq_loans_active_copy UNIQUE (active_copy_id),
    CONSTRAINT ck_loans_status CHECK (status IN ('ACTIVE', 'RETURNED')),
    CONSTRAINT ck_loans_renewals CHECK (renewals >= 0)
);
CREATE INDEX ix_loans_user_status ON loans (user_id, status);
CREATE INDEX ix_loans_due_at ON loans (due_at);

CREATE TABLE reservations (
    id         UUID PRIMARY KEY,
    book_id    UUID        NOT NULL REFERENCES books (id),
    user_id    UUID        NOT NULL REFERENCES users (id),
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
    user_id       UUID          NOT NULL REFERENCES users (id),
    days_late     INTEGER       NOT NULL,
    rate_per_day  NUMERIC(10, 2) NOT NULL,                   -- tarifa vigente al devolver
    amount        NUMERIC(10, 2) NOT NULL,
    status        VARCHAR(20)   NOT NULL,
    waiver_reason TEXT,
    waived_by     UUID          REFERENCES users (id),
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
    cashier_id     UUID           NOT NULL REFERENCES users (id),
    amount         NUMERIC(10, 2) NOT NULL,
    method         VARCHAR(20)    NOT NULL,                  -- (P) efectivo, tarjeta, transferencia
    receipt_number VARCHAR(30)    NOT NULL UNIQUE,
    paid_at        TIMESTAMP      NOT NULL,
    CONSTRAINT ck_payments_method CHECK (method IN ('CASH', 'CARD', 'TRANSFER')),
    CONSTRAINT ck_payments_amount CHECK (amount > 0)
);

CREATE TABLE audit_logs (
    id         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id    UUID         REFERENCES users (id),           -- NULL en eventos sin sesión
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
CREATE TABLE users (
    id                  CHAR(36) PRIMARY KEY,
    institutional_email VARCHAR(255) NOT NULL UNIQUE,
    student_code        VARCHAR(20)  UNIQUE,
    name                VARCHAR(200) NOT NULL,
    role                VARCHAR(20)  NOT NULL,
    faculty             VARCHAR(120),
    password_hash       VARCHAR(255) NOT NULL,
    active              BOOLEAN      NOT NULL,
    created_at          DATETIME(6)  NOT NULL,
    updated_at          DATETIME(6)  NOT NULL,
    CONSTRAINT ck_users_role CHECK (role IN
        ('admin', 'dev', 'librarian', 'cashier', 'teacher', 'student'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE refresh_tokens (
    id          CHAR(36) PRIMARY KEY,
    user_id     CHAR(36)     NOT NULL,
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
    publisher   VARCHAR(200),
    edition     VARCHAR(40),
    year        SMALLINT,
    call_number VARCHAR(60),
    created_at  DATETIME(6)  NOT NULL,
    updated_at  DATETIME(6)  NOT NULL,
    INDEX ix_books_title (title),
    INDEX ix_books_category (category),
    INDEX ix_books_call_number (call_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE book_copies (
    id             CHAR(36) PRIMARY KEY,
    book_id        CHAR(36)    NOT NULL,
    inventory_code VARCHAR(40) NOT NULL UNIQUE,
    status         VARCHAR(20) NOT NULL,
    location_floor VARCHAR(20),
    location_shelf VARCHAR(40),
    created_at     DATETIME(6) NOT NULL,
    updated_at     DATETIME(6) NOT NULL,
    CONSTRAINT fk_book_copies_book FOREIGN KEY (book_id) REFERENCES books (id),
    CONSTRAINT ck_book_copies_status CHECK (status IN
        ('AVAILABLE', 'LOANED', 'RESERVED', 'UNDER_REPAIR', 'WITHDRAWN')),
    INDEX ix_book_copies_book_status (book_id, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE loans (
    id          CHAR(36) PRIMARY KEY,
    copy_id     CHAR(36)    NOT NULL,
    user_id     CHAR(36)    NOT NULL,
    loaned_by   CHAR(36)    NOT NULL,
    loaned_at   DATETIME(6) NOT NULL,
    due_at      DATETIME(6) NOT NULL,
    returned_at DATETIME(6),
    renewals    SMALLINT    NOT NULL,
    status      VARCHAR(20) NOT NULL,
    active_copy_id CHAR(36) GENERATED ALWAYS AS
        (CASE WHEN status = 'ACTIVE' THEN copy_id END) STORED,
    CONSTRAINT uq_loans_active_copy UNIQUE (active_copy_id),
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
    user_id    CHAR(36)    NOT NULL,
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
    user_id       CHAR(36)       NOT NULL,
    days_late     INT            NOT NULL,
    rate_per_day  DECIMAL(10, 2) NOT NULL,
    amount        DECIMAL(10, 2) NOT NULL,
    status        VARCHAR(20)    NOT NULL,
    waiver_reason TEXT,
    waived_by     CHAR(36),
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
    cashier_id     CHAR(36)       NOT NULL,
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
    user_id    CHAR(36),
    action     VARCHAR(60) NOT NULL,
    entity     VARCHAR(60) NOT NULL,
    entity_id  VARCHAR(64) NOT NULL,
    created_at DATETIME(6) NOT NULL,
    CONSTRAINT fk_audit_logs_user FOREIGN KEY (user_id) REFERENCES users (id),
    INDEX ix_audit_logs_entity (entity, entity_id),
    INDEX ix_audit_logs_user_date (user_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## Campos nuevos (P) respecto a la spec

Salen de los prototipos y hay que decidir si entran. Si entran, se añaden primero a `spec/spec.md` (sección 8) y luego al código.

| Campo | Tabla | Prototipo |
|---|---|---|
| `student_code` (carnet) | `users` | Todas las pantallas muestran el carnet (`U-20210894`) y permiten buscar por él |
| `faculty` | `users` | Administración de usuarios y mostrador |
| `edition`, `call_number` | `books` | Catálogo y gestión de catálogo |
| `location_floor`, `location_shelf` | `book_copies` | Gestión de catálogo y mostrador |
| `method` (`CASH`, `CARD`, `TRANSFER`) | `payments` | Caja: forma de liquidación |
| `rate_per_day` | `fines` | La spec pide conservar la tarifa vigente al devolver |
| `loaned_by` | `loans` | Auditar qué bibliotecario registró el préstamo |

## Decisiones pendientes

- **Varias multas en un solo cobro.** La pantalla de caja deja marcar varias multas para pagarlas juntas. Con la spec actual, `payments.fine_id` es único y cada pago tiene su comprobante, así que un cobro múltiple crea un pago por multa. Si se quiere un solo comprobante para varias multas, hace falta una tabla de recibos (`receipts`) y que `payments` apunte a ella.
- **Límite de préstamos.** El mostrador muestra un máximo de 5 libros para un estudiante, mientras que la spec dice 3 (`max_active_loans`). Es el D-5 de las dudas abiertas.
- **Tarifa por "día hábil".** Los prototipos hablan de días hábiles; la spec no define calendario (D-4). `fines.days_late` guarda el número ya calculado.
- **Campos sin base en la spec:** estadísticas y reportes de los prototipos (totales de usuarios, ejemplares por estado) se calculan con consultas, no con columnas.
- **Borrado:** todas las claves foráneas son `RESTRICT` (sin `ON DELETE`). Los usuarios y libros se desactivan (`active`, `WITHDRAWN`), no se borran, para conservar la auditoría.

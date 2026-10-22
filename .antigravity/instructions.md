# Antigravity IDE Instructions

These instructions are specific to the Antigravity IDE for this project. They do not contain system behavior rules nor AI agent instructions (those live in `AGENTS.md`, `CLAUDE.md`, `spec.md` and `.agents/`).

## 1. Initialize the project

From the IDE integrated terminal, run:

```bash
# Backend (from backend/)
cd backend
uv python pin 3.15
uv sync

# Frontend (from frontend/)
cd ../frontend
vp install
```

Or use the initialization script:

```bash
.antigravity/scripts/inicializar-proyecto.sh
```

## 2. Open frontend prototypes

Exported prototypes are located in:

```
.antigravity/prototipos/
  login.jsx
  catalogo.jsx
  prestamos.jsx
  multas.jsx
  README.md
```

Open them as `.jsx` files to consult the visual reference of the screens. Design tokens are in `DESIGN.md`.

## 3. Run common commands from the IDE

| Action | Command | Folder |
|---|---|---|
| Install backend dependencies | `uv sync` | `backend/` |
| Run backend tests | `uv run pytest` | `backend/` |
| Backend lint | `uv run ruff check .` | `backend/` |
| Backend format | `uv run ruff format .` | `backend/` |
| Install frontend dependencies | `vp install` | `frontend/` |
| Frontend dev server | `vp dev` | `frontend/` |
| Frontend tests | `vp test` | `frontend/` |
| Frontend production build | `vp build` | `frontend/` |
| Create DB migration | `alembic revision --autogenerate -m "msg"` | `backend/` |
| Apply DB migrations | `alembic upgrade head` | `backend/` |

## 4. Recommended workspace configuration

- Configure Python formatter as Ruff.
- Configure JavaScript/JSX formatter according to ES2026 and ES modules.
- Set encoding to UTF-8 for all files.
- Error messages, comments, and UI labels are in Spanish.

## 5. IDE configuration files

| File | Purpose |
|---|---|
| `.antigravity/ide-config.json` | General IDE configuration for this project |
| `.antigravity/prototipos/` | Frontend prototypes (visual reference) |
| `.antigravity/scripts/` | Utility scripts (e.g., `inicializar-proyecto.sh`) |

## 6. What to consult in other files

- Work rules, stack, commands, and security: `AGENTS.md`
- Claude Code specific notes: `CLAUDE.md`
- System behavior specification (RF, RNF, architecture): `spec.md`
- Visual identity and design tokens: `DESIGN.md`
- AI agent instructions: `.agents/*/instrucciones.md`

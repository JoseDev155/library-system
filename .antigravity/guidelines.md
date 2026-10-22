# Antigravity IDE Guidelines

These guidelines apply exclusively to using the Antigravity IDE with this project. They do not duplicate or replace the AI agent rules (in `.agents/`) or the system specification (`spec.md`).

## Opening the project

- Open the `library-system` root folder as a workspace in Antigravity IDE.
- Frontend prototypes live in `.antigravity/prototipos/` and open as `.jsx` files.
- Backend configuration is in `backend/` and is managed with `uv`; do not edit `uv.lock` manually.
- Frontend configuration is in `frontend/` and is managed with `vp` (Bun); do not use Node.js as a tool runtime.

## Editing frontend prototypes

- Prototypes are design exports (Claude Design / Stitch) and serve as visual reference.
- Color and typography tokens come from `DESIGN.md`; do not introduce loose colors or typography not defined there.
- Components are React function components with `.jsx` files and ES modules (ES2026).
- Prototype messages and labels are in Spanish.

## Integration with project tools

| Tool | Purpose | How to invoke from the IDE |
|---|---|---|
| `uv` | Python package manager (backend) | Integrated terminal: `uv sync`, `uv run pytest`, etc. |
| `vp` | Bun package manager (frontend) | Integrated terminal: `vp install`, `vp dev`, `vp test`, `vp build` |
| `pytest` | Backend unit tests | `uv run pytest` from `backend/` |
| `ruff` | Python lint and format | `uv run ruff check .` and `uv run ruff format .` from `backend/` |

## Navigating agent folders

The `.agents/` folder contains configuration and scripts for each AI agent. From the IDE you can consult:

- `.agents/backend-agente/instrucciones.md` — backend 7-layer rules
- `.agents/frontend-agente/instrucciones.md` — React frontend rules
- `.agents/bd-agente/instrucciones.md` — database and ORM rules
- `.agents/pruebas-agente/instrucciones.md` — test and coverage rules
- `.agents/documentacion-agente/instrucciones.md` — documentation rules

These files are reference for AI agents; the IDE displays them as plain text files. Do not modify their content from the IDE unless you are updating project documentation.

## What NOT to do from the IDE

- Do not edit `.env` (secrets go only in environment variables).
- Do not manually edit `uv.lock` or the Bun lockfile.
- Do not touch `libs/biblioteca_entidades/` without updating `spec.md` first.
- Do not edit license files (`LICENSE.md`, `NOTICE.md`).
- Do not introduce business rules, POO, 7 layers, or security here; those rules live in `AGENTS.md` and `spec.md`.

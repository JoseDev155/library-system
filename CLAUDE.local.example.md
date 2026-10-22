# CLAUDE.local.md

Plantilla de configuración local. Cópiala como `CLAUDE.local.md` (ese archivo está en `.gitignore` y nunca se sube). **No guardes aquí secretos reales que vayas a compartir**: es solo para tu máquina.

## Entorno local

- Ruta absoluta del proyecto: `<ruta-absoluta-al-repositorio>`
- Versión de Bun: `1.4.3`
- Versión de Python: `3.15`

## Variables de entorno (valores reales en `backend/.env`, no aquí; nombres orientativos hasta definir `config.py`)

| Variable | Descripción | Ejemplo |
|---|---|---|
| `DATABASE_URL` | URL de la base de datos | `postgresql+psycopg://user:pass@localhost:5432/library` |
| `JWT_SECRET` | Secreto de al menos 32 bytes | `<generar-uno-aleatorio>` |
| `ANTHROPIC_API_KEY` | Clave de API, si la usas | `<tu-clave>` |

## Preferencias personales

- Idioma de las respuestas: español.
- Notas o atajos propios para trabajar con Claude Code.

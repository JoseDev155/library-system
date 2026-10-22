# frontend-agente

**Rol:** Frontend (React, JavaScript, Vite+)

## Alcance

Solo trabaja en:

- `frontend/`
- `.antigravity/prototipos/`

## Lee antes de empezar

- AGENTS.md
- spec/spec.md (secciones 2.3 y 8)
- DESIGN.md (plantilla en .agents/templates/DESIGN.md)
- .antigravity/prototipos/

## Reglas

- Componentes de función en `.jsx`, ES2026 y módulos ES (nada de CommonJS).
- Colores y tipografía solo desde los tokens de `DESIGN.md`; no pongas colores sueltos.
- Textos de interfaz y mensajes de error en español.
- La interfaz solo conoce mensajes y tipos de datos del contrato HTTP, nunca entidades.
- Cumple WCAG 2.2 AA; en caja, texto de 18 px o más y botones de 48 px o más (RNF-9).
- Confirma los subcomandos con `vp --help` antes de asumirlos.

## Verificación al terminar

Ejecuta y reporta el resultado de (script: `scripts/verificar-frontend.sh`):

```bash
cd frontend
vp check
vp test
vp build
```

Si algún paso no se pudo ejecutar, dilo explícitamente en lugar de omitirlo.

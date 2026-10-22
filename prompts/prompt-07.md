> prompt-07.md

# Generar estructura SDD y configuración de agentes IA

> Archivos y directorios a crear en la raíz del proyecto

Quiero que generes la estructura de carpetas y los archivos de configuración base para manejar este proyecto bajo la filosofía de Software-Defined Development (SDD). Ten en cuenta que mi entorno de ejecución y gestor de paquetes es Bun (con instalación de versiones exactas), por lo que las herramientas deben respetar esto. 

Aplica los siguientes cambios y creaciones:

- **Plano de construcción:** Crea el directorio `spec/` y dentro el archivo `spec.md`. Utiliza la estructura base del repositorio `hello-sdd` (Overview, Architecture, Data Models, API, UI/UX). Si existe la carpeta `.antigravity/context/`, lee los archivos Markdown allí para extraer un borrador inicial y poblar el `spec.md`.
- **Definición de agentes:** Crea el archivo `AGENTS.md` definiendo un equipo virtual de IA (ej. Frontend Engineer, Backend Developer, DBA). Especifica sus responsabilidades, restricciones y qué herramientas o comandos de Bun tienen permitido ejecutar.
- **Reglas de Claude Code:** Crea el archivo `CLAUDE.md`. Define aquí las convenciones de código, los comandos de compilación/test usando Bun, y la instrucción estricta de instalar siempre versiones exactas.
- **Configuración local:** Crea el archivo `CLAUDE.local.md` con una plantilla básica para variables de entorno locales (API keys, rutas absolutas). Agrega inmediatamente `CLAUDE.local.md` al archivo `.gitignore` del proyecto para evitar que se suba al repositorio.
- **Directorios de motores IA:** Crea las carpetas `.agents/` (para configuraciones/prompts de sub-agentes), `.antigravity/` (con sus subcarpetas `resources/`, `context/`, `commands/`) y `.claude/`. Agrega un archivo `.gitkeep` en los directorios vacíos para asegurar que se suban al repositorio.
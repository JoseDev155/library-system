# Workflow: sincronizar con GitLab

Normalmente lo dispara solo el hook `scripts/hooks/post-commit`. Úsalo para forzar una sincronización manual.

1. Desde el clon de GitHub, ejecuta `bash ~/sync-gitlab.sh` (o la ruta de `SYNC_GITLAB_SCRIPT`).
2. Revisa `.git/sync-gitlab.log` y reporta el resultado.
3. Si el script no existe en esta máquina, dilo; no crees uno ni pongas rutas personales en el repositorio.

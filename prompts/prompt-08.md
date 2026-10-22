# Sincronizar GitHub y GitLab

Tengo 2 cuentas, una de GitHub y otra de GitLab, con llaves SSH y GPG. Ademas, tengo un script que me permite sincronizar los repositorios de GitHub y GitLab, pero el archivo solo puede ejecutarse en bash (lo hago con Git Bash).

Quiero que cada vez que haga un commit en GitHub, se ejecute el script para sincronizarlo con GitLab. Puedes crear un script de hook de Git que se ejecute después de cada commit y que llame al script de sincronización, agregarlo como comando en alguna carpeta de hooks, `.agents/`, en el directorio `.claude/`, en los archivos `CLAUDE.md`, `CLAUDE.local.md` y `AGENTS.md`.

Archivos de configuración de los perfiles de Git (estan incluidos en el `.gitconfig` principal con la instrucción `includeIf`):

```bash
# Git Bash

~/.gitconfig-profile1 # Perfil de GitHub
~/.gitconfig-profile2 # Perfil de GitLab

nano ~/sync-gitlab.sh
chmod +x ~/sync-gitlab.sh
```

Carpetas de trabajo:

```plaintext
# Carpeta de GitHub
C:\Users\Jose_Ramos\Documents\Projects\git-profile1\library-system\

# Carpeta de GitLab
C:\Users\Jose_Ramos\Documents\Projects\git-profile2\josh-workspace\apps\library-system\
```
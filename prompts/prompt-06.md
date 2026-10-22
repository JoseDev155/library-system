# Modificar archivos generados y adaptarlos a Bun

> Archivos generados en `.agents/templates/`

Quiero que modifiques los archivos que generaste, segun lo que puse en esos archivos. Como extra, Vite+ al no funcionar de forma directa en Bun porque requiere Node.js, haz que se ejecute de forma directa exclusiva con Bun, pero, teniendo en cuenta lo siguiente:

* En Node.js yo trabajo con pnpm, y los archivos `.npmrc` y `.node-version`
* Tambien, agrego dependencias con `pnpm add -E ...` para instalar la version exacta y evitar que se actualice frecuentemente por temas de seguridad
* Quiero que adaptes el proyecto del frontend con Bun, para que tenga ese comportamiento de seguridad como cuando uso Node.js + pnpm
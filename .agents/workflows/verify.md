# Workflow: verificar

Úsalo al terminar cualquier tarea.

1. Ejecuta `scripts/verify.sh`.
2. Reporta el resultado de Ruff, pytest (cobertura de al menos 80 %), `vp check`, `vp test` y `vp build`.
3. Si algo falla, corrígelo y vuelve a ejecutar; no desactives pruebas para ponerlas en verde.
4. Si un paso no se pudo ejecutar, dilo explícitamente.

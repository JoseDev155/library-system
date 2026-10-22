# Base de datos

Como la conexion a BD es una clase generica, las bases de datos a usar seran:

1. PostgreSQL (principal)
2. MySQL y MariaDB (secundarias)

La dependencia para el ORM debe poder adaptarse a estas bases de datos, y debe ser compatible con Python 3.15.

Tareas:

* Elegir la dependencia ORM a usar que cumpla con estas condiciones, y que ademas, tengo soporte comunitario activo a largo plazo y documentacion suficiente.
* Adaptar el `spec.md` con las BDs a usar y la dependencia ORM elegida
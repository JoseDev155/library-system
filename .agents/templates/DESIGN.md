# DESIGN.md

Identidad visual del sistema de biblioteca. Sirve de referencia para humanos, para Claude Design y Google Stitch (que pueden importar o generar un `DESIGN.md`), y para los agentes que escriben el frontend.

> **Estado: provisional.** Los colores de abajo son estimaciones hechas a partir del logo de la universidad, no valores oficiales ni extraídos del CSS del sitio. Confírmalos con el cuentagotas del navegador, con la extracción desde URL de Stitch o con la captura web de Claude Design (ver "Cómo confirmar los tokens"). No hay manual de marca público de UNICAES que lo respalde.

## Referencia de estilo

Sitio de referencia: https://bibliotecadigital.catolica.edu.sv/ (Biblioteca Digital Miguel de Cervantes). Del contenido de la página se observa:

- Barra superior simple: logo a la izquierda, enlaces (Recursos, Blog, Comunidad, Tutoriales) y "Iniciar Sesión".
- Bloque de bienvenida con ilustración y un texto corto que invita a iniciar sesión con el correo institucional.
- **Tarjetas con imagen y título** para los recursos principales (Acceso Abierto, Acceso Controlado, Recursos UNICAES).
- **Categorías como enlaces tipo etiqueta** (Ciencias, Ingeniería, Salud, Matemáticas, etc.).
- Tarjetas de blog con imagen, título, extracto y autor.
- Pie de página en columnas: enlaces rápidos, servicios y contacto.

Lo que **no** se pudo leer: colores exactos, tipografías y tamaños (el contenido obtenido no incluye el CSS).

## Principios

1. **Claridad antes que decoración.** Pocas decisiones por pantalla.
2. **Pensado para personal de caja de mayor edad:** texto grande, botones grandes, un solo camino principal por pantalla y mensajes en español sencillo, sin jerga contable ni técnica.
3. **Confirmación antes de lo irreversible** (cobrar, condonar, dar de baja).
4. **Accesible:** WCAG 2.2 AA como mínimo.

## Tokens de color (provisionales)

| Token | Valor estimado | Uso |
|---|---|---|
| `--color-primary` | `#8B1E2D` | Vino institucional: barra superior, botones principales, enlaces destacados |
| `--color-primary-dark` | `#6E1824` | Hover y estados activos del primario |
| `--color-accent` | `#FFC000` | Dorado de acento: resaltados, indicadores, etiquetas |
| `--color-bg` | `#FFFFFF` | Fondo de página |
| `--color-surface` | `#F7F5F2` | Tarjetas y secciones alternas |
| `--color-border` | `#E5E0DA` | Bordes y separadores |
| `--color-text` | `#1F1F1F` | Texto principal |
| `--color-text-muted` | `#6B6B6B` | Texto secundario |
| `--color-success` | `#2E7D32` | Operación exitosa |
| `--color-warning` | `#B26A00` | Advertencias |
| `--color-error` | `#B3261E` | Errores |
| `--color-info` | `#1565C0` | Información |

Reglas de contraste:

- Texto blanco sobre `--color-primary`: cumple con holgura (alrededor de 9:1).
- Texto `--color-text` sobre `--color-accent`: cumple (alrededor de 10:1).
- **Nunca texto blanco sobre `--color-accent`**: el contraste es insuficiente.
- No comuniques estados solo con color: acompáñalos de icono y texto.

## Tipografía

Por confirmar con el sitio de referencia. Mientras tanto: una sans-serif legible del sistema o de Google Fonts, con estos tamaños mínimos:

| Contexto | Tamaño mínimo |
|---|---|
| Cuerpo general | 16 px |
| Pantallas de caja y mostrador | 18 px |
| Botones | 18 px, peso medio |
| Títulos de página | 28 px o más |

## Componentes

- **Botones:** altura mínima de 48 px. Un único botón primario (vino) por pantalla; los secundarios en contorno.
- **Tarjetas:** fondo `--color-surface`, borde `--color-border`, esquinas redondeadas, imagen o icono arriba y título claro.
- **Etiquetas de categoría:** enlaces tipo píldora para filtrar el catálogo.
- **Formularios:** una columna, etiquetas visibles encima del campo (no solo placeholder), un campo por línea, errores junto al campo con texto concreto.
- **Estados del ejemplar:** disponible, prestado, reservado, en reparación y baja, cada uno con color, icono y texto.
- **Tablas:** filas con buen espaciado, encabezado fijo, acciones al final de la fila.
- **Navegación:** barra superior con las secciones según el rol; el usuario solo ve lo que sus permisos permiten.

## Pantallas del alcance v1

1. Inicio de sesión
2. Búsqueda de catálogo y detalle de libro
3. Mis préstamos, reservas y multas
4. Mostrador del bibliotecario: préstamo y devolución
5. Gestión de catálogo
6. Caja: cobro de multas
7. Administración de usuarios y roles

## Cómo confirmar los tokens

- **Cuentagotas del navegador:** abre el sitio de referencia, abre las herramientas de desarrollo, inspecciona la barra superior y los botones, y copia los colores calculados (pestaña de estilos computados).
- **Google Stitch:** usa la extracción de sistema de diseño desde una URL y compara el resultado con esta tabla.
- **Claude Design:** usa la herramienta de captura web sobre la URL de referencia y revisa los tokens extraídos.

Después de confirmar, actualiza esta tabla y quita el aviso de "provisional".

## Marca

El logo y el nombre de la universidad son propiedad de la institución. Usarlos en el sistema requiere su autorización, y no están cubiertos por la licencia del código.
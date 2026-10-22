# DESIGN.md

Identidad visual del sistema de biblioteca. Sirve de referencia para humanos y para los agentes que escriben el frontend.

> **Referencia completa:** el sistema de diseño «Institucional Humanista», exportado desde Google Stitch, está en `.antigravity/resources/institucional_humanista/DESIGN.md`, junto a los prototipos de las pantallas. Este archivo es el resumen que usa el código: si hay una diferencia, se corrige aquí a propósito, no se copia a ciegas.
>
> **Estado de los colores: provisionales.** Se estimaron a partir del logo de la universidad; no son valores oficiales ni salen del CSS del sitio. No hay manual de marca público. La tipografía, las medidas y los componentes ya vienen definidos por el sistema de Stitch.

## Principios

1. **Claridad antes que decoración.** Pocas decisiones por pantalla.
2. **Pensado para personal de caja y mostrador de mayor edad:** texto grande, botones grandes, un solo camino principal por pantalla y mensajes en español sencillo, sin jerga contable ni técnica.
3. **Confirmación antes de lo irreversible** (cobrar, condonar, dar de baja).
4. **Accesible:** WCAG 2.2 AA como mínimo.
5. **Capas tonales y contornos nítidos**, sin sombras pesadas ni efectos de cristal.

## Tokens de color

| Token | Valor | Uso |
|---|---|---|
| `--color-primary` | `#8B1E2D` | Vino institucional: barra superior, botón principal (uno por pantalla), navegación activa |
| `--color-primary-dark` | `#6E1824` | Solo `hover`, `active` y anillos de foco del primario |
| `--color-accent` | `#FFC000` | Dorado: resaltados, insignias de categoría, atención secundaria |
| `--color-bg` | `#FFFFFF` | Fondo de página |
| `--color-surface` | `#F7F5F2` | Tarjetas, paneles de búsqueda y encabezados de tabla |
| `--color-border` | `#E5E0DA` | Bordes y separadores |
| `--color-text` | `#1F1F1F` | Texto principal |
| `--color-text-muted` | `#6B6B6B` | Texto secundario |
| `--color-success` | `#2E7D32` | Préstamo validado, saldo saldado, disponible |
| `--color-warning` | `#B26A00` | Próximo a vencer, reserva por expirar |
| `--color-error` | `#B3261E` | Multa pendiente, bloqueo de cuenta, baja |
| `--color-info` | `#1565C0` | Avisos, ejemplar prestado, guías |
| `--color-overlay` | `#1F1F1F` al 50 % | Fondo de los modales de confirmación |

Reglas de contraste:

- Texto blanco sobre `--color-primary`: cumple con holgura (más de 9:1).
- Texto `--color-text` sobre `--color-accent`: cumple (más de 10:1).
- **Nunca texto blanco sobre `--color-accent`**: el contraste es insuficiente.
- Ningún estado se comunica solo con color: va con icono y texto.

## Tipografía

Familia única: **Source Sans 3** (titulares, cuerpo y controles).

| Nivel | Tamaño / interlineado | Peso | Uso |
|---|---|---|---|
| `headline-xl` | 36 / 44 px (28 / 36 en móvil) | 700 | Título de página |
| `headline-lg` | 28 / 36 px (24 / 32 en móvil) | 600 | Título de sección |
| `headline-md` | 22 / 28 px | 600 | Título de tarjeta |
| `title-desk` | 20 / 26 px | 600 | Subtítulos |
| `body-operational` | 18 / 26 px | 400 y 600 | **Caja, préstamos y devoluciones**: todo texto funcional |
| `label-operational` | 18 / 24 px | 600 | Etiquetas y botones operativos |
| `body-default` | 16 / 24 px | 400 y 600 | Catálogo y consultas |
| `label-default` | 16 / 20 px | 500 | Etiquetas generales |
| `caption` | 14 / 18 px | 400 | Solo ISBN y metadatos no críticos |

No se permiten tamaños menores a 14 px.

## Forma, espacio y distribución

- **Radios:** 4 px en campos, botones y tarjetas; 8 px en modales y paneles; píldora completa (9999 px) solo para etiquetas de categoría y estados de ejemplar.
- **Espaciado:** `space-xs` 4 px, `space-sm` 8 px, `space-md` 16 px, `space-lg` 24 px, `space-xl` 40 px. Márgenes de 32 px (16 px en móvil) y gutters de 24 px (16 px en móvil).
- **Contenedor:** ancho máximo de 1280 px en vistas generales y 1024 px en formularios operativos.
- **Caja y mostrador:** una sola columna primaria centrada, campos en vertical.
- **Catálogo:** grilla de 12 columnas en escritorio, 4 en móvil.
- **Foco:** anillo de 3 px en `--color-primary` o `--color-info`, con 2 px de separación.

## Componentes

- **Botones:** altura mínima de 48 px (52 px recomendado en caja), texto de 18 px en peso 600 y al menos 24 px de espacio horizontal. Primario: fondo vino y texto blanco, **uno por pantalla**. Secundario: contorno de 2 px vino sobre fondo blanco. Destructivo: fondo `--color-error`, siempre con confirmación previa.
- **Campos:** etiqueta permanente encima (nunca solo placeholder), altura mínima de 48 px, borde de 1,5 px `--color-border` que pasa a vino en foco. Error debajo del campo, en `--color-error` a 16 px, con icono y qué hacer para corregirlo.
- **Etiquetas de categoría:** píldoras con fondo `--color-surface` y borde `--color-border`; seleccionadas pasan a fondo vino y texto blanco.
- **Estados de ejemplar** (píldora con icono y texto):

  | Estado | Fondo | Borde y texto |
  |---|---|---|
  | Disponible | `#E8F5E9` | `#2E7D32` |
  | Prestado | `#E3F2FD` | `#1565C0` |
  | Reservado | `#FFF8E1` | `#B26A00` |
  | En reparación o baja | `#FFEBEE` | `#B3261E` |

- **Tarjetas de catálogo:** fondo `--color-surface`, borde `--color-border`, carátula o icono arriba, título en seminegrita, autor y metadatos, y la etiqueta de disponibilidad al final.
- **Tablas operativas:** filas de al menos 56 px, encabezado fijo con fondo `--color-surface`, importes y fechas alineados a la derecha, nombres y descripciones a la izquierda, y las acciones al final de la fila.
- **Modales de confirmación irreversible:** 480 px de ancho, centrados sobre el overlay, con el resumen de la operación (monto a cobrar, libro a dar de baja) y confirmación explícita.
- **Navegación:** barra superior con las secciones según el rol; cada usuario ve solo lo que sus permisos permiten.

## Pantallas del alcance v1

Los prototipos están en `.antigravity/resources/`. Qué se adopta de cada uno y qué se adapta al implementar el frontend está en la spec, sección 12.

1. Inicio de sesión
2. Búsqueda de catálogo y detalle de libro
3. Mis préstamos, reservas y multas
4. Mostrador del bibliotecario: préstamo y devolución
5. Gestión de catálogo
6. Caja: cobro de multas
7. Administración de usuarios y roles

## Marca

El logo y el nombre de la universidad son propiedad de la institución. Usarlos en el sistema requiere su autorización, y no están cubiertos por la licencia del código.

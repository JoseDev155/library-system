---
name: Institucional Humanista
colors:
  surface: '#F7F5F2'
  surface-dim: '#dcd9d9'
  surface-bright: '#fcf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f2'
  surface-container: '#f0eded'
  surface-container-high: '#eae7e7'
  surface-container-highest: '#e5e2e1'
  on-surface: '#1b1b1c'
  on-surface-variant: '#574142'
  inverse-surface: '#303030'
  inverse-on-surface: '#f3f0ef'
  outline: '#8b7171'
  outline-variant: '#debfbf'
  surface-tint: '#a93441'
  primary: '#6b0119'
  on-primary: '#ffffff'
  primary-container: '#8b1e2d'
  on-primary-container: '#ff9da0'
  inverse-primary: '#ffb3b4'
  secondary: '#795900'
  on-secondary: '#ffffff'
  secondary-container: '#febf00'
  on-secondary-container: '#6c5000'
  tertiary: '#003a32'
  on-tertiary: '#ffffff'
  tertiary-container: '#005348'
  on-tertiary-container: '#83c5b7'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdada'
  primary-fixed-dim: '#ffb3b4'
  on-primary-fixed: '#40000b'
  on-primary-fixed-variant: '#881c2b'
  secondary-fixed: '#ffdf9e'
  secondary-fixed-dim: '#fbbd00'
  on-secondary-fixed: '#261a00'
  on-secondary-fixed-variant: '#5b4300'
  tertiary-fixed: '#acf0e0'
  tertiary-fixed-dim: '#90d3c5'
  on-tertiary-fixed: '#00201b'
  on-tertiary-fixed-variant: '#005046'
  background: '#fcf9f8'
  on-background: '#1b1b1c'
  surface-variant: '#e5e2e1'
  primary-dark: '#6E1824'
  border: '#E5E0DA'
  text-muted: '#6B6B6B'
  status-success: '#2E7D32'
  status-warning: '#B26A00'
  status-error: '#B3261E'
  status-info: '#1565C0'
typography:
  headline-xl:
    fontFamily: Source Sans 3
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
  headline-xl-mobile:
    fontFamily: Source Sans 3
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
  headline-lg:
    fontFamily: Source Sans 3
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
  headline-lg-mobile:
    fontFamily: Source Sans 3
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Source Sans 3
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
  title-desk:
    fontFamily: Source Sans 3
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 26px
  body-operational:
    fontFamily: Source Sans 3
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 26px
  body-operational-bold:
    fontFamily: Source Sans 3
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
  body-default:
    fontFamily: Source Sans 3
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-default-bold:
    fontFamily: Source Sans 3
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  label-operational:
    fontFamily: Source Sans 3
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  label-default:
    fontFamily: Source Sans 3
    fontSize: 16px
    fontWeight: '500'
    lineHeight: 20px
  caption:
    fontFamily: Source Sans 3
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 18px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

El sistema de diseño proyecta la identidad de una biblioteca universitaria arraigada en la tradición académica, la calidez del servicio y la sobriedad institucional. Está concebido bajo la premisa de "claridad antes que decoración", priorizando una legibilidad intransigente para personal operativo de mostrador y caja (incluyendo usuarios de mayor edad) así como para estudiantes e investigadores.

El lenguaje visual corresponde a un **Corporate Modern institucional** con matices humanos y orgánicos:
- **Estructura y serenidad:** Interfaz limpia, ordenada y libre de ruido visual superfluo. Cada elemento en pantalla responde a un propósito operativo concreto.
- **Rigor accesible:** Tipografía sobria, proporciones generosas y contraste intencionado para reducir la carga cognitiva durante jornadas intensivas de consulta, cobro y préstamo.
- **Tono institucional amigable:** Comunicación directa en español accesible, evitando tecnicismos bibliotecológicos o contables innecesarios.

## Colors

La paleta se fundamenta en el contraste categórico para asegurar la conformidad estricta con WCAG 2.2 AA y AAA en elementos de lectura crítica.

### Jerarquía y Aplicación
- **Primario (`#8B1E2D` - Vino Institucional):** Utilizado en la barra de navegación superior, botón de acción primaria singular por pantalla y estados activos de navegación clave. Presenta un ratio de contraste superior a 9:1 frente a texto blanco.
- **Primario Oscuro (`#6E1824`):** Reservado estrictamente para estados de interacción (`hover`, `active`) de componentes con fondo primario y bordes de enfoque de alto contraste.
- **Acento Dorado (`#FFC000`):** Destinado a resaltados, etiquetas de advertencia visual, insignias de categoría y elementos de atención secundaria. **Regla mandatoria:** Nunca utilizar tipografía blanca sobre este fondo; debe usarse exclusivamente texto neutro principal (`#1F1F1F`) logrando un contraste superior a 10:1.
- **Superficie (`#F7F5F2`) y Borde (`#E5E0DA`):** Base cálida para tarjetas, paneles de búsqueda y divisiones estructurales que mitigan el deslumbramiento en pantallas de terminales de escritorio continuas.
- **Estados Operativos:**
  - `status-success` (`#2E7D32`): Préstamos validados, devoluciones al día, saldo saldado.
  - `status-warning` (`#B26A00`): Préstamos próximos a vencer, reservas por expirar.
  - `status-error` (`#B3261E`): Ejemplar extraviado, multa pendiente, bloqueo de cuenta.
  - `status-info` (`#1565C0`): Notas de catálogo, avisos bibliotecarios, guías de sistema.

Ningún estado debe comunicarse únicamente mediante color; siempre debe acompañarse de texto descriptivo e iconografía complementaria.

## Typography

Se selecciona **Source Sans 3** como familia tipográfica unificada para titulares, cuerpo y controles. Su origen institucional, amplia altura de x y apertura de caracteres garantizan un rendimiento superior contra la fatiga visual en pantallas de mostrador.

### Niveles y Contextos
- **Escala Base:** El texto de consulta general parte de `16px` (`body-default`) para interfaces públicas de estudiantes y profesores.
- **Contexto Operativo (Caja, Préstamos y Devoluciones):** En estas pantallas se utiliza obligatoriamente el nivel `18px` (`body-operational` y `label-operational`) para todos los textos funcionales, resúmenes de cargos monetarios, títulos de libros procesados y etiquetas de entrada.
- **Botones e Interacción:** Todo texto interactivo en botones operativos utiliza un tamaño mínimo de `18px` con peso medio a seminegrita (`fontWeight: 600`) para maximizar la legibilidad táctil y visual a distancia de escritorio.
- **Tamaño mínimo:** No se permiten tamaños menores a `14px` (`caption`), los cuales quedan estrictamente reservados para códigos ISBN y metadatos no críticos de pie de página.

## Layout & Spacing

El sistema emplea un **grid fluido con contenedor contenido** de ancho máximo (1280px para vistas generales y 1024px para formularios operativos de flujo único).

### Grilla y Filosofía de Distribución
- **Terminales y Caja:** Se rige por el modelo de **una sola columna primaria centrada** con campos ordenados verticalmente. Esto previene omisiones visuales en saltos horizontales.
- **Catálogo y Consultas:** Grilla de 12 columnas en escritorio con gutters de `1.5rem` (24px) que colapsa a 4 columnas en móviles (`gutter-mobile` de 16px).
- **Ritmo Espacial:** Componentes agrupados usan `space-sm` (8px); distancias entre campos y etiquetas emplean `space-xs` (4px); separaciones entre bloques funcionales usan `space-lg` (24px) y `space-xl` (40px).

## Elevation & Depth

El sistema descarta sombras difusas pesadas, efectos de cristal y neomorfismo en favor de **capas tonales y contornos nítidos**, maximizando la solidez institucional y reduciendo distracciones.

- **Superficies Planas:** El fondo principal es blanco puro (`#FFFFFF`). Los contenedores de trabajo, tarjetas de ejemplares y bloques de filtros utilizan la superficie tonal `#F7F5F2`.
- **Delimitación Estructural:** Las divisiones y bordes de tarjetas utilizan el borde continuo `#E5E0DA` con un grosor de `1px` o `2px` según la jerarquía.
- **Focos y Diálogos:** Los modales de confirmación crítica (cobro de multas, condonaciones, anulaciones) se elevan sobre un oscurecimiento del fondo (`overlay` `#1F1F1F` al 50%) con un trazo sutil perimetral y una elevación física mínima de 4px para concentrar la atención del operario.
- **Estados de Foco:** Todo elemento interactivo al recibir navegación por teclado despliega un anillo exterior visible de 3px en `#8B1E2D` o `#1565C0` con un espaciador de 2px, garantizando total visibilidad accesible.

## Shapes

El sistema implementa un nivel de redondeo **Soft (`1`)**:
- **Bases y Botones:** Radio de `0.25rem` (4px) en campos de entrada, botones de formulario y tarjetas. Comunica seriedad institucional y proporciona límites claros para la puntería visual del cursor.
- **Contenedores de Mayor Escala:** Diálogos modales y paneles laterales de información utilizan un radio moderado de `0.5rem` (8px).
- **Excepción para Píldoras de Filtro (Chips):** Únicamente las etiquetas de categoría de catálogo ("Ciencias", "Salud", etc.) y los estados de ejemplar utilizan curvatura envolvente total (`9999px`), distinguiéndose con inmediatez de los botones de acción rectangular.

## Components

### Botones
- **Dimensiones y Tipografía:** Altura mínima obligatoria de **48px** (52px recomendado en caja), con tipografía en `18px`, peso seminegrita y espaciado horizontal de al menos 24px (`space-lg`).
- **Botón Primario:** Fondo `#8B1E2D`, texto `#FFFFFF`. Solo debe existir **uno por pantalla** que represente el objetivo prioritario del flujo (ej. "Realizar Préstamo", "Cobrar Multa").
- **Botón Secundario / Cancelar:** Fondo transparente o `#FFFFFF`, borde de 2px en `#8B1E2D`, texto `#8B1E2D`.
- **Botón Destructivo:** Fondo `#B3261E`, texto `#FFFFFF`, reservado para anulaciones o bajas de ejemplares, siempre protegido por confirmación previa.

### Campos de Entrada (Inputs)
- **Estructura en Columna Única:** Una etiqueta (`label`) permanente siempre ubicada arriba del campo con peso `600` a `18px` (o `16px` general). Prohibido el uso de placeholders como reemplazo de etiquetas.
- **Área Táctil:** Altura de campo mínima de 48px. Fondo `#FFFFFF`, borde perimetral de 1.5px `#E5E0DA` (cambia a `#8B1E2D` en foco).
- **Mensajería de Error:** Se muestra directamente debajo del campo en texto `#B3261E` a `16px`, acompañado del icono de advertencia y una instrucción directa para subsanarlo.

### Etiquetas de Categoría y Chips
- **Etiquetas de Catálogo:** Fondo `#F7F5F2`, borde `#E5E0DA`, forma redondeada de píldora, texto en `16px`. En estado seleccionado, pasan a fondo `#8B1E2D` con texto `#FFFFFF`.
- **Chips de Estado de Ejemplar:** Indicadores con forma de píldora que integran icono formal + texto claro:
  - *Disponible:* Fondo verde claro (`#E8F5E9`), borde y texto `#2E7D32`.
  - *Prestado:* Fondo azul claro (`#E3F2FD`), borde y texto `#1565C0`.
  - *En Reserva:* Fondo ámbar claro (`#FFF8E1`), borde y texto `#B26A00`.
  - *En Reparación / Baja:* Fondo rojo claro (`#FFEBEE`), borde y texto `#B3261E`.

### Tarjetas de Catálogo y Recursos
- Superficie `#F7F5F2` con contorno nítido en `#E5E0DA`.
- Estructura fija: Área superior para carátula o icono de recurso, título descriptivo en seminegrita (`headline-md` o `title-desk`), línea de autor y metadatos con espaciado de `1rem` (`space-md`), finalizando con etiqueta de disponibilidad.

### Tablas Operativas (Préstamos, Multas y Devoluciones)
- Filas amplias con una altura mínima de celda de 56px para evitar clics accidentales.
- Encabezados fijos de alto contraste (`#F7F5F2` con texto `#1F1F1F` en seminegrita).
- Alineación: Valores monetarios y fechas tabulares alineados a la derecha con cifras alineadas; descripciones y nombres a la izquierda.
- Acciones claras y espaciadas al final de la fila con botones de texto de alto contraste.

### Modales de Confirmación Irreversible
- Diálogo modal con ancho de 480px centrado.
- Requiere confirmación explícita mediante dos pasos o lectura obligatoria del resumen de la operación (monto a cobrar en caja, título de libro a dar de baja definitiva).
- Botones de acción dispuestos en orden: Cancelar a la izquierda, Acción Irreversible a la derecha con su color correspondiente.
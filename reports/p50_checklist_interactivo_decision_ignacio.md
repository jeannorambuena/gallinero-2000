# P50 — Checklist interactivo de decisión para Ignacio

## Qué se implementó

- Se convirtió `dashboard/public/checklist-ignacio.html` en un checklist interactivo de decisión.
- Se reorganizó el checklist en 8 grupos: dinero, ventas, cotizaciones, infraestructura, legal, logística, primera compra y medición de primera etapa.
- Cada punto quedó clasificado como `CRÍTICO` o `APOYO`.
- Se mantuvo visible la recomendación vigente: avanzar por etapas, alternativa recomendada +150 pollonas, alternativa conservadora +100 pollonas, no comprar +352 pollonas de una vez todavía y estado general analizar con cautela.
- Se agregó `dashboard/data/checklist-decision-ignacio.json` como respaldo estructurado del checklist.

## Cómo se guarda el avance

- Cada checkbox tiene un `id` estable.
- Al marcar o desmarcar, el estado se guarda automáticamente en `localStorage`.
- La clave usada es `gallinero_ignacio_checklist_decision_v1`.
- Al recargar o volver a abrir la página en el mismo navegador, las marcas se recuperan desde esa clave.
- El botón **Guardar avance** vuelve a escribir el estado actual y muestra el mensaje: “avance guardado en este navegador”.

## Qué calcula

La página calcula dinámicamente:

- porcentaje general de avance;
- puntos completados versus puntos totales;
- puntos críticos completados versus críticos totales;
- apoyos completados versus apoyos totales;
- críticos pendientes;
- apoyos pendientes.

También muestra dos barras de progreso: avance general y avance crítico.

## Reglas de estado

- Si faltan pendientes críticos: **ANALIZAR CON CAUTELA**.
  - Texto: “Todavía no conviene comprar aves, construir ni hacer inversión mayor. Faltan puntos críticos por confirmar.”
- Si todos los críticos están completos, pero faltan pendientes de apoyo: **CASI LISTO PARA DECIDIR**.
  - Texto: “Los puntos críticos están completos, pero conviene revisar los pendientes de apoyo antes de ejecutar.”
- Si todos los críticos y todos los apoyos están completos: **LISTO PARA REVISIÓN FINAL**.
  - Texto: “El checklist está completo. Aun así, la decisión final debe aprobarla Ignacio revisando cotizaciones, dinero disponible y condiciones reales.”

No se pasa el proyecto a verde por sí solo, no se indica inversión aprobada y no se recomienda comprar ahora.

## Resumen “Qué falta para pasar a verde”

El bloque se actualiza según las casillas pendientes:

- Si faltan críticos, indica cuántos faltan y lista cada pendiente crítico agrupado por tema.
- Si no faltan críticos, indica que los puntos críticos están completos y que todavía corresponde revisar apoyos y confirmar decisión final con Ignacio.
- Si todo está completo, indica que se deben reunir cotizaciones, respaldos y la decisión final de Ignacio antes de ejecutar.

## Cómo copiar resumen

El botón **Copiar resumen de pendientes** genera y copia al portapapeles un texto con:

- estado actual;
- avance general;
- críticos completados;
- pendientes críticos;
- pendientes de apoyo;
- recomendación vigente.

Usa `navigator.clipboard.writeText` cuando está disponible y un fallback con `document.execCommand('copy')` si el portapapeles moderno falla.

## Cómo imprimir

El botón **Imprimir / guardar como PDF** ejecuta `window.print()`.

Se actualizó `dashboard/public/informe-print.css` para:

- ocultar botones y acciones;
- mantener visible el resumen de estado y pendientes;
- evitar cortes de tarjetas cuando sea posible;
- conservar casillas marcadas en impresión usando `print-color-adjust` y estilos de checkbox.

## Limitaciones documentadas

1. El avance se guarda solo en el navegador.
2. No hay base de datos.
3. Si se borra caché o se cambia de dispositivo, las marcas pueden no estar.
4. Completar el checklist no aprueba automáticamente la inversión.
5. La decisión final debe revisarla Ignacio con cotizaciones, compradores y dinero real.

## Confirmación de alcance

P50 no cambia los números aprobados, no cambia la recomendación principal, no pasa el proyecto a verde automáticamente y no aprueba compra de aves, construcción ni inversión mayor.

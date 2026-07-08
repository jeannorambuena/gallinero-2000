# P49 — Informe visual para Ignacio

## Páginas visuales creadas

- `dashboard/public/informe-ignacio.html`
- `dashboard/public/resumen-ignacio.html`
- `dashboard/public/checklist-ignacio.html`
- `dashboard/public/anexo-calculos-ignacio.html`
- `dashboard/public/informe-print.css`

## Qué reemplazó a los enlaces .md

El bloque “Informe final disponible” del dashboard dejó de mostrar rutas internas Markdown como experiencia principal. Ahora muestra botones grandes hacia páginas HTML visuales:

1. Ver informe completo.
2. Ver resumen corto.
3. Ver checklist de reunión.
4. Ver anexo de cálculos.
5. Imprimir / guardar como PDF.
6. Copiar resumen WhatsApp.

Los archivos Markdown se mantienen como respaldo técnico en `reports/`.

## Cómo imprimir o guardar PDF

Cada página visual incluye el botón “Imprimir / guardar como PDF”, que ejecuta `window.print()`. También se agregó `dashboard/public/informe-print.css` con reglas de impresión para ocultar navegación y evitar cortes incómodos.

## Cómo copiar resumen WhatsApp

`dashboard/public/resumen-ignacio.html` incluye un bloque “Texto para WhatsApp” y un botón “Copiar resumen WhatsApp”. Usa `navigator.clipboard` cuando está disponible y respaldo con selección temporal si no lo está.

## Confirmación de coherencia numérica

Se mantuvieron los números principales:

- Total base con 1 mes de operación: $15.030.515.
- Diferencia contra $10.000.000: $5.030.515.
- Resultado mensual preliminar con trabajo: $959.617.
- Venta mínima con trabajo: 63,7 bandejas/semana.
- Tiempo estimado para recuperar inversión base con trabajo: 13,91 meses.
- +100: $3.053.801 / $473.570.
- +150: $4.369.862 / $529.532.
- +200: $5.685.923 / $585.493.
- +352: $15.030.515 / $959.617.

## Recomendación conservada

- Estado: analizar con cautela.
- Alternativa recomendada: +150 pollonas.
- +100 es la opción conservadora.
- +200 solo con compradores y caja más confirmados.
- +352 no se recomienda todavía; solo con financiamiento cerrado, equipamiento listo y venta confirmada.
- No se aprueba compra, construcción ni inversión mayor.

## Pendientes que siguen bloqueando pasar a verde

- Cotizaciones finales.
- Financiamiento completo.
- Caja mínima cubierta.
- Compradores confirmados por canal.
- Infraestructura validada.
- Equipamiento definido.
- Validación legal, sanitaria y tributaria.
- Plan de invierno.
- Calendario real.
- Decisión aprobada por Ignacio.

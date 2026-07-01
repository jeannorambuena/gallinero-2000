# P40 — Actualización datos reales Nacho P0

## Datos confirmados

- Gallinas iniciales: 150.
- Gallinas actuales: 148.
- Mortalidad actual: 2 gallinas.
- Producción promedio junio: 132 huevos/día.
- Día bajo: 120 huevos/día.
- Día alto: 142 huevos/día.
- Venta actual: 28 bandejas/semana.
- Precios por categoría: segunda $5.000, primera $6.000, extra $7.000.
- Alimento: 22 sacos/mes de 25 kg a $12.950 por saco.
- Agua mensual aproximada: $6.000.
- Vitaminas mensual: $20.000.
- Luz mensual actual: $0, pero sistema no estable.
- Gallinero actual: 9 x 3 x 2,3 m.
- Terreno disponible nuevo: 7 x 19 m.

## Datos calculados

- Postura actual aproximada: 132 / 148 = 89,2 %.
- Mortalidad actual aproximada: 2 / 150 = 1,3 %.
- Producción semanal aproximada: 132 x 7 = 924 huevos/semana.
- Producción semanal aproximada en bandejas: 924 / 30 = 30,8 bandejas/semana.
- Kilos de alimento mensual: 22 x 25 = 550 kg/mes.
- Costo mensual alimento: 22 x $12.950 = $284.900.
- Alimento por gallina al día: 550 kg / 30 días / 148 gallinas = 0,124 kg/día = 124 g/gallina/día.
- OPEX parcial confirmado: $284.900 + $6.000 + $20.000 = $310.900/mes.
- Superficie gallinero actual: 9 x 3 = 27 m².
- Superficie terreno disponible: 7 x 19 = 133 m².

## Datos pendientes

- Distribución semanal de las 28 bandejas por categoría: segunda, primera y extra.
- Precio promedio real por bandeja.
- Ingresos semanales y mensuales reales.
- OPEX total: transporte, envases/bandejas, cama/viruta, medicamentos, energía estable, mano de obra, mantenciones, sanitización e imprevistos.
- Panel solar / sistema eléctrico estable.
- Equipamiento interior avícola.
- Capital de trabajo.
- Formalización comercial/legal/contable.
- Validación técnica final del módulo 500.

## Impacto en dashboard

- La operación actual queda como parcialmente confirmada / alto avance.
- Comercial queda parcial: precios por categoría confirmados, pero distribución pendiente.
- Finanzas queda parcial: OPEX parcial confirmado de $310.900/mes, ingresos pendientes.
- Las alertas visibles incorporan distribución comercial pendiente, OPEX parcial, energía inestable y bloqueo de ROI/VAN/TIR/Payback.
- Las rutas de datos siguen usando `DATA_BASE = new URL('../data/', window.location.href)`.

## Por qué el semáforo sigue bloqueado

El semáforo se mantiene amarillo y conservador porque los nuevos datos mejoran el diagnóstico P0, pero todavía no cierran las condiciones de decisión. Falta calcular ingresos reales, OPEX total, CAPEX total, flujo completo, energía estable, validación comercial para 500 aves y validación técnica final. Por eso P1 preliminar sigue no habilitado, compra de aves bloqueada, construcción no autorizada, inversión mayor bloqueada y decisión final no disponible.

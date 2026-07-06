# P42 — Sincronización respuestas Nacho y dashboard ejecutivo

- Fecha: 2026-07-05 20:20 America/Santiago
- Rama: `dashboard/v2-ejecutivo-500`
- Commit anterior: `27076e0 P41 corrige validacion comercial y pendientes P0`

## Resumen

P42 sincroniza dashboard, datos, CSV, documentación y validadores con las últimas respuestas reales de Nacho. La corrección principal es separar el objetivo de **500 gallinas totales** de la hipótesis antigua de comprar 500 pollonas, actualizar el mix real de bandejas y completar OPEX parcial con envases, viruta, reparto y medicamentos adicionales informados.

El estado del proyecto se mantiene **amarillo**: no se autoriza compra de aves, construcción ni inversión mayor.

## Inconsistencias detectadas

- CAPEX principal antiguo basado en comprar 500 unidades al precio histórico de $8.500, equivalente a $4.250.000.
- `precio_pollona = $8.500` usado como vigente en vez de histórico.
- Supuesto principal antiguo de 500 pollonas nuevas.
- Mix antiguo o ambiguo de bandejas; el correcto P42 es **6 / 13 / 9**.
- Envases, viruta, reparto, panel solar y formalización marcados como pendientes aunque Nacho ya respondió parte de esos puntos.
- Validador P0 esperando valores antiguos de ingresos y CAPEX.

## Datos nuevos incorporados

### Venta actual

- Total actual: **28 bandejas/semana**.
- Segunda: **6 bandejas/semana**.
- Primera: **13 bandejas/semana**.
- Extra: **9 bandejas/semana**.
- Ingreso semanal calculado: **$171.000**.
- Precio promedio por bandeja: **$6.107 aprox.**
- Ingreso mensual estimado: **$741.000**.

### Meta comercial

- Meta: **100 bandejas/semana**.
- Trabajo: 20.
- Vecinos: 30.
- Almacenes: 30.
- Facebook: 20.

Marcada como **plan comercial por validar**, escenario base; validar operación, precios netos y cobranza.

### OPEX parcial actualizado

- Alimento: **$284.900/mes**.
- Agua: **$6.000/mes**.
- Vitaminas: **$20.000/mes**.
- Envases actuales: **$12.740/mes aprox.**
- Viruta: **$10.000/mes**.
- Bencina/reparto: **$10.000/mes**.
- Medicamentos adicionales fuera de vitaminas: **$0 informado**.

OPEX parcial conocido actualizado: **$343.640/mes**.

No se cierra OPEX total.

## Corrección de pollonas

- Gallinas actuales: **148**.
- Objetivo operativo: **500 gallinas totales**.
- Pollonas/gallinas faltantes: **352**.
- Precio histórico pagado 16/01/2026: **$8.500**.
- Precio vigente nuevas compras: **$12.000**.
- Costo histórico comparable: **352 x $8.500 = $2.992.000**.
- Costo vigente pollonas faltantes: **352 x $12.000 = $4.224.000**.
- Diferencia por pollona: **$3.500**.
- Incremento CAPEX pollonas: **$1.232.000**.

El supuesto antiguo de comprar 500 unidades al precio histórico de $8.500 queda eliminado como CAPEX principal y solo se conserva conceptualmente como antecedente histórico descartado.

## CAPEX corregido

- Galpón COT-GN-0035: **$5.547.765**.
- Pollonas faltantes: **$4.224.000**.
- Subtotal conocido corregido: **$9.771.765**.

Este subtotal **no es CAPEX total cerrado**. Faltan comederos, bebederos, ponederos, bomba de agua, mallas interiores, ampliación bodega alimento, alimento inicial, logística, formalización y eventuales permisos/costos sanitarios.

## Energía, equipamiento y formalización

- Panel solar comprado por **$300.000**.
- Falta validar dimensionamiento, instalación, autonomía, baterías/inversor si aplica y capacidad para bomba/luces/cámaras.
- Tiene estanque de agua, luz/panel solar y bodega de alimento.
- Falta comederos, bebederos, nidos/ponederos, bomba, mallas interiores y ampliación bodega.
- Si escala a 500, Nacho daría boleta y factura; siguen pendientes ruta y costos tributarios/sanitarios.

## Archivos modificados

Principales:

- `dashboard/data/flujo-caja-preliminar.json`
- `dashboard/data/finanzas-preliminares.json`
- `dashboard/data/capex-preliminar.json`
- `dashboard/data/indicadores-comerciales.json`
- `dashboard/data/validacion-comercial.json`
- `dashboard/data/datos-faltantes.json`
- `dashboard/data/resumen-ejecutivo-p0.json`
- `dashboard/data/alertas-p0.json`
- `dashboard/data/estado-proyecto.json`
- `dashboard/data/semaforo-decision.json`
- `dashboard/data/logistica-construccion.json`
- `dashboard/data/legal-contable.json`
- `dashboard/public/app.js`
- `datos/procesados/indicadores/*.csv`
- `datos/entrada/**/*.csv`
- `docs/01-p0-diagnostico/*.md`
- `docs/02-informes/informe-ejecutivo-nacho-500.md`
- `scripts/auditoria/validar_indicadores_p0.py`
- `scripts/auditoria/verificar_dashboard_publicado.sh`

## Validaciones

Resultado final local:

```text
node --check dashboard/public/app.js: OK
python3 scripts/auditoria/validar_json_dashboard.py: OK JSON dashboard: 20 archivos válidos
python3 scripts/auditoria/validar_csv_indicadores.py: OK CSV indicadores: 8 archivos válidos / OK CSV entrada: 11 archivos válidos
python3 scripts/auditoria/validar_todo_p0.py: Resultado general OK
```

Grep de residuos críticos P42:

```text
Patrones antiguos críticos de CAPEX pollonas y precio histórico usado como vigente: sin hallazgos
```

## Pendientes que siguen bloqueando P1

- Precio real confirmado por canal/cliente.
- Compromisos reales de compra.
- Costo comederos.
- Costo bebederos.
- Costo ponederos.
- Costo bomba.
- Costo mallas interiores.
- Costo ampliación bodega.
- Alimento inicial para escala.
- Verificación operativa del panel solar comprado.
- Agua/bomba.
- Formalización tributaria/sanitaria.
- Capital de trabajo.
- Logística de invierno.

## Conclusión

P42 mejora la coherencia del dashboard y deja datos reales sincronizados, pero mantiene la decisión bloqueada. El proyecto sigue en diagnóstico amarillo: no invertir todavía.

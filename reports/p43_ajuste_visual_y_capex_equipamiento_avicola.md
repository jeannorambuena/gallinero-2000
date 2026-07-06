# P43 — Ajuste visual y CAPEX equipamiento avícola

- Fecha: 2026-07-05 21:08 America/Santiago
- Rama: `dashboard/v2-ejecutivo-500`
- Commit base P42: `816ef1a3261b0d28e8fe9e0ba19cdd8d752a33d8`

## Resumen

P43 ajusta el dashboard ejecutivo después de revisión visual de P42 e incorpora aclaraciones de Jean sobre panel solar, criterio comercial base y CAPEX faltante de equipamiento avícola.

El estado sigue **amarillo**: no se habilita P1 preliminar, compra de aves, construcción ni inversión mayor.

## Ajustes visuales realizados

- Se eliminó la lectura de la lectura comercial antigua como bloqueo principal.
- Se reemplazó por:
  - meta comercial base: **100 bandejas/semana**;
  - producción estimada 500 aves: **104,1 bandejas/semana**;
  - diferencia técnica: **4,1 bandejas/semana**.
- Se corrigieron textos residuales de distribución por categoría.
- Se corrigió OPEX parcial a **$343.640/mes**.
- Se ajustó el nombre del indicador de costo unitario del galpón a **Costo galpón por ave objetivo**.

## Aclaración panel solar

Criterio P43:

> Panel solar comprado por $300.000, considerado como paquete completo informado por Nacho para alimentar bomba, luces y cámaras. Pendiente solo verificación operativa en terreno.

El panel solar ya no queda como cotización principal pendiente ni como bloqueo financiero principal.

## Cierre comercial con meta 100 bandejas

La meta de **100 bandejas/semana** se usa desde P43 como escenario comercial base de análisis.

Canales objetivo:

- Trabajo: 20 bandejas/semana.
- Vecinos: 30 bandejas/semana.
- Almacenes: 30 bandejas/semana.
- Facebook: 20 bandejas/semana.

Pendientes comerciales redefinidos:

- precios netos por canal;
- forma de pago;
- cobranza;
- estabilidad semanal;
- requisitos de boleta/factura por canal.

## CAPEX equipamiento avícola

Se creó:

- `dashboard/data/capex-equipamiento-avicola.json`

Ítems pendientes:

- Comederos para 500 aves.
- Bebederos para 500 aves.
- Nidos/ponederos para 500 aves.
- Bomba de agua.
- Mallas interiores.
- Ampliación o bodega interna de alimento.
- Instalación o distribución interna de agua si aplica.
- Instalación o distribución interna eléctrica si aplica.

No se inventaron precios. Todos quedan como `pendiente_cotizacion`.

## Archivos principales modificados

- `dashboard/data/capex-equipamiento-avicola.json`
- `dashboard/data/capex-preliminar.json`
- `dashboard/data/finanzas-preliminares.json`
- `dashboard/data/flujo-caja-preliminar.json`
- `dashboard/data/indicadores-comerciales.json`
- `dashboard/data/validacion-comercial.json`
- `dashboard/data/datos-faltantes.json`
- `dashboard/data/alertas-p0.json`
- `dashboard/data/resumen-ejecutivo-p0.json`
- `dashboard/data/semaforo-decision.json`
- `dashboard/public/app.js`
- `datos/entrada/capex/cotizaciones-capex.csv`
- `datos/procesados/indicadores/p0-capex-preliminar.csv`
- `docs/01-p0-diagnostico/capex-preliminar.md`
- `docs/01-p0-diagnostico/datos-faltantes.md`
- `docs/02-informes/informe-ejecutivo-nacho-500.md`
- `scripts/auditoria/validar_indicadores_p0.py`
- `scripts/auditoria/validar_json_dashboard.py`

## Validaciones ejecutadas

Resultado final P43:

```bash
node --check dashboard/public/app.js
python3 scripts/auditoria/validar_json_dashboard.py
python3 scripts/auditoria/validar_csv_indicadores.py
python3 scripts/auditoria/validar_todo_p0.py
```

Resultados:

- `node --check dashboard/public/app.js`: OK.
- JSON dashboard: OK, 21 archivos válidos.
- CSV indicadores: OK, 8 archivos válidos.
- CSV entrada: OK, 11 archivos válidos.
- Indicadores P0: OK.
- Resultado general: OK.

Greps P43:

- Residuos críticos antiguos: sin hallazgos.
- Residuos de lectura comercial antigua: sin hallazgos.
- Marcas nuevas P43: presentes OPEX actualizado, meta 100, diferencia técnica 4,1, panel solar comprado y archivo de CAPEX equipamiento avícola.

## Pendientes definitivos para cierre financiero

- CAPEX equipamiento avícola cotizado.
- OPEX total de escala 500.
- Capital de trabajo inicial.
- Precios netos, forma de pago y estabilidad por canal.
- Formalización tributaria/sanitaria valorizada.
- Logística de invierno.
- Flujo financiero completo y estacional.
- EBITDA, Payback, ROI, VAN y TIR solo después de cerrar CAPEX/OPEX/flujo.

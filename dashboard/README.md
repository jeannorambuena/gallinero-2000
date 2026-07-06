# Dashboard V2 — Gallinero Nacho

Dashboard ejecutivo P0 en HTML/CSS/JS puro. Su propósito es entregar a Nacho una lectura rápida, visual y compacta del estado del proyecto, sin convertir el diagnóstico en una autorización de inversión.

## Propósito

- Resumir el diagnóstico P0 en una pantalla ejecutiva.
- Mostrar el escenario base vigente: **500 aves totales**.
- Dejar claro el estado actual: **amarillo**.
- Separar lo permitido ahora de lo bloqueado.
- Mantener 648 aves solo como escenario anterior/referencial.

## Secciones principales

1. **Resumen ejecutivo:** estado general, P1 preliminar, compra, construcción e inversión mayor.
2. **Operación actual:** gallinas, producción, venta, postura, mortalidad, agua, edad y raza.
3. **Escenario base 500 aves:** producción estimada, bandejas requeridas, validación operativa comercial, agua, superficie y costo pendiente.
4. **Comparativo de escalas:** 500, 1000 y 2000 aves como referencia visual; 1000 y 2000 son comparativos futuros.
5. **Semáforo de inversión:** rojo, amarillo y verde con regla de decisión.
6. **Bloqueadores principales:** mercado, CAPEX, flujo, agua, energía, logística, legal/contable y P1 preliminar.
7. **Riesgos clave:** lectura breve por dimensión.
8. **Qué sí / qué no:** acciones permitidas y acciones bloqueadas.

## Cómo levantarlo localmente

Desde la raíz del repositorio:

```bash
python3 -m http.server 8081 --bind 127.0.0.1 --directory dashboard
```

Abrir:

```text
http://127.0.0.1:8081/public/
```

## Qué representa el estado amarillo

Amarillo significa que el proyecto tiene una base productiva interesante, pero todavía no tiene mercado, CAPEX, flujo, agua/energía, logística y revisión legal/contable suficientemente cerrados.

En amarillo solo se permite inversión menor/controlada para desbloquear información: cotizaciones, mediciones, croquis, validación comercial, asesoría legal/contable y dimensionamiento técnico.

## Advertencia de decisión

Este dashboard **no autoriza**:

- compra de aves o pollonas;
- construcción del galpón;
- inversión mayor;
- habilitación de P1 preliminar;
- rentabilidad cerrada.

El escenario base vigente es **500 aves totales**. El escenario de **648 aves** queda solo como histórico/referencial del P0 original.

## Validación

```bash
git diff --check
node --check dashboard/public/app.js
python3 scripts/auditoria/validar_todo_p0.py
```

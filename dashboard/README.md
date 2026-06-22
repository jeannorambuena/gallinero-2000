# Dashboard — Gallinero Nacho

Dashboard P0 en HTML/CSS/JS puro. Resume estado, riesgos, finanzas, CAPEX, flujo, semáforo, replanteo de escala y criterios de avance.

## Estado vigente

- Nuevo escenario base: **500 aves totales**.
- Escenario anterior: **648 aves**, referencia histórica.
- Estado general: amarillo.
- P1 preliminar: no habilitado.
- Compra de aves: bloqueada.
- Construcción: no autorizada.
- Inversión mayor: no autorizada.

## Nuevas secciones visuales

- Replanteo base 500 aves.
- Decisión de inversión por semáforo.
- Costo de galpón por escala: 500, 1000 y 2000 aves.

## Datos principales

- `dashboard/data/replanteo-escala.json`
- `dashboard/data/matriz-decision-inversion.json`
- `dashboard/data/estimacion-galpones.json`
- `dashboard/data/resumen-ejecutivo-p0.json`
- `dashboard/data/criterios-p1.json`
- `dashboard/data/flujo-caja-preliminar.json`
- `dashboard/data/capex-preliminar.json`
- `dashboard/data/validacion-comercial.json`
- `dashboard/data/desbloqueo-p1-preliminar.json`
- `dashboard/data/semaforo-decision.json`
- `dashboard/data/estado-proyecto.json`

## Ejecutar dashboard

Desde la raíz del repositorio:

```bash
python3 -m http.server 8081 --bind 127.0.0.1 --directory dashboard
```

Abrir:

```text
http://127.0.0.1:8081/public/
```

## Auditoría

```bash
python3 scripts/auditoria/validar_todo_p0.py
```

## Advertencia

El dashboard no autoriza compra de pollonas, construcción ni inversión mayor. En semáforo amarillo solo permite inversión menor de desbloqueo: cotizaciones, mediciones, visitas técnicas, croquis, validación comercial, asesoría legal/contable y dimensionamiento agua/energía.

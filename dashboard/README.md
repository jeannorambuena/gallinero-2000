# Dashboard — Gallinero Nacho

## Objetivo

Este dashboard resume el avance del P0, los indicadores productivos, comerciales, financieros preliminares y el semáforo de decisión del proyecto Gallinero Nacho.

## Módulos actuales

- `dashboard/data/estado-proyecto.json`
- `dashboard/data/indicadores-productivos.json`
- `dashboard/data/indicadores-comerciales.json`
- `dashboard/data/finanzas-preliminares.json`
- `dashboard/data/semaforo-decision.json`
- `dashboard/data/alertas-p0.json`
- `dashboard/data/datos-faltantes.json`

## Abrir localmente

Desde la raíz del repositorio:

```bash
python3 -m http.server 8080 --bind 127.0.0.1 --directory dashboard
```

Luego abrir:

```text
http://127.0.0.1:8080/public/
```

## Estado actual

- Fase: P0 — Diagnóstico real
- Avance P0 estimado: 80%
- Semáforo general: amarillo
- P1 preliminar: no habilitado todavía
- P1 definitivo: no habilitado
- Compra de 500 pollonas: no autorizada

## Lectura resumida

- Productivo: verde
- Comercial: amarillo_rojo
- Financiero: amarillo
- Constructivo: pendiente
- Legal/contable: pendiente

## Advertencia

El dashboard es preliminar. Sirve para orientar decisiones, pero no autoriza inversión, diseño definitivo ni compra de 500 pollonas.

## Próximos módulos posibles

- consolidación documental P0
- subproyecto agua
- subproyecto solar
- riesgos constructivos
- riesgos legales y contables
- flujo de caja proyectado
- P1 preliminar

# Dashboard — Gallinero Nacho

## Objetivo

Este dashboard resume el avance del P0, el resumen ejecutivo P0, los indicadores productivos, comerciales, financieros preliminares, CAPEX preliminar, flujo de caja preliminar, criterios de habilitación P1 preliminar, subproyectos críticos de agua y energía, diagnóstico logístico/constructivo, validación comercial, revisión legal/contable preliminar y el semáforo de decisión del proyecto Gallinero Nacho.

## Referencias de cierre P0

- Checklist MVP P0: `docs/01-p0-diagnostico/mvp-p0-checklist.md`
- Cierre preliminar P0: `docs/01-p0-diagnostico/cierre-preliminar-p0.md`
- Resumen ejecutivo P0: `docs/01-p0-diagnostico/resumen-ejecutivo-p0.md`

## Módulos actuales

- `dashboard/data/resumen-ejecutivo-p0.json`
- `dashboard/data/estado-proyecto.json`
- `dashboard/data/indicadores-productivos.json`
- `dashboard/data/indicadores-comerciales.json`
- `dashboard/data/finanzas-preliminares.json`
- `dashboard/data/semaforo-decision.json`
- `dashboard/data/alertas-p0.json`
- `dashboard/data/datos-faltantes.json`
- `dashboard/data/subproyectos-criticos.json`
- `dashboard/data/logistica-construccion.json`
- `dashboard/data/validacion-comercial.json`
- `dashboard/data/legal-contable.json`
- `dashboard/data/capex-preliminar.json`
- `datos/procesados/indicadores/p0-capex-preliminar.csv`
- `dashboard/data/flujo-caja-preliminar.json`
- `datos/procesados/indicadores/p0-flujo-caja-preliminar.csv`
- `dashboard/data/criterios-p1.json`

## Dashboard visual

Dashboard visual básico mejorado, sin dependencias externas. Usa HTML, CSS y JavaScript puro.

Desde la raíz del repositorio:

```bash
python3 -m http.server 8081 --bind 127.0.0.1 --directory dashboard
```

Luego abrir:

```text
http://127.0.0.1:8081/public/
```

## Auditoría de datos

Desde la raíz del repositorio:

```bash
python3 scripts/auditoria/validar_todo_p0.py
```

## Estado actual

- Fase: P0 — Diagnóstico real
- Avance P0 estimado: 80%
- Semáforo general: amarillo
- MVP P0: funcional
- P1 preliminar: no habilitado todavía
- P1 definitivo: bloqueado
- Compra de 500 pollonas: bloqueada

## Lectura resumida

- Productivo: verde
- Comercial: amarillo_rojo
- Financiero: amarillo
- CAPEX preliminar: pendiente/amarillo
- Flujo de caja preliminar: amarillo
- Resumen ejecutivo P0: amarillo
- Criterios P1 preliminar: no habilitado
- Constructivo: pendiente/amarillo
- Logístico: amarillo_rojo
- Agua: amarillo
- Energía solar: amarillo
- Validación comercial: amarillo_rojo
- Legal/contable: pendiente

## Advertencia

El dashboard es preliminar. Sirve para orientar decisiones, pero no autoriza inversión, diseño definitivo, construcción ni compra de 500 pollonas.

## Próximos pasos posibles

- validación comercial real
- croquis del terreno 19 x 7 m
- dimensionamiento real de agua
- dimensionamiento real de energía
- CAPEX completo con cotizaciones
- flujo proyectado 648 aves
- revisión legal/contable externa
- criterios de no avance cuantificados
- eventual P1 preliminar

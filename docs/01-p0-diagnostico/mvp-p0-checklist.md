# MVP P0 — Checklist final

## Objetivo del MVP P0

Dejar una base funcional y auditable del diagnóstico P0 del Proyecto Gallinero Nacho, con dashboard visual, datos estructurados, documentación narrativa, alertas, criterios de decisión y auditoría automática.

El MVP P0 no autoriza compra de 500 pollonas, construcción ni inversión mayor. Su objetivo es ordenar la información disponible y dejar claro qué falta para evaluar una eventual P1 preliminar.

## Checklist de módulos listos

- [x] Estructura base repo.
- [x] Dashboard visual.
- [x] Resumen ejecutivo P0.
- [x] Diagnóstico P0 narrativo.
- [x] Indicadores productivos.
- [x] Indicadores comerciales.
- [x] Finanzas preliminares.
- [x] CAPEX preliminar.
- [x] Flujo de caja preliminar.
- [x] Alertas P0.
- [x] Datos faltantes.
- [x] Agua.
- [x] Energía solar.
- [x] Logística.
- [x] Construcción.
- [x] Validación comercial.
- [x] Legal/contable.
- [x] Criterios P1 preliminar.
- [x] Auditoría automática.

## Checklist de módulos pendientes

- [ ] Validación comercial real.
- [ ] Croquis del terreno 19 x 7 m.
- [ ] Dimensionamiento real de agua.
- [ ] Dimensionamiento real de energía.
- [ ] CAPEX completo con cotizaciones.
- [ ] Flujo proyectado 648 aves.
- [ ] Revisión legal/contable externa.
- [ ] Criterios de no avance cuantificados.
- [ ] Eventual P1 preliminar.

## Checklist de decisiones bloqueadas

- [x] P1 preliminar: no habilitado.
- [x] P1 definitivo: bloqueado.
- [x] Compra de 500 pollonas: bloqueada.
- [x] Construcción: no autorizada.
- [x] Inversión mayor: no autorizada.
- [x] VAN, TIR, ROI y Payback: bloqueados.

## Checklist de comandos de operación

### Abrir dashboard

Desde la raíz de la repo:

```bash
python3 -m http.server 8081 --bind 127.0.0.1 --directory dashboard
```

Abrir en navegador:

```text
http://127.0.0.1:8081/public/
```

### Ejecutar auditoría

```bash
python3 scripts/auditoria/validar_todo_p0.py
```

## Checklist de auditoría

Resultado esperado:

- [x] JSON dashboard: OK.
- [x] CSV indicadores: OK.
- [x] Indicadores P0: OK.
- [x] Resultado general: OK.

## Estado final del MVP P0

- Rama: `p0/consolidacion-diagnostico-nacho`.
- Estado general: amarillo.
- P0: avanzado preliminarmente.
- MVP P0: funcional.
- Dashboard: funcional y visualmente reorganizado.
- Auditoría automática: creada.
- P1 preliminar: no habilitado.
- P1 definitivo: bloqueado.
- Compra de 500 pollonas: bloqueada.

El MVP P0 queda listo como base de diagnóstico y control. La siguiente etapa no es inversión: es validar brechas críticas antes de decidir si corresponde habilitar una P1 preliminar.

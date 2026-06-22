# Cierre preliminar P0 — Proyecto Gallinero Nacho

## Propósito

Consolidar el estado final del MVP P0 y dejar una lectura clara sobre qué quedó listo, qué falta, qué decisiones siguen bloqueadas y cuáles son los próximos pasos recomendados.

Este cierre es preliminar: P0 está avanzado, pero no cerrado definitivamente.

## Lectura ejecutiva

El proyecto tiene una buena base productiva actual, pero el salto a 648 aves todavía no está validado. La mayor brecha está en mercado, CAPEX total, flujo proyectado, agua, energía, logística, construcción y revisión legal/contable.

El semáforo general se mantiene amarillo. No se cambia el estado a verde.

## Estado actual

- Rama: `p0/consolidacion-diagnostico-nacho`.
- Fase actual: P0 — Diagnóstico real.
- Estado general: amarillo.
- P0: avanzado preliminarmente.
- MVP P0: funcional.
- P1 preliminar: no habilitado.
- P1 definitivo: bloqueado.
- Compra de 500 pollonas: bloqueada.
- Construcción: no autorizada.
- Inversión mayor: no autorizada.

## Qué quedó listo

- Dashboard visual funcional y reorganizado.
- Resumen ejecutivo P0.
- Diagnóstico narrativo P0.
- Indicadores productivos, comerciales y financieros preliminares.
- Semáforo de decisión.
- Alertas P0 y datos faltantes.
- Subproyectos críticos de agua y energía solar.
- Diagnóstico logístico y constructivo preliminar.
- Validación comercial preliminar.
- Riesgos legales/contables preliminares.
- CAPEX preliminar.
- Flujo de caja preliminar.
- Criterios de habilitación P1 preliminar.
- Auditoría automática P0.

## Qué falta

- Validación comercial real con clientes/canales y bandejas comprometidas.
- Croquis del terreno 19 x 7 m.
- Dimensionamiento real de agua.
- Dimensionamiento real de energía solar.
- CAPEX completo con cotizaciones.
- Flujo proyectado para 648 aves.
- Revisión legal/contable externa.
- Criterios de no avance cuantificados.
- Decidir si eventualmente corresponde abrir P1 preliminar.

## Decisión actual

- P1 preliminar: no habilitado.
- P1 definitivo: bloqueado.
- Compra de 500 pollonas: bloqueada.
- Construcción: no autorizada.
- Inversión mayor: no autorizada.
- VAN, TIR, ROI y Payback: no calculados y bloqueados.

## Por qué no se habilita P1 preliminar todavía

P1 preliminar requiere condiciones mínimas que aún no están completas: mercado validado, revisión legal/contable preliminar, croquis, alternativa constructiva, dimensionamiento de agua y energía, evaluación logística, CAPEX por categorías, flujo proyectado y criterios de no avance.

Mientras esos puntos no estén resueltos, P1 preliminar no debe habilitarse formalmente.

## Por qué no se compran pollonas

La compra de 500 pollonas sigue bloqueada porque:

- La venta actual es de 28 bandejas/semana.
- La operación proyectada de 648 aves requiere cerca de 135 bandejas/semana.
- La brecha comercial es de 107 bandejas/semana.
- El CAPEX total está pendiente.
- El flujo proyectado para 648 aves está incompleto.
- Agua, energía, construcción y logística no están cerradas.
- Legal/contable sigue pendiente.

Comprar pollonas antes de cerrar estos puntos puede producir sobreproducción, falta de infraestructura, costos no considerados y riesgo financiero.

## Próximos pasos recomendados

1. Validar mercado real para 130–135 bandejas/semana.
2. Preparar croquis del terreno inmediato 19 x 7 m.
3. Dimensionar agua.
4. Dimensionar energía solar.
5. Cotizar CAPEX completo por categorías.
6. Preparar flujo proyectado para 648 aves.
7. Revisar legal/contable con apoyo externo.
8. Definir criterios cuantificados de no avance.
9. Re-evaluar si corresponde habilitar P1 preliminar.

## Operación del MVP

### Dashboard

```bash
python3 -m http.server 8081 --bind 127.0.0.1 --directory dashboard
```

Abrir:

```text
http://127.0.0.1:8081/public/
```

### Auditoría

```bash
python3 scripts/auditoria/validar_todo_p0.py
```

Resultado esperado:

- JSON dashboard: OK.
- CSV indicadores: OK.
- Indicadores P0: OK.
- Resultado general: OK.

## Conclusión

El MVP P0 queda funcional y consolidado. Sirve como base clara para revisar el proyecto, explicar el estado a terceros y decidir próximos levantamientos de información.

La decisión actual sigue siendo prudente: no comprar 500 pollonas, no construir, no invertir y no habilitar P1 preliminar hasta cerrar las brechas críticas.

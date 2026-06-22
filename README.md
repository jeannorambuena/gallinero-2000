# Gallinero Nacho — Diagnóstico P0

Repositorio técnico y evolutivo para diagnosticar, diseñar, presupuestar, construir y evaluar un gallinero modular escalable.

## Estado actual del proyecto

- Rama P0: `p0/consolidacion-diagnostico-nacho`.
- Fase actual: P0 — Diagnóstico real.
- Estado general: amarillo.
- P0: avanzado preliminarmente.
- MVP P0: funcional.
- Dashboard: funcional y visualmente reorganizado.
- Auditoría automática: creada.
- P1 preliminar: no habilitado.
- P1 definitivo: bloqueado.
- Compra de 500 pollonas: bloqueada.
- Construcción: no autorizada.
- Inversión mayor: no autorizada.

## Decisión actual

El proyecto tiene una buena base productiva, pero el salto a 648 aves todavía no está validado. No se autoriza compra de 500 pollonas, construcción ni inversión mayor.

P1 preliminar solo podrá evaluarse después de cerrar brechas críticas: mercado, croquis, CAPEX completo, flujo proyectado, agua, energía, logística y legal/contable.

## Dashboard P0

Desde la raíz del repositorio:

```bash
python3 -m http.server 8081 --bind 127.0.0.1 --directory dashboard
```

Abrir:

```text
http://127.0.0.1:8081/public/
```

## Auditoría P0

Desde la raíz del repositorio:

```bash
python3 scripts/auditoria/validar_todo_p0.py
```

Resultado esperado:

- JSON dashboard: OK.
- CSV indicadores: OK.
- Indicadores P0: OK.
- Resultado general: OK.

## Documentos principales P0

- `docs/01-p0-diagnostico/resumen-ejecutivo-p0.md`
- `docs/01-p0-diagnostico/mvp-p0-checklist.md`
- `docs/01-p0-diagnostico/cierre-preliminar-p0.md`
- `docs/01-p0-diagnostico/diagnostico.md`
- `docs/01-p0-diagnostico/criterios-habilitacion-p1.md`

## Reglas de trabajo

- No cambiar el estado general a verde sin cierre formal de P0.
- No modificar P1 sin instrucción explícita.
- No autorizar compra de 500 pollonas.
- No autorizar construcción.
- No autorizar inversión mayor.
- No calcular VAN, TIR, ROI ni Payback hasta tener CAPEX completo y flujo proyectado.
- No hacer commit sin confirmación explícita.

## Estructura

```text
gallinero-2000/
├── README.md
├── dashboard/
├── docs/
├── datos/
├── scripts/
├── presupuestos/
├── normativa/
├── openclaw/
├── skills/
├── templates/
└── tests/
```

## Próximos pasos recomendados

1. Validar mercado real para 130–135 bandejas/semana.
2. Crear croquis del terreno 19 x 7 m.
3. Dimensionar agua.
4. Dimensionar energía solar.
5. Completar CAPEX con cotizaciones.
6. Preparar flujo proyectado para 648 aves.
7. Revisar legal/contable con apoyo externo.
8. Definir criterios cuantificados de no avance.
9. Re-evaluar si corresponde habilitar P1 preliminar.

# Gallinero modular para 2.000 gallinas ponedoras

Repositorio técnico y evolutivo para diagnosticar, diseñar, presupuestar, construir y evaluar un gallinero modular escalable en Chile.

## Estado vigente del proyecto

- Fase actual: P0 — Diagnóstico real.
- Estado general: amarillo.
- Nuevo escenario base: **500 aves totales**.
- Escenario anterior: **648 aves**, conservado como referencia histórica.
- P1 preliminar: no habilitado.
- P1 definitivo: bloqueado.
- Compra de aves/pollonas: bloqueada.
- Construcción: no autorizada.
- Inversión mayor: no autorizada.

## Replanteo de escala

Desde el replanteo P0, la decisión ya no se trabaja sobre el escenario anterior/referencial de 648 aves como objetivo central. El nuevo objetivo base es operar **500 aves totales**.

El escenario anterior de 648 aves correspondía a 148 aves actuales + hipótesis de 500 pollonas adicionales. Ese historial no se borra; queda documentado como referencia.

## Matriz de inversión por semáforo

| Color | Decisión |
|---|---|
| ROJO | No invertir. Solo diagnóstico, corrección de datos o levantamiento mínimo. |
| AMARILLO | Inversión menor y controlada solo para desbloqueo: cotizaciones, mediciones, visitas técnicas, correcciones menores, validación comercial, asesoría legal/contable y dimensionamiento agua/energía. |
| VERDE | Se puede evaluar inversión operativa o construcción solo con mercado, CAPEX, flujo y riesgos completos, bajo presupuesto aprobado. |

El estado actual no es verde. No se autoriza compra ni construcción.

## Escalamiento previsto

1. Operación actual: 148 aves.
2. Escenario base vigente: 500 aves totales.
3. Escenario comparativo futuro: 1.000 aves.
4. Escenario comparativo futuro: 2.000 aves.

## Brecha comercial base 500

Con postura referencial actual de 89,2%:

- Producción estimada 500 aves: 446 huevos/día.
- Bandejas estimadas 500 aves: 104,1 bandejas/semana.
- Venta actual: 28 bandejas/semana.
- Brecha estimada: 76,1 bandejas/semana.

Esta estimación es preliminar y no garantiza mercado.

## Galpones 500 / 1000 / 2000

Estimación financiera preliminar con cotización COT-GN-0035 y densidad aproximada de 7 gallinas/m²:

| Escenario | Superficie útil referencial | Costo |
|---|---:|---|
| 500 aves | 72 m² | $5.547.765 |
| 1000 aves | 144 m² | $11.095.530 proporcional |
| 2000 aves | 288 m² | $22.191.060 proporcional |

Hay costo referencial formal para 500 aves. No es autorización de construcción ni diseño constructivo definitivo.

## Documentos P0 principales

- `docs/01-p0-diagnostico/replanteo-escala-500-aves.md`
- `docs/01-p0-diagnostico/matriz-decision-inversion.md`
- `docs/01-p0-diagnostico/estimacion-galpones-500-1000-2000.md`
- `docs/01-p0-diagnostico/criterios-semaforo-inversion.md`
- `docs/01-p0-diagnostico/escenarios-escalamiento.md`
- `docs/01-p0-diagnostico/plan-desbloqueo-p1-preliminar.md`

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

Comando recomendado:

```bash
python3 scripts/auditoria/validar_todo_p0.py
```

## Restricción vigente

No se calcula VAN, TIR, ROI ni Payback definitivo. No se autoriza compra de pollonas, construcción ni inversión mayor mientras el semáforo no esté verde con evidencia completa.

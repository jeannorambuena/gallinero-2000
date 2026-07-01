# Replanteo de escala — nuevo escenario base 500 aves totales

## Motivo del replanteo

El diagnóstico P0 venía usando como escenario anterior/referencial de trabajo 648 aves, entendido como operación actual de 148 aves más una posible compra de 500 pollonas. Desde este replanteo, el escenario base objetivo cambia a **500 aves totales de operación**.

Esto reduce el salto inicial, obliga a recalcular brechas comerciales y evita confundir “comprar 500 pollonas” con “operar 500 aves totales”.

## Escenario anterior versus nuevo escenario base

| Concepto | Escenario anterior | Nuevo escenario base |
|---|---:|---:|
| Aves actuales | 148 | 148 |
| Objetivo usado para evaluar | 648 aves (anterior/referencial) | 500 aves totales |
| Interpretación | 148 actuales + 500 pollonas adicionales | operación total objetivo de 500 aves |
| Estado | referencia histórica | base decisional vigente |

El escenario de 648 aves **no se borra**. Queda documentado como escenario anterior/referencial para auditoría del proceso.

## Qué cambia

- La decisión comercial se calcula desde 28 bandejas/semana actuales hacia aproximadamente **104.1 bandejas/semana** para 500 aves.
- La brecha comercial baja desde 107 bandejas/semana referenciales para 648 aves a aproximadamente **76.1 bandejas/semana** para 500 aves.
- Agua, energía, CAPEX, flujo y galpón deben recalcularse con 500 aves como base.
- La compra de 500 pollonas deja de ser el supuesto directo del escenario base; queda pendiente definir estrategia de reposición/compra para llegar a 500 aves totales.
- P1 preliminar sigue no habilitado.

## Documentos y datos afectados

- resumen ejecutivo P0;
- criterios de habilitación P1;
- validación comercial;
- CAPEX preliminar;
- flujo de caja preliminar;
- plan de desbloqueo P1 preliminar;
- dashboard P0;
- auditoría P0;
- CSV de escenarios y matriz de inversión.

## Nueva escala base y comparativos

| Escenario | Aves | Uso |
|---|---:|---|
| Actual | 148 | operación real observada |
| Base | 500 | nueva base de decisión |
| Futuro | 1000 | comparativo futuro no habilitado |
| Futuro | 2000 | comparativo futuro no habilitado |

## Impacto en venta requerida

Fórmula preliminar:

```text
huevos_dia_estimados = aves x postura_promedio_actual
bandejas_semana_estimadas = huevos_dia_estimados x 7 / 30
```

Con postura actual referencial de 89.2%:

- 500 aves: 446 huevos/día estimados.
- 500 aves: 104.1 bandejas/semana estimadas.
- Venta actual: 28 bandejas/semana.
- Brecha estimada para 500 aves: 76.1 bandejas/semana.

Esta estimación no garantiza venta ni producción futura.

## Impacto en agua

El agua debe recalcularse para 500 aves. Como referencia histórica/referencial proporcional desde 150–200 L/día para 648 aves:

- 500 aves: 115.7–154.3 L/día estimados.

También debe contrastarse contra consumo actual de 34 L/día para 148 aves, equivalente a 0.23 L/ave/día.

## Impacto en galpón

Referencia preliminar de superficie útil cubierta:

```text
superficie_util = aves / 7 gallinas_m2_aprox
```

- 500 aves: 72 m² útiles según cotización COT-GN-0035.
- 1000 aves: 144 m² útiles como proporcional referencial.
- 2000 aves: 288 m² útiles como proporcional referencial.

La superficie total debe considerar bodega, pasillos, apoyo operativo, ventilación y diseño. No es diseño constructivo definitivo.

## Impacto en CAPEX

El CAPEX total para 500 aves queda pendiente. El dato anterior de 500 pollonas x $8.500 = $4.250.000 queda como antecedente histórico de precio unitario, pero ya no significa automáticamente que el escenario base requiera comprar 500 aves adicionales.

Debe definirse estrategia de compra/reposición para llegar a 500 aves totales.

## Impacto en flujo

El flujo base debe pasar de 648 referencial a 500 aves. No se calculan VAN, TIR, ROI ni Payback. El flujo proyectado sigue pendiente hasta completar ventas, costos, CAPEX, mano de obra, logística y formalización.

## Conclusión

Desde ahora la decisión P0/P1 se trabaja sobre **500 aves totales**. El escenario 648 queda como referencia histórica. No se habilita P1 preliminar, compra de pollonas, construcción ni inversión mayor hasta completar mercado, CAPEX, flujo, agua, energía, logística y legal/contable.

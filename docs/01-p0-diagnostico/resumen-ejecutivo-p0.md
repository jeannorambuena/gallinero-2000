# Resumen ejecutivo P0 — Proyecto Gallinero Nacho

## Propósito del resumen

Este resumen consolida el estado actual del P0 para que una persona no técnica pueda entender rápidamente qué está bien, qué falta, cuáles son los riesgos y por qué todavía no se debe comprar 500 pollonas ni iniciar una inversión mayor.

## Estado general

- Fase actual: P0 — Diagnóstico real.
- Avance P0 estimado: 80%.
- Semáforo general: amarillo.
- P1 preliminar: no habilitado.
- P1 definitivo: bloqueado.
- Compra de 500 pollonas: bloqueada.
- Construcción: no autorizada.
- Inversión mayor: no autorizada.

## Lo que está favorable

El proyecto tiene una buena base productiva actual:

- 148 gallinas actuales.
- Producción promedio de 132 huevos/día.
- Postura promedio de 89.2%.
- Mortalidad acumulada baja: 1.3%.

Esto muestra que la operación actual funciona productivamente. Sin embargo, producir bien hoy no significa que el salto a 648 aves esté validado.

## Principales riesgos

### Riesgo comercial

La venta actual es de 28 bandejas/semana. Para una operación de 648 aves se requerirían aproximadamente 135 bandejas/semana.

Eso deja una brecha de 107 bandejas/semana y exige crecer 4.82 veces. Este es uno de los principales bloqueos del proyecto.

### Riesgo financiero

La operación actual tiene:

- Ingreso mensual estimado: $736.667.
- Costos conocidos: $534.900.
- Margen sin mano de obra: $201.767.
- Mano de obra referencial: $182.000.
- Margen con mano de obra: $19.767.

El margen existe, pero queda muy ajustado al valorizar mano de obra.

### Riesgo de inversión

El único CAPEX conocido es la compra potencial de 500 pollonas por $4.250.000. El CAPEX total sigue pendiente, porque faltan galpón, bodega, agua, energía, equipamiento, logística, mano de obra e imprevistos.

### Riesgo de flujo proyectado

El flujo actual preliminar existe, pero el flujo proyectado para 648 aves sigue incompleto. VAN, TIR, ROI y Payback están bloqueados.

### Riesgos técnicos y operativos

- Agua: consumo actual 34 L/día; proyección 648 aves 150–200 L/día; solución conceptual estanque 1.000 L + bomba, pero falta dimensionamiento.
- Energía: se requieren 20 luces interiores, 2 exteriores, cámara 24/7 y respaldo deseado de 2 días; falta dimensionamiento.
- Construcción: galpón actual 27 m2, bodega actual 6 m2, terreno inmediato 133 m2; falta croquis, diseño, cubicación y cotización.
- Logística: camino rural de tierra, cerro, pendiente, camión grande complicado e invierno barroso.
- Legal/contable: falta revisar formalización, registro de ingresos/gastos, boletas/facturas, impuestos, trazabilidad y permisos aplicables.

## Decisiones bloqueadas

Siguen bloqueadas:

- Compra de 500 pollonas.
- P1 preliminar.
- P1 definitivo.
- Construcción.
- Inversión mayor.
- VAN, TIR, ROI y Payback definitivo.

## Por qué no se compra todavía

No se compra todavía porque el proyecto aún no demuestra condiciones suficientes para absorber 500 pollonas adicionales. Falta validar mercado, completar CAPEX, proyectar flujo de caja, dimensionar agua y energía, resolver logística y revisar temas legales/contables.

Comprar antes de cerrar estos puntos puede generar sobreproducción, falta de infraestructura, problemas de agua/energía, costos no considerados y una inversión difícil de recuperar.

## Qué falta para habilitar P1 preliminar

Para pensar en P1 preliminar falta, como mínimo:

- Validar mercado y canales de venta para acercarse a 130–135 bandejas/semana.
- Crear croquis del terreno inmediato 19 x 7 m.
- Definir alternativa constructiva preliminar.
- Dimensionar agua.
- Dimensionar energía solar.
- Evaluar logística de acceso, descarga y acopio.
- Completar CAPEX preliminar por categorías.
- Preparar flujo de caja proyectado.
- Revisar legal/contable.
- Definir criterios de no avance.

## Acciones recomendadas inmediatas

1. Validar clientes y canales reales para aumentar ventas.
2. Dibujar croquis del terreno y zonas de acceso/acopio.
3. Cotizar o dimensionar agua y energía solar.
4. Levantar CAPEX completo por categorías.
5. Preparar flujo proyectado para 648 aves.
6. Revisar formalización, impuestos, trazabilidad y venta a comercios.
7. Ejecutar auditoría de datos P0:

```bash
python3 scripts/auditoria/validar_todo_p0.py
```

## Conclusión ejecutiva

El proyecto tiene buena base productiva. El salto a 648 aves no está validado todavía. La compra de 500 pollonas sigue bloqueada. P1 preliminar aún no está habilitado. El foco siguiente debe ser validar mercado, croquis, CAPEX completo, flujo proyectado, agua, energía, logística y legal/contable.

# P44 — Estimación proporcional 500 y preguntas finales

## Base

- Rama: `dashboard/v2-ejecutivo-500`
- Commit base P43: `26b3390b58c7dc2d7b01f0c97a8c028ad29ae706`
- Estado: **amarillo / no invertir todavía**

## Escenario proporcional preliminar 500 aves

Factor de escala: **500 / 148 = 3,378378**.

### Densidad

- Galpón: **72 m²**.
- Densidad: **500 / 72 = 6,94 aves/m²**, mostrar como aprox. **7 aves/m²**.

### Alimento proyectado

- Consumo actual: **124 g/gallina/día**.
- 500 aves x 124 g/día = **62 kg/día**.
- 62 kg/día x 30 = **1.860 kg/mes**.
- 1.860 / 25 = **74,4 sacos/mes**.
- Redondeo operativo: **75 sacos/mes**.
- Precio saco: **$12.950**.
- Costo alimento proyectado: **$971.250/mes**.

### Envases meta

- Meta: **100 bandejas/semana**.
- Costo envase: **$105/bandeja**.
- Costo semanal: **$10.500**.
- Costo mensual: **$45.500**.

### Viruta proyectada

- Actual: **$10.000/mes** para 148 aves.
- Proyección: **$10.000 x 500 / 148 = $33.784**.
- Redondeo: **$34.000/mes**.

### Agua estimada

- Actual: **34 L/día**.
- Proporcional: **115 L/día mínimo**.
- Rango mantenido: **115 a 154 L/día**.

### OPEX mínimo proporcional preliminar

- Alimento: **$971.250**.
- Envases: **$45.500**.
- Viruta: **$34.000**.
- Bencina/reparto base: **$10.000**.
- Total: **$1.060.750/mes**.

Texto obligatorio:

> OPEX mínimo proporcional preliminar: incluye alimento, envases, viruta y bencina base. No equivale a OPEX total final porque falta sanidad de escala, mantenciones, mano de obra, mortalidad, reposición, agua definitiva e imprevistos.

## Requerimientos de equipamiento para cotizar

- Comederos: **40-50 m lineales** o **22-24 unidades**.
- Bebederos: **60 nipples** aprox.
- Nidos/ponederos: **72 nidos** individuales o **5 m² comunitario**.
- Perchas: **75 m lineales**.
- Bodega alimento: **19 sacos/semana** o **38 sacos/2 semanas**.
- Agua/bomba: validar **115 a 154 L/día**; cotizar bomba si no está expresamente incluida/lista en sistema solar.
- Panel solar: no generar CAPEX adicional; P43 lo dejó como paquete completo informado.

## Preguntas finales reducidas para Nacho

1. ¿Confirmas que para el análisis usamos estos precios: segunda $5.000, primera $6.000 y extra $7.000?
2. Para 100 bandejas/semana, ¿los almacenes pagarían esos mismos precios o pedirían descuento?
3. ¿Las 100 bandejas semanales se venderían al contado o habría venta fiada/semanal/mensual?
4. Para 500 gallinas, usaremos 75 sacos de alimento al mes. ¿Te parece razonable o sería más/menos?
5. Para 500 gallinas, usaremos $34.000 mensuales de viruta. ¿Te parece razonable o sería más?
6. Para 500 gallinas, falta cotizar comederos, bebederos, ponederos, perchas, bomba, mallas interiores y bodega/ampliación. ¿Tienes precio o cotización de alguno?
7. ¿El estanque actual alcanza para 115 a 154 litros diarios?
8. El panel solar de $300.000, ¿está listo para operar bomba, luces y cámaras sin comprar nada adicional?
9. Con 500 gallinas, ¿la operación diaria tendrá costo mensual de mano de obra o será trabajo familiar sin sueldo al inicio?
10. ¿Comprarías las 352 pollonas faltantes de una vez o por etapas?

## Archivos nuevos

- `dashboard/data/escenario-proporcional-500.json`
- `dashboard/data/requerimientos-equipamiento-avicola.json`

## Decisión

P44 no desbloquea inversión. El proyecto sigue amarillo hasta cerrar CAPEX total, OPEX total final, capital de trabajo, formalización, logística, agua/bomba, mano de obra y flujo financiero completo.

# Gallinero modular para 2.000 gallinas ponedoras

Repositorio técnico y evolutivo para diagnosticar, diseñar, presupuestar, construir y evaluar un gallinero modular escalable en Chile.

## Escalamiento previsto

1. Situación actual: aproximadamente 300 gallinas.
2. Etapa inicial: capacidad para 500 gallinas.
3. Segunda etapa: capacidad total para 1.000 gallinas.
4. Etapa final: capacidad total para 2.000 gallinas.

## Estado del proyecto

| Fase | Estado | Objetivo |
|---|---|---|
| P0 | En preparación | Diagnóstico real de la operación actual |
| P1 | Pendiente | Diseño del módulo para 500 gallinas |
| P2 | Pendiente | Presupuesto y planificación definitiva |
| P3 | Pendiente | Construcción y habilitación |
| P4 | Pendiente | Operación piloto y evaluación |
| P5 | Pendiente | Ampliación a 1.000 gallinas |
| P6 | Pendiente | Ampliación a 2.000 gallinas |

## Prioridad actual

Completar el P0 antes de diseñar o presupuestar definitivamente.

Se necesitan datos verificables de aves, producción, consumo, gastos, ventas, mortalidad, sanidad, infraestructura existente, terreno, agua, electricidad y problemas operacionales.

## Jerarquía de información

1. Dato real: medición, factura, boleta, registro o declaración directa.
2. Fuente oficial: normativa o documento de autoridad competente.
3. Referencia técnica: manual, estudio o proyecto comparable.
4. Precio comprobado: cotización con proveedor y fecha.
5. Estimación: supuesto calculado pendiente de validación.

Una estimación nunca debe presentarse como dato real.

## Reglas

- No inventar precios, medidas, consumos o rendimientos.
- No sobrescribir datos originales.
- Registrar fuente, fecha, unidad y nivel de confiabilidad.
- Mantener separados datos reales, referencias, precios y resultados calculados.
- No avanzar de fase sin cerrar sus entregables mínimos.
- Registrar cambios importantes con Git.
- Mantener actualizados `README.md`, `ROADMAP.md` y `CHANGELOG.md`.
- Exigir revisión humana para decisiones estructurales, sanitarias, veterinarias, eléctricas, económicas o normativas.

## Estructura

```text
gallinero-2000/
├── README.md
├── ROADMAP.md
├── CHANGELOG.md
├── config/
├── docs/
├── datos/
│   ├── reales/
│   ├── referencias/
│   ├── precios/
│   └── procesados/
├── freecad/
├── scripts/
├── presupuestos/
├── normativa/
├── openclaw/
├── skills/
├── templates/
└── tests/
```

## Próximas acciones

1. Completar `templates/formularios/levantamiento-p0.md`.
2. Registrar producción y consumo reales.
3. Incorporar el proyecto anterior en papel.
4. Medir gallinero actual y terreno futuro.
5. Incorporar fotografías, boletas y registros.
6. Calcular indicadores del P0.
7. Emitir diagnóstico y decisión de avance a P1.

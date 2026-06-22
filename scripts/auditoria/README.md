# Auditoría P0

Scripts de control de calidad para validar la estructura mínima del dashboard P0, los CSV procesados, las plantillas de entrada y la coherencia crítica del replanteo a 500 aves.

Usan solo Python estándar. No requieren pandas, numpy ni dependencias externas.

## Scripts

### `validar_json_dashboard.py`

Valida JSON locales del dashboard, incluyendo:

- `dashboard/data/replanteo-escala.json`
- `dashboard/data/matriz-decision-inversion.json`
- `dashboard/data/estimacion-galpones.json`
- datos ejecutivos, CAPEX, flujo, validación comercial, semáforo y criterios P1.

```bash
python3 scripts/auditoria/validar_json_dashboard.py
```

### `validar_csv_indicadores.py`

Valida CSV procesados y plantillas de entrada, incluyendo escenarios, estimación de galpones, matriz de inversión y flujo 500.

```bash
python3 scripts/auditoria/validar_csv_indicadores.py
```

### `validar_indicadores_p0.py`

Valida coherencia básica:

- escenario base actual = 500 aves;
- 648 aves = referencia histórica;
- P1 preliminar no habilitado;
- compra de aves no autorizada;
- inversión mayor no autorizada;
- galpones 500/1000/2000 presentes;
- costo m2 y costo total de galpón pendientes.

```bash
python3 scripts/auditoria/validar_indicadores_p0.py
```

### `validar_todo_p0.py`

Comando recomendado:

```bash
python3 scripts/auditoria/validar_todo_p0.py
```

## Resultado esperado

- Si todo está correcto, los scripts imprimen `OK` y terminan con exit code `0`.
- Si detectan errores, imprimen `ERROR` y terminan con exit code `1`.

# Auditoría P0

Scripts de control de calidad para validar la estructura mínima del dashboard P0, los CSV procesados, las plantillas de entrada para desbloqueo P1 preliminar y la coherencia de indicadores críticos del Proyecto Gallinero Nacho.

Usan solo Python estándar. No requieren pandas, numpy ni dependencias externas.

## Scripts

### `validar_json_dashboard.py`

Valida que existan y sean JSON válidos los archivos de `dashboard/data/` usados por el dashboard P0. También revisa campos mínimos y listas principales no vacías.

Ejecutar desde la raíz de la repo:

```bash
python3 scripts/auditoria/validar_json_dashboard.py
```

### `validar_csv_indicadores.py`

Valida que existan y sean CSV legibles los archivos procesados de indicadores P0 y las plantillas de entrada del paquete de desbloqueo P1 preliminar. Revisa encabezado, filas y que no estén vacíos.

```bash
python3 scripts/auditoria/validar_csv_indicadores.py
```

### `validar_indicadores_p0.py`

Valida coherencia básica de indicadores críticos productivos, comerciales, financieros, CAPEX y criterios P1.

```bash
python3 scripts/auditoria/validar_indicadores_p0.py
```

### `validar_todo_p0.py`

Ejecuta todas las validaciones anteriores y entrega resumen general.

Comando recomendado:

```bash
python3 scripts/auditoria/validar_todo_p0.py
```

## Resultado esperado

- Si todo está correcto, los scripts imprimen `OK` y terminan con exit code `0`.
- Si detectan errores, imprimen `ERROR` y terminan con exit code `1`.

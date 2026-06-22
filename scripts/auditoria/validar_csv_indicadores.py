#!/usr/bin/env python3
"""Valida existencia y lectura básica de CSV de indicadores P0 y plantillas de entrada."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path.cwd()

CSV_INDICADORES = [
    "datos/procesados/indicadores/p0-indicadores-productivos.csv",
    "datos/procesados/indicadores/p0-indicadores-comerciales.csv",
    "datos/procesados/indicadores/p0-indicadores-financieros-basicos.csv",
    "datos/procesados/indicadores/p0-capex-preliminar.csv",
    "datos/procesados/indicadores/p0-flujo-caja-preliminar.csv",
]

CSV_ENTRADA = [
    "datos/entrada/validacion-comercial/clientes-actuales.csv",
    "datos/entrada/validacion-comercial/clientes-potenciales.csv",
    "datos/entrada/validacion-comercial/canales-venta.csv",
    "datos/entrada/terreno/croquis-mediciones.csv",
    "datos/entrada/agua/dimensionamiento-agua.csv",
    "datos/entrada/energia/dimensionamiento-solar.csv",
    "datos/entrada/capex/cotizaciones-capex.csv",
    "datos/entrada/flujo/flujo-proyectado-648.csv",
    "datos/entrada/legal-contable/checklist-legal-contable.csv",
    "datos/entrada/logistica/checklist-logistica.csv",
]


def validate_csv(rel_path: str, require_rows: bool = True) -> list[str]:
    errors: list[str] = []
    path = ROOT / rel_path

    if not path.exists():
        return [f"no existe: {rel_path}"]
    if path.stat().st_size == 0:
        return [f"archivo vacío: {rel_path}"]

    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                return [f"sin encabezado: {rel_path}"]
            if any(not (name or "").strip() for name in reader.fieldnames):
                errors.append(f"encabezado con columna vacía: {rel_path}")
            rows = list(reader)
    except csv.Error as exc:
        return [f"CSV inválido en {rel_path}: {exc}"]
    except UnicodeDecodeError as exc:
        return [f"encoding inválido en {rel_path}: {exc}"]

    if require_rows and not rows:
        errors.append(f"sin filas de datos: {rel_path}")

    return errors


def main() -> int:
    indicator_errors: list[str] = []
    input_errors: list[str] = []

    for rel_path in CSV_INDICADORES:
        indicator_errors.extend(validate_csv(rel_path, require_rows=True))

    for rel_path in CSV_ENTRADA:
        input_errors.extend(validate_csv(rel_path, require_rows=True))

    if indicator_errors or input_errors:
        print("ERROR CSV indicadores/entrada")
        for error in indicator_errors:
            print(f"- indicadores: {error}")
        for error in input_errors:
            print(f"- entrada: {error}")
        return 1

    print(f"OK CSV indicadores: {len(CSV_INDICADORES)} archivos válidos")
    print(f"OK CSV entrada: {len(CSV_ENTRADA)} archivos válidos")
    return 0


if __name__ == "__main__":
    sys.exit(main())

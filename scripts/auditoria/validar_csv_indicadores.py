#!/usr/bin/env python3
"""Valida existencia y lectura básica de CSV de indicadores P0."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path.cwd()

CSV_FILES = [
    "datos/procesados/indicadores/p0-indicadores-productivos.csv",
    "datos/procesados/indicadores/p0-indicadores-comerciales.csv",
    "datos/procesados/indicadores/p0-indicadores-financieros-basicos.csv",
    "datos/procesados/indicadores/p0-capex-preliminar.csv",
    "datos/procesados/indicadores/p0-flujo-caja-preliminar.csv",
]


def validate_csv(rel_path: str) -> list[str]:
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

    if not rows:
        errors.append(f"sin filas de datos: {rel_path}")

    return errors


def main() -> int:
    errors: list[str] = []
    for rel_path in CSV_FILES:
        errors.extend(validate_csv(rel_path))

    if errors:
        print("ERROR CSV indicadores")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"OK CSV indicadores: {len(CSV_FILES)} archivos válidos")
    return 0


if __name__ == "__main__":
    sys.exit(main())

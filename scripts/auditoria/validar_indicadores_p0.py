#!/usr/bin/env python3
"""Valida coherencia básica de indicadores críticos P0."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path.cwd()


def load_json(rel_path: str) -> dict[str, Any]:
    path = ROOT / rel_path
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{rel_path}: raíz no es objeto")
    return data


def index_indicators(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    indicators = data.get("indicadores", [])
    if not isinstance(indicators, list):
        raise ValueError("indicadores no es lista")
    return {item.get("indicador"): item for item in indicators if isinstance(item, dict)}


def value(index: dict[str, dict[str, Any]], key: str) -> Any:
    if key not in index:
        raise KeyError(f"falta indicador: {key}")
    return index[key].get("valor")


def assert_equal(errors: list[str], label: str, actual: Any, expected: Any) -> None:
    if actual != expected:
        errors.append(f"{label}: esperado {expected!r}, encontrado {actual!r}")


def assert_close(errors: list[str], label: str, actual: Any, expected: float, tolerance: float = 0.02) -> None:
    try:
        number = float(actual)
    except (TypeError, ValueError):
        errors.append(f"{label}: valor no numérico {actual!r}")
        return
    if math.fabs(number - expected) > tolerance:
        errors.append(f"{label}: esperado cercano a {expected}, encontrado {number}")


def main() -> int:
    errors: list[str] = []

    try:
        productivos = index_indicators(load_json("dashboard/data/indicadores-productivos.json"))
        comerciales = index_indicators(load_json("dashboard/data/indicadores-comerciales.json"))
        flujo = load_json("dashboard/data/flujo-caja-preliminar.json")
        capex = load_json("dashboard/data/capex-preliminar.json")
        criterios = load_json("dashboard/data/criterios-p1.json")
    except Exception as exc:  # noqa: BLE001 - auditoría debe capturar y reportar claro
        print("ERROR Indicadores P0")
        print(f"- no se pudieron cargar datos: {exc}")
        return 1

    try:
        # Productivo
        assert_equal(errors, "gallinas actuales", value(productivos, "gallinas_actuales"), 148)
        assert_equal(errors, "producción promedio", value(productivos, "produccion_promedio_huevos_dia"), 132)
        assert_close(errors, "postura promedio", value(productivos, "postura_promedio_porcentaje"), 89.2, 0.05)

        # Comercial
        assert_equal(errors, "venta actual", value(comerciales, "venta_actual_bandejas_semana"), 28)
        assert_equal(errors, "venta requerida 648", value(comerciales, "bandejas_semana_proyectadas_648_aves"), 135)
        assert_equal(errors, "brecha comercial", value(comerciales, "brecha_bandejas_semana_para_648"), 107)
        assert_close(errors, "crecimiento requerido", value(comerciales, "crecimiento_requerido_veces"), 4.82, 0.01)

        # Finanzas / flujo
        assert_equal(errors, "ingreso mensual actual", flujo.get("ingresos_actuales", {}).get("ingreso_mensual_estimado_clp"), 736667)
        assert_equal(errors, "costos conocidos", flujo.get("costos_actuales", {}).get("total_costos_conocidos_clp"), 534900)
        assert_equal(errors, "margen sin mano de obra", flujo.get("margenes_actuales", {}).get("margen_sin_mano_obra_clp"), 201767)
        assert_equal(errors, "mano de obra referencial", flujo.get("mano_obra_referencial", {}).get("monto_clp"), 182000)
        assert_equal(errors, "margen con mano de obra", flujo.get("margenes_actuales", {}).get("margen_con_mano_obra_clp"), 19767)

        # CAPEX
        assert_equal(errors, "CAPEX conocido pollonas", capex.get("capex_conocido", {}).get("pollonas", {}).get("monto_clp"), 4250000)
        capex_total = capex.get("capex_pendiente", {}).get("monto_total_pendiente")
        if capex_total not in (None, "pendiente"):
            errors.append(f"CAPEX total pendiente: esperado None o 'pendiente', encontrado {capex_total!r}")

        # Criterios P1
        assert_equal(errors, "estado_p1_preliminar", criterios.get("estado_p1_preliminar"), "no habilitado")
        assert_equal(errors, "estado_p1_definitivo", criterios.get("estado_p1_definitivo"), "bloqueado")
        assert_equal(errors, "compra_pollonas", criterios.get("compra_pollonas"), "bloqueada")
        assert_equal(errors, "decision_actual.compra_500_pollonas", criterios.get("decision_actual", {}).get("compra_500_pollonas"), False)
    except Exception as exc:  # noqa: BLE001
        errors.append(str(exc))

    if errors:
        print("ERROR Indicadores P0")
        for error in errors:
            print(f"- {error}")
        return 1

    print("OK Indicadores P0: coherencia básica validada")
    return 0


if __name__ == "__main__":
    sys.exit(main())

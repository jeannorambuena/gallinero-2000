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


def flatten_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        strings: list[str] = []
        for nested in value.values():
            strings.extend(flatten_strings(nested))
        return strings
    if isinstance(value, list):
        strings = []
        for nested in value:
            strings.extend(flatten_strings(nested))
        return strings
    return []


def is_648_reference_allowed(text: str) -> bool:
    lowered = text.lower()
    allowed_markers = (
        "histórico",
        "histórica",
        "historico",
        "historica",
        "referencial",
        "anterior",
        "escenario anterior",
        "trazabilidad",
    )
    return "648 aves" not in lowered or any(marker in lowered for marker in allowed_markers)


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
        comerciales_data = load_json("dashboard/data/indicadores-comerciales.json")
        comerciales = index_indicators(comerciales_data)
        flujo = load_json("dashboard/data/flujo-caja-preliminar.json")
        capex = load_json("dashboard/data/capex-preliminar.json")
        criterios = load_json("dashboard/data/criterios-p1.json")
        replanteo = load_json("dashboard/data/replanteo-escala.json")
        matriz = load_json("dashboard/data/matriz-decision-inversion.json")
        galpones = load_json("dashboard/data/estimacion-galpones.json")
        validacion = load_json("dashboard/data/validacion-comercial.json")
        estado = load_json("dashboard/data/estado-proyecto.json")
        alertas = load_json("dashboard/data/alertas-p0.json")
        datos_faltantes = load_json("dashboard/data/datos-faltantes.json")
        subproyectos = load_json("dashboard/data/subproyectos-criticos.json")
    except Exception as exc:  # noqa: BLE001 - auditoría debe capturar y reportar claro
        print("ERROR Indicadores P0")
        print(f"- no se pudieron cargar datos: {exc}")
        return 1

    try:
        # Productivo actual
        assert_equal(errors, "gallinas actuales", value(productivos, "gallinas_actuales"), 148)
        assert_equal(errors, "producción promedio", value(productivos, "produccion_promedio_huevos_dia"), 132)
        assert_close(errors, "postura promedio", value(productivos, "postura_promedio_porcentaje"), 89.2, 0.05)

        # Replanteo base 500
        assert_equal(errors, "replanteo.escenario_base_actual", replanteo.get("escenario_base_actual", {}).get("aves"), 500)
        assert_equal(errors, "replanteo.escenario_anterior", replanteo.get("escenario_anterior", {}).get("aves"), 648)
        assert_equal(errors, "estado.escenario_base_actual", estado.get("escenario_base_actual"), 500)
        assert_equal(errors, "criterios.escenario_base_actual", criterios.get("escenario_base_actual"), 500)

        # Comercial base 500
        assert_equal(errors, "venta actual", validacion.get("venta_actual_bandejas_semana"), 28)
        assert_equal(errors, "indicador venta actual", value(comerciales, "venta_actual_bandejas_semana"), 28)
        assert_close(errors, "venta requerida 500", validacion.get("venta_requerida_500_bandejas_semana"), 104.1, 0.05)
        assert_close(errors, "indicador venta requerida 500", value(comerciales, "bandejas_semana_estimadas_500_aves"), 104.1, 0.05)
        assert_equal(errors, "meta comercial base 500", validacion.get("meta_comercial_base_bandejas_semana"), 100)
        assert_close(errors, "diferencia técnica producción/meta", validacion.get("diferencia_tecnica_produccion_meta_bandejas_semana"), 4.1, 0.05)
        assert_close(errors, "indicador diferencia técnica", value(comerciales, "diferencia_tecnica_produccion_meta_bandejas_semana"), 4.1, 0.05)
        assert_close(errors, "diferencia técnica 500 P43", validacion.get("diferencia_tecnica_bandejas_semana"), 4.1, 0.05)
        assert_close(errors, "indicador diferencia técnica 500 P43", value(comerciales, "diferencia_tecnica_bandejas_semana_para_500_p43"), 4.1, 0.05)
        assert_equal(
            errors,
            "indicador 648 histórico/referencial",
            comerciales.get("bandejas_semana_proyectadas_648_aves", {}).get("estado"),
            "historico/referencial",
        )

        # Finanzas / flujo actual y base 500 — P42
        distribucion = flujo.get("ingresos_actuales", {}).get("distribucion_semanal_por_categoria", {})
        assert_equal(errors, "bandejas segunda", distribucion.get("segunda"), 6)
        assert_equal(errors, "bandejas primera", distribucion.get("primera"), 13)
        assert_equal(errors, "bandejas extra", distribucion.get("extra"), 9)
        assert_equal(errors, "ingreso semanal actual", flujo.get("ingresos_actuales", {}).get("ingreso_semanal_actual_clp"), 171000)
        assert_equal(errors, "ingreso mensual actual", flujo.get("ingresos_actuales", {}).get("ingreso_mensual_estimado_clp"), 741000)
        assert_equal(errors, "precio promedio bandeja", flujo.get("ingresos_actuales", {}).get("precio_promedio_real_bandeja"), 6107)
        assert_equal(errors, "costos conocidos", flujo.get("costos_actuales", {}).get("total_costos_conocidos_clp"), 343640)
        assert_equal(errors, "envases actuales mes", flujo.get("costos_actuales", {}).get("envases_actual_mensual_aprox_clp"), 12740)
        assert_equal(errors, "viruta mensual", flujo.get("costos_actuales", {}).get("cama_viruta_mensual_clp"), 10000)
        assert_equal(errors, "bencina reparto mensual", flujo.get("costos_actuales", {}).get("bencina_reparto_mensual_clp"), 10000)
        assert_equal(errors, "medicamentos adicionales", flujo.get("costos_actuales", {}).get("medicamentos_limpieza_adicional_mensual_clp"), 0)
        assert_equal(errors, "margen sin mano de obra", flujo.get("margenes_actuales", {}).get("margen_sin_mano_obra_clp"), 397360)
        assert_equal(errors, "mano de obra referencial", flujo.get("mano_obra_referencial", {}).get("monto_clp"), 182000)
        assert_equal(errors, "margen con mano de obra", flujo.get("margenes_actuales", {}).get("margen_con_mano_obra_clp"), 215360)
        assert_equal(errors, "flujo escenario 500", flujo.get("escenario_500", {}).get("aves"), 500)
        assert_equal(errors, "flujo escenario 648 histórico", flujo.get("escenario_648", {}).get("aves"), 648)

        # CAPEX — P42
        assert_equal(errors, "pollonas faltantes", capex.get("capex_conocido", {}).get("pollonas", {}).get("cantidad_faltante"), 352)
        assert_equal(errors, "precio vigente pollona", capex.get("capex_conocido", {}).get("pollonas", {}).get("precio_vigente_unitario_clp"), 12000)
        assert_equal(errors, "CAPEX pollonas faltantes", capex.get("capex_conocido", {}).get("pollonas", {}).get("monto_clp"), 4224000)
        assert_equal(errors, "incremento CAPEX pollonas", capex.get("capex_conocido", {}).get("pollonas", {}).get("incremento_por_actualizacion_precio_clp"), 1232000)
        assert_equal(errors, "subtotal galpón + pollonas", capex.get("capex_conocido", {}).get("monto_total_conocido_clp"), 9771765)
        assert_equal(errors, "panel solar comprado", capex.get("capex_conocido", {}).get("panel_solar", {}).get("monto_clp"), 300000)
        assert_equal(errors, "CAPEX equipamiento avícola estado", capex.get("capex_pendiente", {}).get("equipamiento_avicola_estado"), "pendiente_cotizacion")
        equip_path = ROOT / "dashboard/data/capex-equipamiento-avicola.json"
        try:
            equipamiento = load_json("dashboard/data/capex-equipamiento-avicola.json")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"CAPEX equipamiento avícola: no se pudo cargar: {exc}")
            equipamiento = {}
        assert_equal(errors, "CAPEX equipamiento objetivo aves", equipamiento.get("objetivo_aves"), 500)
        if len(equipamiento.get("items", [])) < 8:
            errors.append("CAPEX equipamiento avícola: debe tener al menos 8 ítems pendientes")
        capex_total = capex.get("capex_pendiente", {}).get("monto_total_pendiente")
        if capex_total not in (None, "pendiente"):
            errors.append(f"CAPEX total pendiente: esperado None o 'pendiente', encontrado {capex_total!r}")

        # Criterios P1 / inversión
        assert_equal(errors, "estado_p1_preliminar", criterios.get("estado_p1_preliminar"), "no habilitado")
        assert_equal(errors, "estado.p1_preliminar_habilitado", estado.get("p1_preliminar_habilitado"), False)
        assert_equal(errors, "decision_actual.p1_preliminar", criterios.get("decision_actual", {}).get("p1_preliminar"), False)
        assert_equal(errors, "estado_p1_definitivo", criterios.get("estado_p1_definitivo"), "bloqueado")
        assert_equal(errors, "compra_pollonas", criterios.get("compra_pollonas"), "bloqueada")
        assert_equal(errors, "decision_actual.compra_aves", criterios.get("decision_actual", {}).get("compra_aves"), False)
        assert_equal(errors, "decision_actual.construccion", criterios.get("decision_actual", {}).get("construccion"), False)
        assert_equal(errors, "decision_actual.inversion_mayor", criterios.get("decision_actual", {}).get("inversion_mayor"), False)
        assert_equal(errors, "matriz.compra_aves_autorizada", matriz.get("compra_aves_autorizada"), False)
        assert_equal(errors, "matriz.construccion_autorizada", matriz.get("construccion_autorizada"), False)
        assert_equal(errors, "matriz.inversion_mayor_autorizada", matriz.get("inversion_mayor_autorizada"), False)
        assert_equal(errors, "estado.compra_aves_autorizada", estado.get("compra_aves_autorizada"), False)
        assert_equal(errors, "estado.construccion_autorizada", estado.get("construccion_autorizada"), False)
        assert_equal(errors, "estado.inversion_mayor_autorizada", estado.get("inversion_mayor_autorizada"), False)

        # Galpones: COT-GN-0035 ya está integrada como base referencial formal; no autoriza construcción.
        escenarios = galpones.get("escenarios", [])
        escenarios_por_aves = {item.get("aves"): item for item in escenarios if isinstance(item, dict)}
        aves_galpon = set(escenarios_por_aves)
        if aves_galpon != {500, 1000, 2000}:
            errors.append(f"estimación galpones: esperado {{500, 1000, 2000}}, encontrado {aves_galpon!r}")
        assert_equal(errors, "galpón 500 superficie", escenarios_por_aves.get(500, {}).get("superficie_util_m2"), 72)
        assert_equal(errors, "galpón 500 costo_m2", escenarios_por_aves.get(500, {}).get("costo_m2"), 77052)
        assert_equal(errors, "galpón 500 costo_total", escenarios_por_aves.get(500, {}).get("costo_total"), 5547765)
        assert_equal(errors, "galpón 1000 costo_total", escenarios_por_aves.get(1000, {}).get("costo_total"), 11095530)
        assert_equal(errors, "galpón 2000 costo_total", escenarios_por_aves.get(2000, {}).get("costo_total"), 22191060)
        if "no autoriza" not in str(escenarios_por_aves.get(500, {}).get("estado", "")).lower():
            errors.append("galpón 500: debe mantener advertencia de no autorización de construcción")
        advertencia_galpon = str(galpones.get("capex_referencial_formal", {}).get("advertencia", "")).lower()
        if "autorización" not in advertencia_galpon or "no" not in advertencia_galpon:
            errors.append("galpón COT-GN-0035: debe mantener advertencia de no autorización")

        # Dashboard crítico: 648 aves solo puede quedar como histórico/referencial/anterior/trazabilidad.
        critical_dashboard = {
            "dashboard/data/alertas-p0.json": alertas,
            "dashboard/data/datos-faltantes.json": datos_faltantes,
            "dashboard/data/subproyectos-criticos.json": subproyectos,
            "dashboard/data/indicadores-comerciales.json": comerciales_data,
            "dashboard/data/validacion-comercial.json": validacion,
            "dashboard/data/replanteo-escala.json": replanteo,
        }
        for rel_path, payload in critical_dashboard.items():
            for entry in flatten_strings(payload):
                if not is_648_reference_allowed(entry):
                    errors.append(f"{rel_path}: referencia 648 aves sin marca histórica/referencial: {entry!r}")
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

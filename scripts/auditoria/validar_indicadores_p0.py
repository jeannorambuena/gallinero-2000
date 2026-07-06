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
        escenario_proporcional = load_json("dashboard/data/escenario-proporcional-500.json")
        requerimientos_equipamiento = load_json("dashboard/data/requerimientos-equipamiento-avicola.json")
        finanzas_data = load_json("dashboard/data/finanzas-preliminares.json")
        finanzas = index_indicators(finanzas_data)
        capex_total_500 = load_json("dashboard/data/capex-total-referencial-500.json")
        opex_500 = load_json("dashboard/data/opex-proyectado-500.json")
        ingresos_500 = load_json("dashboard/data/ingresos-proyectados-500.json")
        flujo_500 = load_json("dashboard/data/flujo-financiero-preliminar-500.json")
        estrategia_pollonas = load_json("dashboard/data/estrategia-compra-pollonas.json")
        decision_p47 = load_json("dashboard/data/decision-ejecutiva-p47.json")
        alternativas_p47 = load_json("dashboard/data/alternativas-crecimiento-p47.json")
        plan_p47 = load_json("dashboard/data/plan-implementacion-6-meses.json")
        reglas_p47 = load_json("dashboard/data/reglas-decision-semaforo-p47.json")
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
        assert_equal(errors, "mano de obra referencial P45-P46", flujo.get("mano_obra_referencial", {}).get("monto_clp"), 600000)
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
        assert_equal(errors, "P44 objetivo proporcional", escenario_proporcional.get("objetivo_aves"), 500)
        assert_equal(errors, "P44 base actual aves", escenario_proporcional.get("base_actual_aves"), 148)
        assert_close(errors, "P44 factor escala", escenario_proporcional.get("factor_escala"), 3.378378, 0.0005)
        assert_close(errors, "P44 densidad aves/m2", escenario_proporcional.get("densidad", {}).get("aves_m2"), 6.94, 0.02)
        assert_equal(errors, "P44 alimento sacos", escenario_proporcional.get("alimento", {}).get("proyeccion_sacos_mes_redondeada"), 75)
        assert_equal(errors, "P44 alimento costo", escenario_proporcional.get("alimento", {}).get("costo_proyectado_clp_mes"), 971250)
        assert_equal(errors, "P44 envases meta", escenario_proporcional.get("envases_meta", {}).get("costo_mensual_clp"), 45500)
        assert_equal(errors, "P44 viruta proyectada", escenario_proporcional.get("viruta", {}).get("proyeccion_redondeada_clp_mes"), 34000)
        assert_equal(errors, "P44 OPEX mínimo proporcional", escenario_proporcional.get("opex_minimo_proporcional", {}).get("total_clp_mes"), 1060750)
        assert_equal(errors, "indicador P44 alimento sacos", value(finanzas, "alimento_proyectado_500_sacos_mes"), 75)
        assert_equal(errors, "indicador P44 alimento costo", value(finanzas, "alimento_proyectado_500_clp_mes"), 971250)
        assert_equal(errors, "indicador P44 envases", value(finanzas, "envases_meta_100_bandejas_clp_mes"), 45500)
        assert_equal(errors, "indicador P44 viruta", value(finanzas, "viruta_proyectada_500_clp_mes"), 34000)
        assert_equal(errors, "indicador P44 OPEX mínimo", value(finanzas, "opex_minimo_proporcional_500_clp"), 1060750)
        req_resumen = requerimientos_equipamiento.get("resumen", {})
        for label, expected in {
            "comederos": "40-50 m lineales o 22-24 unidades",
            "bebederos": "60 nipples aprox.",
            "nidos": "72 nidos individuales o 5 m² comunitario",
            "perchas": "75 m lineales",
        }.items():
            assert_equal(errors, f"P44 requerimiento {label}", req_resumen.get(label), expected)
        capex_total = capex.get("capex_pendiente", {}).get("monto_total_pendiente")
        if capex_total not in (None, "pendiente"):
            errors.append(f"CAPEX total pendiente: esperado None o 'pendiente', encontrado {capex_total!r}")

        # P45-P46: CAPEX/OPEX/flujo referencial 500
        assert_equal(errors, "P45 CAPEX equipamiento bajo", capex_total_500.get("equipamiento_escenarios", {}).get("bajo", {}).get("total_clp"), 1723000)
        assert_equal(errors, "P45 CAPEX equipamiento base", capex_total_500.get("equipamiento_escenarios", {}).get("base", {}).get("total_clp"), 3572000)
        assert_equal(errors, "P45 CAPEX equipamiento alto", capex_total_500.get("equipamiento_escenarios", {}).get("alto", {}).get("total_clp"), 7010000)
        assert_equal(errors, "P45 CAPEX total bajo", capex_total_500.get("capex_total_referencial", {}).get("bajo", {}).get("capex_total_referencial_clp"), 11494765)
        assert_equal(errors, "P45 CAPEX total base", capex_total_500.get("capex_total_referencial", {}).get("base", {}).get("capex_total_referencial_clp"), 13343765)
        assert_equal(errors, "P45 CAPEX total alto", capex_total_500.get("capex_total_referencial", {}).get("alto", {}).get("capex_total_referencial_clp"), 16781765)
        assert_equal(errors, "P45 OPEX sin mano de obra", opex_500.get("subtotal_sin_mano_obra_clp_mes"), 1086750)
        assert_equal(errors, "P45 OPEX con mano de obra", opex_500.get("subtotal_con_mano_obra_clp_mes"), 1686750)
        assert_equal(errors, "P45 ingreso mensual base", ingresos_500.get("sensibilidades", {}).get("base", {}).get("ingreso_mensual_clp"), 2646367)
        assert_equal(errors, "P45 margen sin mano de obra", flujo_500.get("margenes", {}).get("sin_mano_obra_clp_mes"), 1559617)
        assert_equal(errors, "P45 margen con mano de obra", flujo_500.get("margenes", {}).get("con_mano_obra_clp_mes"), 959617)
        assert_close(errors, "P45 punto equilibrio sin mano de obra semana", flujo_500.get("punto_equilibrio", {}).get("sin_mano_obra_bandejas_semana"), 41.1, 0.05)
        assert_close(errors, "P45 punto equilibrio con mano de obra semana", flujo_500.get("punto_equilibrio", {}).get("con_mano_obra_bandejas_semana"), 63.7, 0.05)
        assert_equal(errors, "P45 estrategia 352", estrategia_pollonas.get("estrategias", {}).get("comprar_352_de_una_vez", {}).get("capex_pollonas_clp"), 4224000)
        assert_equal(errors, "P45 estrategia 100", estrategia_pollonas.get("estrategias", {}).get("100_primero", {}).get("capex_pollonas_clp"), 1200000)
        if capex_total_500.get("capex_total_referencial", {}).get("base", {}).get("deficit_o_excedente_clp", 0) >= 0:
            errors.append("P45 CAPEX base debe mostrar déficit frente a $10.000.000")

        # P47: decisión ejecutiva y plan por etapas
        assert_equal(errors, "P47 estado", decision_p47.get("estado_general"), "AMARILLO")
        assert_equal(errors, "P47 alternativa recomendada", decision_p47.get("alternativa_recomendada"), "mas_150_pollonas")
        assert_equal(errors, "P47 capital trabajo mínimo", decision_p47.get("capital_trabajo", {}).get("minimo_1_mes_clp"), 1686750)
        assert_equal(errors, "P47 capital trabajo prudente", decision_p47.get("capital_trabajo", {}).get("prudente_2_meses_clp"), 3373500)
        assert_equal(errors, "P47 deficit base 1m CT", decision_p47.get("respuestas_clave", {}).get("dinero_faltante_escenario_base", {}).get("deficit_base_con_1_mes_ct_vs_10m_clp"), -5030515)
        assert_equal(errors, "P47 deficit base 2m CT", decision_p47.get("respuestas_clave", {}).get("dinero_faltante_escenario_base", {}).get("deficit_base_con_2_meses_ct_vs_10m_clp"), -6717265)
        p47_alts = {item.get("pollonas_a_comprar"): item for item in alternativas_p47.get("alternativas", []) if isinstance(item, dict)}
        if set(p47_alts) != {100, 150, 200, 352}:
            errors.append(f"P47 alternativas: esperado {{100, 150, 200, 352}}, encontrado {set(p47_alts)!r}")
        assert_equal(errors, "P47 +100 plantel", p47_alts.get(100, {}).get("plantel_total_aves"), 248)
        assert_close(errors, "P47 +100 bandejas", p47_alts.get(100, {}).get("bandejas_semana_estimadas"), 49.6, 0.05)
        assert_equal(errors, "P47 +150 plantel", p47_alts.get(150, {}).get("plantel_total_aves"), 298)
        assert_close(errors, "P47 +150 bandejas", p47_alts.get(150, {}).get("bandejas_semana_estimadas"), 59.6, 0.05)
        assert_equal(errors, "P47 +200 plantel", p47_alts.get(200, {}).get("plantel_total_aves"), 348)
        assert_close(errors, "P47 +200 bandejas", p47_alts.get(200, {}).get("bandejas_semana_estimadas"), 69.6, 0.05)
        assert_equal(errors, "P47 +352 plantel", p47_alts.get(352, {}).get("plantel_total_aves"), 500)
        assert_equal(errors, "P47 +352 requerimiento 1m", p47_alts.get(352, {}).get("lectura_con_galpon_completo_desde_inicio", {}).get("requerimiento_total_inicial_1_mes_ct_clp"), 15030515)
        assert_equal(errors, "P47 semaforo 100", p47_alts.get(100, {}).get("semaforo"), "AMARILLO BAJO")
        assert_equal(errors, "P47 semaforo 150", p47_alts.get(150, {}).get("semaforo"), "AMARILLO MEDIO")
        assert_equal(errors, "P47 semaforo 352", p47_alts.get(352, {}).get("semaforo"), "AMARILLO ALTO")
        assert_equal(errors, "P47 plan 6 meses", plan_p47.get("horizonte_meses"), 6)
        if len(plan_p47.get("fases", [])) != 6:
            errors.append("P47 plan debe tener 6 fases")
        if len(reglas_p47.get("verde_solo_si", [])) < 7:
            errors.append("P47 reglas verde: faltan condiciones")
        if "compra de aves" not in decision_p47.get("decisiones_no_autorizadas", []):
            errors.append("P47 debe mantener compra de aves no autorizada")

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

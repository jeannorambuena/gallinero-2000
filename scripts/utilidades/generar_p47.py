#!/usr/bin/env python3
"""Genera P47: decisión ejecutiva y plan de implementación por etapas."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REVISION_DATE = "2026-07-06"

CURRENT_BIRDS = 148
TARGET_BIRDS = 500
OWN_CAPITAL = 10_000_000
POLLONA_PRICE = 12_000
GALPON_CLP = 5_547_765
FULL_EQUIPMENT_BASE = 3_572_000
CAPEX_TOTAL_BASE = 13_343_765
OPEX_500_WITHOUT_LABOR = 1_086_750
OPEX_500_WITH_LABOR = 1_686_750
CT_MIN = OPEX_500_WITH_LABOR
CT_PRUDENT = OPEX_500_WITH_LABOR * 2
PRICE_AVG = 6_107

LABOR_BY_NEW_BIRDS = {100: 300_000, 150: 400_000, 200: 500_000, 352: 600_000}
NAMES = {
    100: "Alternativa 1: crecimiento mínimo controlado",
    150: "Alternativa 2: crecimiento intermedio prudente",
    200: "Alternativa 3: crecimiento acelerado moderado",
    352: "Alternativa 4: escala completa inmediata",
}
USAGES = {
    100: "Prueba comercial y operacional.",
    150: "Recomendación preliminar si no hay financiamiento completo.",
    200: "Viable solo con compradores más confirmados y caja adicional.",
    352: "Solo con financiamiento cerrado y venta confirmada.",
}
ADVANTAGES = {
    100: "Menor riesgo financiero.",
    150: "Equilibrio entre crecimiento y riesgo.",
    200: "Se acerca más rápido a escala comercial.",
    352: "Captura ingreso completo antes.",
}
DISADVANTAGES = {
    100: "No llega a meta de 100 bandejas/semana.",
    150: "Aún no alcanza 100 bandejas/semana.",
    200: "Más presión de caja y equipamiento.",
    352: "Requiere financiamiento importante y aumenta riesgo operativo.",
}
SEMAFORO = {
    100: "AMARILLO BAJO",
    150: "AMARILLO MEDIO",
    200: "AMARILLO ALTO",
    352: "AMARILLO ALTO",
}
CONDITIONS = {
    100: "Ejecutar solo si infraestructura actual alcanza y están listos comederos/bebederos/nidos mínimos.",
    150: "Ejecutar solo con infraestructura actual validada, compradores para al menos el punto de equilibrio y caja para capital de trabajo.",
    200: "Ejecutar solo con venta adicional documentada, caja adicional y equipamiento proporcional cerrado.",
    352: "No ejecutar sin financiamiento cerrado para CAPEX total, equipamiento, capital de trabajo y venta de 100 bandejas/semana confirmada al contado.",
}
RECOMMENDATION = (
    "Conviene seguir avanzando solo como P0/P47 amarillo: levantar cotizaciones, validar permisos, cerrar compradores y preparar una primera etapa. "
    "No conviene comprar las 352 pollonas de una vez salvo que exista financiamiento cerrado para CAPEX base + capital de trabajo y venta de 100 bandejas/semana confirmada al contado. "
    "La alternativa preliminar preferida es +150 pollonas; +100 es la opción más conservadora si se quiere reducir riesgo; +200 requiere venta y caja más confirmadas."
)


def clp(value: int | float | None) -> str:
    if value is None:
        return "pendiente"
    return "$" + f"{round(value):,}".replace(",", ".")


def write_json(rel: str, data: dict[str, Any]) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(rel: str) -> dict[str, Any]:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_csv(rel: str, header: list[str], rows: list[list[Any]]) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def monthly_income(bandejas_semana: float) -> int:
    return round(bandejas_semana * PRICE_AVG * 52 / 12)


def stage_data(new_birds: int) -> dict[str, Any]:
    total_birds = CURRENT_BIRDS + new_birds
    bird_ratio = total_birds / TARGET_BIRDS
    increment_ratio = new_birds / 352
    bandejas_semana = round(100 * bird_ratio, 1)
    income = monthly_income(bandejas_semana)
    opex_without_labor = round(OPEX_500_WITHOUT_LABOR * bird_ratio)
    labor = LABOR_BY_NEW_BIRDS[new_birds]
    opex_with_labor = opex_without_labor + labor
    margin_without_labor = income - opex_without_labor
    margin_with_labor = income - opex_with_labor
    break_even_without_labor = round((opex_without_labor / PRICE_AVG) * 12 / 52, 1)
    break_even_with_labor = round((opex_with_labor / PRICE_AVG) * 12 / 52, 1)
    pollonas_capex = new_birds * POLLONA_PRICE
    equipment_incremental = round(FULL_EQUIPMENT_BASE * increment_ratio)
    equipment_by_total_birds = round(FULL_EQUIPMENT_BASE * bird_ratio)

    if new_birds == 352:
        partial_investment = None
        partial_initial_requirement = None
        partial_delta = None
        full_investment = CAPEX_TOTAL_BASE
        full_initial_requirement = full_investment + CT_MIN
        full_initial_requirement_2m = full_investment + CT_PRUDENT
        full_delta = OWN_CAPITAL - full_initial_requirement
        full_delta_2m = OWN_CAPITAL - full_initial_requirement_2m
        payback_partial = None
    else:
        partial_investment = pollonas_capex + equipment_incremental
        partial_initial_requirement = partial_investment + opex_with_labor
        partial_delta = OWN_CAPITAL - partial_initial_requirement
        full_investment = pollonas_capex + GALPON_CLP + equipment_by_total_birds
        full_initial_requirement = full_investment + opex_with_labor
        full_initial_requirement_2m = full_investment + (opex_with_labor * 2)
        full_delta = OWN_CAPITAL - full_initial_requirement
        full_delta_2m = OWN_CAPITAL - full_initial_requirement_2m
        payback_partial = round(partial_investment / margin_with_labor, 2) if margin_with_labor > 0 else None

    payback_full = round(full_investment / margin_with_labor, 2) if margin_with_labor > 0 else None

    return {
        "id": f"mas_{new_birds}_pollonas",
        "nombre": NAMES[new_birds],
        "pollonas_a_comprar": new_birds,
        "plantel_total_aves": total_birds,
        "bandejas_semana_estimadas": bandejas_semana,
        "capex_pollonas_clp": pollonas_capex,
        "equipamiento_proporcional_incremental_clp": equipment_incremental,
        "equipamiento_proporcional_por_plantel_clp": equipment_by_total_birds,
        "lectura_parcial_infraestructura_actual": {
            "aplica": new_birds != 352,
            "nota": "Requiere validación de capacidad de infraestructura actual; equipamiento no escala perfectamente lineal.",
            "total_inversion_estimada_clp": partial_investment,
            "capital_trabajo_recomendado_1_mes_clp": opex_with_labor if new_birds != 352 else None,
            "requerimiento_total_inicial_clp": partial_initial_requirement,
            "deficit_o_excedente_vs_10m_clp": partial_delta,
            "payback_simple_con_mano_obra_meses": payback_partial,
        },
        "lectura_con_galpon_completo_desde_inicio": {
            "incluye_galpon_72m2_clp": GALPON_CLP,
            "total_inversion_estimada_clp": full_investment,
            "capital_trabajo_minimo_1_mes_clp": CT_MIN if new_birds == 352 else opex_with_labor,
            "capital_trabajo_prudente_2_meses_clp": CT_PRUDENT if new_birds == 352 else opex_with_labor * 2,
            "requerimiento_total_inicial_1_mes_ct_clp": full_initial_requirement,
            "requerimiento_total_inicial_2_meses_ct_clp": full_initial_requirement_2m,
            "deficit_o_excedente_vs_10m_1_mes_ct_clp": full_delta,
            "deficit_o_excedente_vs_10m_2_meses_ct_clp": full_delta_2m,
            "payback_simple_con_mano_obra_meses": payback_full,
        },
        "ingreso_mensual_estimado_clp": income,
        "opex_mensual_sin_mano_obra_clp": opex_without_labor,
        "mano_obra_referencial_clp_mes": labor,
        "opex_mensual_con_mano_obra_clp": opex_with_labor,
        "margen_mensual_sin_mano_obra_clp": margin_without_labor,
        "margen_mensual_con_mano_obra_clp": margin_with_labor,
        "punto_equilibrio_sin_mano_obra_bandejas_semana": break_even_without_labor,
        "punto_equilibrio_con_mano_obra_bandejas_semana": break_even_with_labor,
        "ventaja": ADVANTAGES[new_birds],
        "desventaja": DISADVANTAGES[new_birds],
        "uso_recomendado": USAGES[new_birds],
        "semaforo": SEMAFORO[new_birds],
        "condicion_para_ejecutar": CONDITIONS[new_birds],
    }


alternatives = [stage_data(n) for n in (100, 150, 200, 352)]
by_id = {alt["id"]: alt for alt in alternatives}
full = by_id["mas_352_pollonas"]

rules = {
    "proyecto": "Gallinero Nacho",
    "fase": "P47",
    "estado": "AMARILLO",
    "regla_general": "P47 no aprueba inversión; solo ordena decisión ejecutiva y condiciones para pasar de amarillo a verde.",
    "verde_solo_si": [
        "existen cotizaciones formales finales",
        "financiamiento total está cubierto",
        "capital de trabajo mínimo está cubierto",
        "venta de al menos punto de equilibrio con mano de obra está confirmada",
        "validación legal/sanitaria/tributaria está cerrada",
        "plan logístico invierno definido",
        "calendario de ejecución real aprobado",
    ],
    "amarillo_si": [
        "flujo es positivo pero falta financiamiento o cotización formal",
        "venta está estimada pero no documentada por canal",
        "permisos/formalización no validados",
        "infraestructura actual no confirmada para etapa",
    ],
    "rojo_si": [
        "no se alcanza punto de equilibrio",
        "no hay financiamiento para déficit",
        "no hay capacidad de vender la producción",
        "no hay agua/equipamiento mínimo",
        "se intenta comprar 352 pollonas sin equipamiento ni capital de trabajo",
    ],
}

plan = {
    "proyecto": "Gallinero Nacho",
    "fase": "P47",
    "estado": "AMARILLO",
    "horizonte_meses": 6,
    "objetivo": "Implementar crecimiento por etapas sin aprobar inversión mayor hasta cerrar evidencia crítica.",
    "fases": [
        {"fase": "Fase 0", "nombre": "cierre de decisión", "periodo": "semana 1-2", "acciones": ["revisar dashboard con Nacho", "confirmar monto disponible real", "validar permisos/formalización", "pedir cotizaciones formales", "confirmar compradores por canal"]},
        {"fase": "Fase 1", "nombre": "preparación mínima", "periodo": "mes 1", "acciones": ["cotizar equipamiento final", "revisar infraestructura actual", "revisar capacidad de bodega semanal", "resolver agua/energía faltante", "plan invierno/acceso"]},
        {"fase": "Fase 2", "nombre": "primera compra", "periodo": "mes 2", "acciones": ["ejecutar alternativa 100-150 pollonas solo si están listos comederos/bebederos/nidos mínimos", "registrar producción", "registrar consumo", "registrar ventas"]},
        {"fase": "Fase 3", "nombre": "medición 30-60 días", "periodo": "mes 3-4", "acciones": ["medir ventas reales", "medir mortalidad", "medir consumo alimento", "medir horas de trabajo", "medir margen real", "levantar problemas sanitarios/logísticos"]},
        {"fase": "Fase 4", "nombre": "segunda expansión", "periodo": "mes 4-5", "acciones": ["si ventas y margen cumplen, subir a 200 o avanzar hacia 500", "si no cumplen, mantener escala y corregir"]},
        {"fase": "Fase 5", "nombre": "escala completa", "periodo": "mes 6", "acciones": ["llegar a 500 solo con flujo real validado", "equipamiento completo", "financiamiento cerrado", "compradores estables", "formalización validada"]},
    ],
}

decision = {
    "proyecto": "Gallinero Nacho",
    "fase": "P47",
    "estado_general": "AMARILLO",
    "decision": "Avanzar solo en preparación y primera etapa controlada; no aprobar compra completa, construcción ni inversión mayor.",
    "recomendacion_ejecutiva": RECOMMENDATION,
    "respuestas_clave": {
        "conviene_avanzar": "Sí, pero solo por etapas y con control de riesgo; el negocio muestra margen positivo si se venden 100 bandejas/semana.",
        "conviene_comprar_352_de_una_vez": "No como recomendación base; solo sería viable con financiamiento cerrado y venta de 100 bandejas/semana confirmada al contado.",
        "etapa_inicial_mas_prudente": "+150 pollonas como recomendación base prudente; +100 si se prioriza máxima reducción de riesgo.",
        "dinero_faltante_escenario_base": {
            "capex_base_sin_ct_clp": CAPEX_TOTAL_BASE,
            "deficit_capex_base_vs_10m_clp": OWN_CAPITAL - CAPEX_TOTAL_BASE,
            "requerimiento_base_con_1_mes_ct_clp": full["lectura_con_galpon_completo_desde_inicio"]["requerimiento_total_inicial_1_mes_ct_clp"],
            "deficit_base_con_1_mes_ct_vs_10m_clp": full["lectura_con_galpon_completo_desde_inicio"]["deficit_o_excedente_vs_10m_1_mes_ct_clp"],
            "requerimiento_base_con_2_meses_ct_clp": full["lectura_con_galpon_completo_desde_inicio"]["requerimiento_total_inicial_2_meses_ct_clp"],
            "deficit_base_con_2_meses_ct_vs_10m_clp": full["lectura_con_galpon_completo_desde_inicio"]["deficit_o_excedente_vs_10m_2_meses_ct_clp"],
        },
        "antes_de_invertir": rules["verde_solo_si"],
        "plan_6_meses": "Fase 0 cierre de decisión, Fase 1 preparación mínima, Fase 2 primera compra 100-150, Fase 3 medición 30-60 días, Fase 4 segunda expansión, Fase 5 escala completa condicionada.",
    },
    "alternativa_recomendada": "mas_150_pollonas",
    "alternativa_conservadora": "mas_100_pollonas",
    "alternativa_no_recomendada_sin_financiamiento": "mas_352_pollonas",
    "capital_trabajo": {"minimo_1_mes_clp": CT_MIN, "prudente_2_meses_clp": CT_PRUDENT, "criterio": "Usar OPEX con mano de obra como escenario prudente."},
    "condiciones_para_pasar_a_verde": rules["verde_solo_si"],
    "decisiones_no_autorizadas": ["compra de aves", "construcción", "inversión mayor", "P1 definitivo"],
}

alt_json = {
    "proyecto": "Gallinero Nacho",
    "fase": "P47",
    "estado": "AMARILLO",
    "supuestos": {
        "precios_p45_p46": "referenciales, no cotización formal",
        "escenario_base_bandejas_semana": 100,
        "precio_promedio_bandeja_clp": PRICE_AVG,
        "opex_base_prudente": "OPEX con mano de obra",
        "capital_trabajo_minimo_1_mes_clp": CT_MIN,
        "capital_trabajo_prudente_2_meses_clp": CT_PRUDENT,
        "horizonte_implementacion_meses": 6,
        "produccion_proporcional": "500 aves = 100 bandejas/semana",
        "nota_equipamiento": "El equipamiento proporcional es aproximado; no escala perfectamente lineal.",
    },
    "alternativas": alternatives,
}

write_json("dashboard/data/decision-ejecutiva-p47.json", decision)
write_json("dashboard/data/alternativas-crecimiento-p47.json", alt_json)
write_json("dashboard/data/plan-implementacion-6-meses.json", plan)
write_json("dashboard/data/reglas-decision-semaforo-p47.json", rules)

write_csv(
    "datos/procesados/indicadores/p47-alternativas-crecimiento.csv",
    [
        "alternativa", "pollonas", "plantel_total", "bandejas_semana", "capex_pollonas_clp", "equipamiento_parcial_clp",
        "inversion_parcial_clp", "requerimiento_parcial_1m_ct_clp", "deficit_excedente_parcial_vs_10m_clp",
        "inversion_con_galpon_clp", "requerimiento_con_galpon_1m_ct_clp", "deficit_excedente_con_galpon_vs_10m_clp",
        "ingreso_mensual_clp", "opex_con_mano_obra_clp", "margen_con_mano_obra_clp", "semaforo", "condicion_para_ejecutar",
    ],
    [
        [
            alt["id"], alt["pollonas_a_comprar"], alt["plantel_total_aves"], alt["bandejas_semana_estimadas"], alt["capex_pollonas_clp"], alt["equipamiento_proporcional_incremental_clp"],
            alt["lectura_parcial_infraestructura_actual"]["total_inversion_estimada_clp"], alt["lectura_parcial_infraestructura_actual"]["requerimiento_total_inicial_clp"], alt["lectura_parcial_infraestructura_actual"]["deficit_o_excedente_vs_10m_clp"],
            alt["lectura_con_galpon_completo_desde_inicio"]["total_inversion_estimada_clp"], alt["lectura_con_galpon_completo_desde_inicio"]["requerimiento_total_inicial_1_mes_ct_clp"], alt["lectura_con_galpon_completo_desde_inicio"]["deficit_o_excedente_vs_10m_1_mes_ct_clp"],
            alt["ingreso_mensual_estimado_clp"], alt["opex_mensual_con_mano_obra_clp"], alt["margen_mensual_con_mano_obra_clp"], alt["semaforo"], alt["condicion_para_ejecutar"],
        ]
        for alt in alternatives
    ],
)
write_csv(
    "datos/procesados/indicadores/p47-decision-ejecutiva.csv",
    ["indicador", "valor", "unidad", "estado", "observacion"],
    [
        ["estado_general_p47", "AMARILLO", "semaforo", "vigente", "No desbloquea inversión, compra ni construcción"],
        ["alternativa_recomendada", "+150 pollonas", "texto", "preliminar", "Base prudente si no hay financiamiento completo"],
        ["deficit_base_1m_ct", abs(full["lectura_con_galpon_completo_desde_inicio"]["deficit_o_excedente_vs_10m_1_mes_ct_clp"]), "CLP", "pendiente_financiamiento", "Escala completa inmediata con 1 mes de capital de trabajo"],
        ["deficit_base_2m_ct", abs(full["lectura_con_galpon_completo_desde_inicio"]["deficit_o_excedente_vs_10m_2_meses_ct_clp"]), "CLP", "pendiente_financiamiento", "Escala completa inmediata con 2 meses de capital de trabajo"],
        ["capital_trabajo_minimo", CT_MIN, "CLP", "prudente", "1 mes OPEX con mano de obra"],
        ["capital_trabajo_prudente", CT_PRUDENT, "CLP", "prudente", "2 meses OPEX con mano de obra"],
    ],
)

# Actualizar JSON existentes
res = read_json("dashboard/data/resumen-ejecutivo-p0.json")
res.update({"fase": "P0 — Diagnóstico real / P47", "estado_general": "amarillo"})
res["decision_ejecutiva_p47"] = decision
res["conclusion"] = "P47 mantiene estado AMARILLO: conviene avanzar solo por etapas y con control de riesgo. La alternativa base prudente es +150 pollonas; +352 no debe ejecutarse sin financiamiento cerrado, equipamiento, capital de trabajo y venta confirmada."
for point in ["P47 ordena alternativas 100/150/200/352 pollonas con inversión, margen, capital de trabajo y semáforo.", "El negocio muestra margen positivo si se vende la producción estimada, pero falta evidencia crítica."]:
    if point not in res.setdefault("puntos_favorables", []):
        res["puntos_favorables"].append(point)
for risk in ["Escala completa inmediata requiere $15.030.515 con 1 mes de capital de trabajo y $16.717.265 con 2 meses.", "Comprar 352 pollonas sin financiamiento cerrado sería AMARILLO ALTO y no recomendado."]:
    if risk not in res.setdefault("riesgos_principales", []):
        res["riesgos_principales"].append(risk)
write_json("dashboard/data/resumen-ejecutivo-p0.json", res)

sem = read_json("dashboard/data/semaforo-decision.json")
sem.update({"fase": "P0 — Diagnóstico real / P47", "estado": "amarillo", "semaforo_general": "amarillo", "reglas_p47": rules, "alternativas_p47": {alt["id"]: alt["semaforo"] for alt in alternatives}})
sem["condiciones_para_avanzar"] = rules["verde_solo_si"]
sem["conclusion"] = "P47 mantiene AMARILLO: flujo preliminar positivo, pero faltan cotizaciones, financiamiento, capital de trabajo, validación comercial/legal y plan logístico."
write_json("dashboard/data/semaforo-decision.json", sem)

estado = read_json("dashboard/data/estado-proyecto.json")
estado.update({"fase": "P0 — Diagnóstico real / P47", "semaforo_general": "amarillo", "decision_actual": "P47 recomienda avanzar solo por etapas: +150 pollonas como base prudente, +100 si se prioriza máximo control, +200 solo con venta/caja confirmadas, +352 solo con financiamiento cerrado."})
estado["proximos_pasos"] = ["revisar P47 con Nacho", "confirmar capital disponible real", "cerrar cotizaciones formales", "validar infraestructura actual para etapa 100-150", "confirmar compradores por canal", "validar legal/sanitario/tributario", "definir calendario de 6 meses"]
write_json("dashboard/data/estado-proyecto.json", estado)

falt = read_json("dashboard/data/datos-faltantes.json")
falt.update({"fase": "P0 — Diagnóstico real / P47", "estado": "AMARILLO"})
falt["nota"] = "P47 transforma P45-P46 en decisión ejecutiva por etapas; siguen faltando condiciones de verde antes de invertir."
falt["p47_pendientes_criticos"] = rules["verde_solo_si"]
write_json("dashboard/data/datos-faltantes.json", falt)

alerts = read_json("dashboard/data/alertas-p0.json")
alerts.update({"fase": "P0 — Diagnóstico real / P47"})
for new_alert in [
    {"id": "A25", "titulo": "P47 no aprueba inversión", "severidad": "alta", "dimension": "decision", "descripcion": "P47 entrega recomendación ejecutiva y plan por etapas, pero mantiene estado AMARILLO y no autoriza compra, construcción ni inversión mayor.", "estado": "bloqueante"},
    {"id": "A26", "titulo": "Escala completa inmediata requiere financiamiento adicional", "severidad": "alta", "dimension": "financiera", "descripcion": f"Escala completa base con 1 mes de capital de trabajo requiere {clp(full['lectura_con_galpon_completo_desde_inicio']['requerimiento_total_inicial_1_mes_ct_clp'])}; faltan {clp(abs(full['lectura_con_galpon_completo_desde_inicio']['deficit_o_excedente_vs_10m_1_mes_ct_clp']))} vs $10.000.000.", "estado": "abierta"},
    {"id": "A27", "titulo": "Compra 352 pollonas es AMARILLO ALTO", "severidad": "alta", "dimension": "operacional", "descripcion": "No ejecutar compra de 352 pollonas sin equipamiento, capital de trabajo, financiamiento cerrado y venta confirmada al contado.", "estado": "bloqueante"},
]:
    if not any(a.get("id") == new_alert["id"] for a in alerts.setdefault("alertas", [])):
        alerts["alertas"].append(new_alert)
write_json("dashboard/data/alertas-p0.json", alerts)

flujo = read_json("dashboard/data/flujo-financiero-preliminar-500.json")
flujo["p47_decision_por_etapas"] = {"alternativas": alternatives, "recomendacion": RECOMMENDATION}
flujo["advertencia"] = "Flujo preliminar referencial P45-P47; no declara inversión aprobada ni semáforo verde."
write_json("dashboard/data/flujo-financiero-preliminar-500.json", flujo)

estrategia = read_json("dashboard/data/estrategia-compra-pollonas.json")
estrategia["p47_alternativas_detalladas"] = alternatives
estrategia["recomendacion_preliminar"] = RECOMMENDATION
estrategia["estado"] = "recomendacion_preliminar/amarillo/P47"
write_json("dashboard/data/estrategia-compra-pollonas.json", estrategia)

# Reporte y docs
alt_lines = []
for alt in alternatives:
    partial = alt["lectura_parcial_infraestructura_actual"]
    full_read = alt["lectura_con_galpon_completo_desde_inicio"]
    alt_lines.append(
        f"### {alt['nombre']}\n\n"
        f"- Pollonas: **{alt['pollonas_a_comprar']} pollonas**; plantel total: **{alt['plantel_total_aves']} aves**.\n"
        f"- Producción estimada: **{alt['bandejas_semana_estimadas']} bandejas/semana**.\n"
        f"- Ingreso mensual estimado: **{clp(alt['ingreso_mensual_estimado_clp'])}**.\n"
        f"- OPEX con mano de obra: **{clp(alt['opex_mensual_con_mano_obra_clp'])}**.\n"
        f"- Margen con mano de obra: **{clp(alt['margen_mensual_con_mano_obra_clp'])}**.\n"
        f"- Lectura parcial sin galpón completo: inversión **{clp(partial['total_inversion_estimada_clp'])}**, requerimiento inicial con CT **{clp(partial['requerimiento_total_inicial_clp'])}**, excedente/déficit vs $10M **{clp(partial['deficit_o_excedente_vs_10m_clp'])}**.\n"
        f"- Lectura con galpón completo: inversión **{clp(full_read['total_inversion_estimada_clp'])}**, requerimiento inicial 1 mes CT **{clp(full_read['requerimiento_total_inicial_1_mes_ct_clp'])}**, excedente/déficit vs $10M **{clp(full_read['deficit_o_excedente_vs_10m_1_mes_ct_clp'])}**.\n"
        f"- Semáforo: **{alt['semaforo']}**.\n"
        f"- Uso: {alt['uso_recomendado']}\n"
        f"- Condición: {alt['condicion_para_ejecutar']}\n"
    )

plan_lines = []
for phase in plan["fases"]:
    actions = "\n".join([f"  - {item}" for item in phase["acciones"]])
    plan_lines.append(f"### {phase['fase']} — {phase['nombre']} ({phase['periodo']})\n\n{actions}\n")

report = f"""# P47 — Decisión ejecutiva y plan por etapas

Estado general: **AMARILLO**. P47 **no aprueba inversión**, no desbloquea compra de aves y no autoriza construcción.

## Recomendación ejecutiva

{RECOMMENDATION}

## Respuestas clave

1. **¿Conviene avanzar?** Sí, pero solo por etapas y con control de riesgo. El negocio muestra margen positivo si se venden 100 bandejas/semana.
2. **¿Conviene comprar las 352 pollonas de una vez?** No como recomendación base. Solo con financiamiento cerrado, equipamiento, capital de trabajo y venta confirmada.
3. **¿Cuál etapa inicial es más prudente?** +150 pollonas como base prudente; +100 si se prioriza máxima reducción de riesgo.
4. **¿Cuánto falta en escenario base?** CAPEX base + 1 mes CT requiere **{clp(full['lectura_con_galpon_completo_desde_inicio']['requerimiento_total_inicial_1_mes_ct_clp'])}**, déficit **{clp(abs(full['lectura_con_galpon_completo_desde_inicio']['deficit_o_excedente_vs_10m_1_mes_ct_clp']))}**. Con 2 meses CT requiere **{clp(full['lectura_con_galpon_completo_desde_inicio']['requerimiento_total_inicial_2_meses_ct_clp'])}**, déficit **{clp(abs(full['lectura_con_galpon_completo_desde_inicio']['deficit_o_excedente_vs_10m_2_meses_ct_clp']))}**.
5. **Antes de invertir:** cotizaciones formales, financiamiento, capital de trabajo, ventas por canal, validación legal/sanitaria/tributaria, logística invierno y calendario real.

## Capital de trabajo considerado

- Mínimo 1 mes: **{clp(CT_MIN)}**.
- Prudente 2 meses: **{clp(CT_PRUDENT)}**.

## Matriz de alternativas

{chr(10).join(alt_lines)}

## Reglas de decisión

### VERDE solo si

{chr(10).join([f'- {item}' for item in rules['verde_solo_si']])}

### AMARILLO si

{chr(10).join([f'- {item}' for item in rules['amarillo_si']])}

### ROJO si

{chr(10).join([f'- {item}' for item in rules['rojo_si']])}

## Plan de implementación 6 meses

{chr(10).join(plan_lines)}

## Pendientes críticos

- Cotizaciones formales finales.
- Validación legal/sanitaria/tributaria.
- Confirmación comercial por canal.
- Financiamiento para déficit + capital de trabajo.
- Plan logístico invierno.
- Calendario real de compra/inversión.
"""
for rel in [
    "reports/p47_decision_ejecutiva_y_plan_por_etapas.md",
    "docs/01-p0-diagnostico/flujo-caja-preliminar.md",
    "docs/02-informes/informe-ejecutivo-nacho-500.md",
]:
    (ROOT / rel).write_text(report, encoding="utf-8")

faltantes_md = f"""# Datos faltantes P47 — Proyecto Gallinero Nacho

P47 mantiene estado **AMARILLO**. Ya existe decisión ejecutiva preliminar y plan por etapas, pero no hay autorización de compra, construcción ni inversión mayor.

## Pendientes para pasar a verde

{chr(10).join([f'- {item}' for item in rules['verde_solo_si']])}

## Pendientes críticos operativos

- Confirmar si infraestructura actual permite +100 o +150 pollonas sin galpón completo.
- Cerrar cotización formal de comederos, bebederos, nidos, agua y energía.
- Confirmar compradores por canal para al menos el punto de equilibrio con mano de obra.
- Confirmar financiamiento de déficit y capital de trabajo.
- Definir calendario real de compra/inversión.
"""
(ROOT / "docs/01-p0-diagnostico/datos-faltantes.md").write_text(faltantes_md, encoding="utf-8")

print("P47 data generated")

#!/usr/bin/env python3
"""Genera datos P45-P46: CAPEX/OPEX/flujo/estrategia pollonas."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVISION_DATE = "2026-07-06"

KNOWN_CAPEX = {
    "galpon_clp": 5_547_765,
    "pollonas_faltantes_clp": 4_224_000,
    "subtotal_conocido_clp": 9_771_765,
    "capacidad_inversion_propia_clp": 10_000_000,
}

OPEX = {
    "alimento_clp_mes": 971_250,
    "envases_clp_mes": 45_500,
    "viruta_clp_mes": 34_000,
    "bencina_reparto_clp_mes": 10_000,
    "vitaminas_clp_mes": 20_000,
    "agua_clp_mes": 6_000,
    "medicamentos_limpieza_adicional_clp_mes": 0,
}
OPEX_SIN_MO = sum(OPEX.values())
MANO_OBRA = 600_000
OPEX_CON_MO = OPEX_SIN_MO + MANO_OBRA
IMP_5 = round(OPEX_SIN_MO * 0.05)
IMP_10 = round(OPEX_SIN_MO * 0.10)

PRICE_AVG = 6_107
INGRESO_SEMANAL_BASE = 100 * PRICE_AVG
INGRESO_MENSUAL_BASE = round(INGRESO_SEMANAL_BASE * 52 / 12)
INGRESOS = {
    "base": {
        "bandejas_semana": 100,
        "precio_promedio_clp": PRICE_AVG,
        "ingreso_semanal_clp": INGRESO_SEMANAL_BASE,
        "ingreso_mensual_clp": INGRESO_MENSUAL_BASE,
        "observacion": "Meta comercial base: 100 bandejas/semana al mix/precio promedio actual.",
    },
    "conservador_90": {
        "bandejas_semana": 90,
        "precio_promedio_clp": PRICE_AVG,
        "ingreso_semanal_clp": 90 * PRICE_AVG,
        "ingreso_mensual_clp": round(90 * PRICE_AVG * 52 / 12),
        "observacion": "Sensibilidad conservadora: 90 bandejas/semana al mismo precio promedio.",
    },
    "descuento_almacenes": {
        "bandejas_semana": 100,
        "precio_promedio_clp": PRICE_AVG,
        "descuento_sobre_bandejas_semana": 30,
        "descuento_porcentaje": 10,
        "ingreso_semanal_clp": round((70 * PRICE_AVG) + (30 * PRICE_AVG * 0.90)),
        "ingreso_mensual_clp": round(((70 * PRICE_AVG) + (30 * PRICE_AVG * 0.90)) * 52 / 12),
        "observacion": "Sensibilidad, aunque Nacho informa que almacenes pagarían igual.",
    },
    "alto_104_1": {
        "bandejas_semana": 104.1,
        "precio_promedio_clp": PRICE_AVG,
        "ingreso_semanal_clp": round(104.1 * PRICE_AVG),
        "ingreso_mensual_clp": round(104.1 * PRICE_AVG * 52 / 12),
        "observacion": "Sensibilidad alta: venta de toda la producción técnica estimada para 500 aves.",
    },
}

SOURCES = [
    {
        "id": "sodimac_malla_gallinero_busqueda",
        "proveedor": "Sodimac Chile",
        "url": "https://www.sodimac.cl/sodimac-cl/search?Ntt=malla%20gallinero",
        "fecha_revision": REVISION_DATE,
        "observacion": "Búsqueda pública Sodimac; precios extraídos desde __NEXT_DATA__.",
    },
    {
        "id": "sodimac_polin_impregnado_busqueda",
        "proveedor": "Sodimac Chile",
        "url": "https://www.sodimac.cl/sodimac-cl/search?Ntt=polin%20impregnado%202x2",
        "fecha_revision": REVISION_DATE,
        "observacion": "Referencia para perchas, soportes y sectorización interior.",
    },
    {
        "id": "sodimac_estante_rimax",
        "proveedor": "Sodimac Chile",
        "url": "https://www.sodimac.cl/sodimac-cl/articulo/116341305/Estante-Repisa-Rack-plastico-4-Niveles-91x45x145cm-Rimax/116341308",
        "fecha_revision": REVISION_DATE,
        "observacion": "Página con oferta JSON-LD: precio normal $55.990 CLP.",
    },
    {
        "id": "sodimac_agua_manguera_valvula",
        "proveedor": "Sodimac Chile",
        "url": "https://www.sodimac.cl/sodimac-cl/search?Ntt=manguera%20jardin%2025%20m",
        "fecha_revision": REVISION_DATE,
        "observacion": "Referencia de mangueras y fittings; se complementa con búsqueda de válvula bola PVC 25 mm.",
    },
    {
        "id": "sodimac_electrico_conduit_protecciones",
        "proveedor": "Sodimac Chile",
        "url": "https://www.sodimac.cl/sodimac-cl/search?Ntt=tubo%20conduit%2020%20mm",
        "fecha_revision": REVISION_DATE,
        "observacion": "Referencia para canalización, fijaciones y protecciones eléctricas menores.",
    },
    {
        "id": "mercadolibre_ponedero_copele",
        "proveedor": "MercadoLibre Chile",
        "url": "https://articulo.mercadolibre.cl/MLC-1379188913-ponedero-galvanizado-copele-12m-capacidad-100-gallinas-_JM",
        "fecha_revision": REVISION_DATE,
        "observacion": "Referencia de producto avícola; precio no recuperable por verificación anti-bot, por lo que escenarios usan estimación interna.",
    },
    {
        "id": "mercadolibre_nipple_b11",
        "proveedor": "MercadoLibre Chile",
        "url": "https://articulo.mercadolibre.cl/MLC-1778401396-pack-x10-bebedero-goteo-nipple-b-11-para-gallina-amarillo-_JM",
        "fecha_revision": REVISION_DATE,
        "observacion": "Referencia de producto avícola; precio no recuperable por verificación anti-bot, por lo que escenarios usan estimación interna.",
    },
]

RAW_QUOTES = [
    ["mallas_interiores", "0.60x25 m malla 3/4 hexagonal galvanizada", "Sodimac Chile", SOURCES[0]["url"], REVISION_DATE, 36562, "rollo 0,6 x 25 m", 2, 73124, "alto", "SKU 292699; precio fuente trazable"],
    ["mallas_interiores", "1.2x50 m malla 3/4 hexagonal galvanizada", "Sodimac Chile", SOURCES[0]["url"], REVISION_DATE, 124738, "rollo 1,2 x 50 m", 1, 124738, "alto", "SKU 706523; precio fuente trazable"],
    ["perchas_mallas", "Polín impregnado 75-100 mm x 2,44 m", "Sodimac Chile", SOURCES[1]["url"], REVISION_DATE, 4990, "unidad", 31, 154690, "alto", "SKU 75577X; 31 unidades cubren aprox. 75 m lineales"],
    ["almacenamiento", "Estante Repisa Rack plástico 4 niveles Rimax", "Sodimac Chile", SOURCES[2]["url"], REVISION_DATE, 55990, "unidad", 2, 111980, "alto", "Precio JSON-LD; se agregan protección/roedores en escenario base"],
    ["agua", "Manguera 25 m Tramontina", "Sodimac Chile", SOURCES[3]["url"], REVISION_DATE, 43990, "rollo 25 m", 1, 43990, "medio", "Referencia de distribución flexible"],
    ["agua", "Válvula bola 25 mm PVC", "Sodimac Chile", "https://www.sodimac.cl/sodimac-cl/search?Ntt=valvula%20bola%20pvc%2025%20mm", REVISION_DATE, 6590, "unidad", 4, 26360, "alto", "SKU 122610; referencia fittings"],
    ["energia", "Interruptor automático 10 A Lexo", "Sodimac Chile", "https://www.sodimac.cl/sodimac-cl/search?Ntt=interruptor%20automatico%2010a", REVISION_DATE, 2290, "unidad", 2, 4580, "medio", "Referencia protección eléctrica menor"],
    ["energia", "Pack 15 abrazaderas conduit 20 mm", "Sodimac Chile", SOURCES[4]["url"], REVISION_DATE, 1287, "pack 15", 3, 3861, "medio", "Referencia canalización/fijaciones"],
    ["bebederos", "Pack x10 bebedero nipple B-11", "MercadoLibre Chile", SOURCES[6]["url"], REVISION_DATE, None, "pack x10", 6, None, "bajo", "Precio no recuperable; usar estimación interna, requiere cotización"],
    ["nidos_ponederos", "Ponedero galvanizado Copele 1,2 m cap. 100 gallinas", "MercadoLibre Chile", SOURCES[5]["url"], REVISION_DATE, None, "unidad", 5, None, "bajo", "Precio no recuperable; usar estimación interna, requiere cotización"],
]

EQUIPMENT_SCENARIOS = {
    "bajo": {
        "descripcion": "Mínimo funcional, más fabricación en obra y productos económicos.",
        "items": {
            "comederos": {"subtotal_clp": 260_000, "cantidad": "40-50 m lineales fabricados", "confianza": "bajo", "observacion": "estimación interna, requiere cotización; canaletas/tolvas simples + soportes"},
            "bebederos": {"subtotal_clp": 168_000, "cantidad": "60 nipples + tubería básica", "confianza": "bajo", "observacion": "estimación interna, requiere cotización; referencia ML no entregó precio"},
            "nidos_ponederos": {"subtotal_clp": 350_000, "cantidad": "5 m² ponedero comunitario fabricado", "confianza": "bajo", "observacion": "estimación interna, requiere cotización; madera/OSB/fijaciones"},
            "perchas": {"subtotal_clp": 250_000, "cantidad": "75 m lineales", "confianza": "medio", "observacion": "basado en polines Sodimac + fijaciones"},
            "mallas_interiores": {"subtotal_clp": 125_000, "cantidad": "división mínima", "confianza": "medio", "observacion": "malla gallinero Sodimac + pocos soportes"},
            "almacenamiento_semanal": {"subtotal_clp": 120_000, "cantidad": "tarima/pallet + cierre/protección básica", "confianza": "bajo", "observacion": "estimación interna, requiere cotización"},
            "componentes_energia": {"subtotal_clp": 180_000, "cantidad": "cableado/canalización/protección mínima", "confianza": "bajo", "observacion": "estimación interna, requiere cotización; no incluye panel ni bomba"},
            "distribucion_agua": {"subtotal_clp": 120_000, "cantidad": "manguera/tubería/fittings mínimos", "confianza": "medio", "observacion": "referencias Sodimac de manguera y válvulas"},
            "logistica_contingencia": {"subtotal_clp": 150_000, "cantidad": "traslado/acopio/imprevistos mínimos", "confianza": "bajo", "observacion": "referencial por acceso invierno"},
        },
    },
    "base": {
        "descripcion": "Prudente, funcional y realista para operar 500 aves.",
        "items": {
            "comederos": {"subtotal_clp": 500_000, "cantidad": "22-24 comederos tipo plato/tolva o lineal equivalente", "confianza": "bajo", "observacion": "estimación interna, requiere cotización"},
            "bebederos": {"subtotal_clp": 322_000, "cantidad": "60 nipples + líneas + llaves + regulador/depósito", "confianza": "bajo", "observacion": "estimación interna, requiere cotización"},
            "nidos_ponederos": {"subtotal_clp": 900_000, "cantidad": "72 nidos fabricados o ponedero comunitario mejorado", "confianza": "bajo", "observacion": "estimación interna, requiere cotización"},
            "perchas": {"subtotal_clp": 350_000, "cantidad": "75 m lineales con soportes firmes", "confianza": "medio", "observacion": "polines Sodimac + fijaciones y merma"},
            "mallas_interiores": {"subtotal_clp": 260_000, "cantidad": "divisiones funcionales principales", "confianza": "medio", "observacion": "malla 1,2x50 + soportes/fijaciones"},
            "almacenamiento_semanal": {"subtotal_clp": 300_000, "cantidad": "2 racks/tarimas + protección contra humedad/roedores", "confianza": "medio", "observacion": "racks Sodimac + estimación interna de protección"},
            "componentes_energia": {"subtotal_clp": 420_000, "cantidad": "cables, canalización, conectores, protecciones, luces básicas e instalación", "confianza": "bajo", "observacion": "estimación interna, requiere cotización; no incluye panel ni bomba"},
            "distribucion_agua": {"subtotal_clp": 220_000, "cantidad": "manguera/tubería/fittings/llaves/regulador", "confianza": "medio", "observacion": "referencias Sodimac + estimación instalación"},
            "logistica_contingencia": {"subtotal_clp": 300_000, "cantidad": "acopio/traslado adicional/ripio menor imprevisto", "confianza": "bajo", "observacion": "referencial por invierno"},
        },
    },
    "alto": {
        "descripcion": "Más holgura, mayor durabilidad y componentes más completos.",
        "items": {
            "comederos": {"subtotal_clp": 960_000, "cantidad": "24 unidades mejor calidad/mayor capacidad", "confianza": "bajo", "observacion": "estimación interna, requiere cotización"},
            "bebederos": {"subtotal_clp": 600_000, "cantidad": "sistema automático con mayor holgura/filtros/repuestos", "confianza": "bajo", "observacion": "estimación interna, requiere cotización"},
            "nidos_ponederos": {"subtotal_clp": 2_000_000, "cantidad": "módulos comerciales o fabricación reforzada", "confianza": "bajo", "observacion": "estimación interna, requiere cotización; referencia Copele sin precio recuperable"},
            "perchas": {"subtotal_clp": 550_000, "cantidad": "75 m lineales reforzados", "confianza": "medio", "observacion": "polines/perfiles/fijaciones con mayor holgura"},
            "mallas_interiores": {"subtotal_clp": 550_000, "cantidad": "mayor sectorización", "confianza": "medio", "observacion": "más rollos/soportes/perfiles/fijaciones"},
            "almacenamiento_semanal": {"subtotal_clp": 600_000, "cantidad": "racks/contención/protección superior", "confianza": "bajo", "observacion": "estimación interna, requiere cotización"},
            "componentes_energia": {"subtotal_clp": 750_000, "cantidad": "instalación más completa para bomba, luces y cámaras", "confianza": "bajo", "observacion": "estimación interna, requiere cotización; no incluye panel ni bomba"},
            "distribucion_agua": {"subtotal_clp": 400_000, "cantidad": "red interna con llaves, regulador, flotador y repuestos", "confianza": "medio", "observacion": "referencias Sodimac + estimación instalación"},
            "logistica_contingencia": {"subtotal_clp": 600_000, "cantidad": "mayor contingencia por invierno/acceso", "confianza": "bajo", "observacion": "referencial"},
        },
    },
}

for scenario in EQUIPMENT_SCENARIOS.values():
    scenario["total_clp"] = sum(item["subtotal_clp"] for item in scenario["items"].values())

CAPEX_TOTAL = {}
for key, scenario in EQUIPMENT_SCENARIOS.items():
    total = KNOWN_CAPEX["subtotal_conocido_clp"] + scenario["total_clp"]
    CAPEX_TOTAL[key] = {
        "capex_conocido_clp": KNOWN_CAPEX["subtotal_conocido_clp"],
        "equipamiento_clp": scenario["total_clp"],
        "capex_total_referencial_clp": total,
        "capacidad_inversion_propia_clp": KNOWN_CAPEX["capacidad_inversion_propia_clp"],
        "deficit_o_excedente_clp": KNOWN_CAPEX["capacidad_inversion_propia_clp"] - total,
        "lectura": "déficit" if total > KNOWN_CAPEX["capacidad_inversion_propia_clp"] else "excedente",
    }

MARGEN_SIN_MO = INGRESO_MENSUAL_BASE - OPEX_SIN_MO
MARGEN_CON_MO = INGRESO_MENSUAL_BASE - OPEX_CON_MO
BREAKEVEN_SIN_MO_MES = OPEX_SIN_MO / PRICE_AVG
BREAKEVEN_CON_MO_MES = OPEX_CON_MO / PRICE_AVG

PAYBACK = {}
for key, values in CAPEX_TOTAL.items():
    capex = values["capex_total_referencial_clp"]
    PAYBACK[key] = {
        "capex_total_referencial_clp": capex,
        "margen_mensual_sin_mano_obra_clp": MARGEN_SIN_MO,
        "payback_simple_sin_mano_obra_meses": round(capex / MARGEN_SIN_MO, 2),
        "margen_mensual_con_mano_obra_clp": MARGEN_CON_MO,
        "payback_simple_con_mano_obra_meses": round(capex / MARGEN_CON_MO, 2),
    }

FLOWS = {}
for key, values in CAPEX_TOTAL.items():
    capex = values["capex_total_referencial_clp"]
    rows = [{"mes": 0, "ingresos_clp": 0, "opex_sin_mano_obra_clp": 0, "opex_con_mano_obra_clp": 0, "flujo_sin_mano_obra_clp": -capex, "flujo_con_mano_obra_clp": -capex, "acumulado_sin_mano_obra_clp": -capex, "acumulado_con_mano_obra_clp": -capex}]
    acc_without = -capex
    acc_with = -capex
    for month in range(1, 13):
        acc_without += MARGEN_SIN_MO
        acc_with += MARGEN_CON_MO
        rows.append({
            "mes": month,
            "ingresos_clp": INGRESO_MENSUAL_BASE,
            "opex_sin_mano_obra_clp": OPEX_SIN_MO,
            "opex_con_mano_obra_clp": OPEX_CON_MO,
            "flujo_sin_mano_obra_clp": MARGEN_SIN_MO,
            "flujo_con_mano_obra_clp": MARGEN_CON_MO,
            "acumulado_sin_mano_obra_clp": acc_without,
            "acumulado_con_mano_obra_clp": acc_with,
        })
    FLOWS[key] = rows

STRATEGIES = {
    "comprar_352_de_una_vez": {
        "pollonas": 352,
        "capex_pollonas_clp": 4_224_000,
        "semaforo": "amarillo/alto riesgo si falta financiamiento",
        "ventajas": ["llega más rápido a 500 aves", "captura antes ingreso meta", "simplifica planificación"],
        "riesgos": ["exige más capital inicial", "aumenta presión comercial inmediata", "requiere equipamiento completo desde el inicio", "mayor riesgo sanitario/logístico/de venta", "supera probablemente los $10 millones disponibles al agregar equipamiento y capital de trabajo"],
        "lectura": "Puede ser viable solo si se asegura financiamiento suficiente para equipamiento, alimento inicial y contingencia, y si la venta de 100 bandejas está realmente confirmada al contado.",
    },
    "100_primero": {"pollonas": 100, "capex_pollonas_clp": 1_200_000, "semaforo": "menor riesgo financiero", "lectura": "Permite validar mercado, operación y equipamiento proporcional con menor presión de caja; crecimiento más lento."},
    "150_primero": {"pollonas": 150, "capex_pollonas_clp": 1_800_000, "semaforo": "riesgo intermedio", "lectura": "Compromiso balanceado: más avance que 100, todavía bajo la compra total; exige plan de equipamiento por etapas."},
    "200_primero": {"pollonas": 200, "capex_pollonas_clp": 2_400_000, "semaforo": "riesgo medio/alto", "lectura": "Acelera crecimiento, pero aumenta OPEX, equipamiento y venta requerida; usar solo con compradores más confirmados."},
}

MANDATORY_CAPEX_TEXT = "El subtotal conocido de galpón + pollonas ya consume casi todo el máximo informado de $10.000.000; cualquier equipamiento, capital de trabajo o contingencia requiere financiamiento, aporte adicional o compra por etapas."
OPEX_WARNING = "OPEX proyectado preliminar; falta validar sanidad de escala, mantenciones, reposición por mortalidad, costos tributarios/sanitarios efectivos y variaciones de alimento."


def write_json(rel: str, data: dict) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_csv(rel: str, header: list[str], rows: list[list[object]]) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


cotizacion = {
    "proyecto": "Gallinero Nacho",
    "fase": "P45-P46",
    "estado": "referencial_preliminar",
    "fecha_revision": REVISION_DATE,
    "advertencia": "Precios web referenciales y estimaciones internas cuando no se encontró precio fuente. No ejecutar compra sin cotización final.",
    "fuentes": SOURCES,
    "cotizaciones": [dict(zip(["item", "producto", "proveedor", "url", "fecha_revision", "precio_unitario_clp", "unidad_compra", "cantidad_usada", "subtotal_clp", "nivel_confianza", "observacion"], row)) for row in RAW_QUOTES],
    "escenarios": EQUIPMENT_SCENARIOS,
}
write_json("dashboard/data/cotizacion-referencial-equipamiento-avicola.json", cotizacion)

capex_total_json = {
    "proyecto": "Gallinero Nacho",
    "fase": "P45-P46",
    "estado": "referencial_preliminar/amarillo",
    "capex_conocido": KNOWN_CAPEX,
    "equipamiento_escenarios": {key: {"total_clp": value["total_clp"], "descripcion": value["descripcion"], "items": value["items"]} for key, value in EQUIPMENT_SCENARIOS.items()},
    "capex_total_referencial": CAPEX_TOTAL,
    "capital_trabajo_inicial": {"un_mes_opex_con_mano_obra_clp": OPEX_CON_MO, "dos_meses_opex_con_mano_obra_clp": OPEX_CON_MO * 2, "nota": "No confundir con CAPEX."},
    "texto_obligatorio": MANDATORY_CAPEX_TEXT,
    "decision": "No desbloquea compra de aves, construcción ni inversión mayor.",
}
write_json("dashboard/data/capex-total-referencial-500.json", capex_total_json)

opex_json = {
    "proyecto": "Gallinero Nacho",
    "fase": "P45-P46",
    "estado": "preliminar/amarillo",
    "objetivo_aves": 500,
    "componentes_sin_mano_obra": OPEX,
    "subtotal_sin_mano_obra_clp_mes": OPEX_SIN_MO,
    "mano_obra_economica": {"horas_diarias": 3, "costo_diario_referencial_clp": 20_000, "dias_mes": 30, "subtotal_clp_mes": MANO_OBRA},
    "subtotal_con_mano_obra_clp_mes": OPEX_CON_MO,
    "imprevistos_operativos": {
        "cinco_por_ciento_sobre_opex_sin_mano_obra_clp": IMP_5,
        "diez_por_ciento_sobre_opex_sin_mano_obra_clp": IMP_10,
        "total_sin_mano_obra_mas_5_clp": OPEX_SIN_MO + IMP_5,
        "total_sin_mano_obra_mas_10_clp": OPEX_SIN_MO + IMP_10,
        "total_con_mano_obra_mas_5_clp": OPEX_CON_MO + IMP_5,
        "total_con_mano_obra_mas_10_clp": OPEX_CON_MO + IMP_10,
    },
    "advertencia": OPEX_WARNING,
}
write_json("dashboard/data/opex-proyectado-500.json", opex_json)

ingresos_json = {
    "proyecto": "Gallinero Nacho",
    "fase": "P45-P46",
    "estado": "preliminar/amarillo",
    "precio_promedio_actual_clp_bandeja": PRICE_AVG,
    "mix_actual": {"segunda": 6, "primera": 13, "extra": 9},
    "precios_confirmados_clp": {"segunda": 5000, "primera": 6000, "extra": 7000},
    "sensibilidades": INGRESOS,
    "nota": "Todas las ventas se modelan al contado. 100 bandejas/semana es venta segura o casi segura según dato informado.",
}
write_json("dashboard/data/ingresos-proyectados-500.json", ingresos_json)

flujo_json = {
    "proyecto": "Gallinero Nacho",
    "fase": "P45-P46",
    "estado": "preliminar_referencial/amarillo",
    "base_calculo": {"ingreso_mensual_base_clp": INGRESO_MENSUAL_BASE, "opex_sin_mano_obra_clp_mes": OPEX_SIN_MO, "opex_con_mano_obra_clp_mes": OPEX_CON_MO, "precio_promedio_clp_bandeja": PRICE_AVG},
    "margenes": {"sin_mano_obra_clp_mes": MARGEN_SIN_MO, "con_mano_obra_clp_mes": MARGEN_CON_MO},
    "payback_simple": PAYBACK,
    "punto_equilibrio": {
        "sin_mano_obra_bandejas_mes": round(BREAKEVEN_SIN_MO_MES, 1),
        "sin_mano_obra_bandejas_semana": round(BREAKEVEN_SIN_MO_MES * 12 / 52, 1),
        "con_mano_obra_bandejas_mes": round(BREAKEVEN_CON_MO_MES, 1),
        "con_mano_obra_bandejas_semana": round(BREAKEVEN_CON_MO_MES * 12 / 52, 1),
    },
    "flujo_12_meses": FLOWS,
    "van_tir": "no calculado por falta de tasa, vida útil y calendario definitivo",
    "advertencia": "Flujo mensual preliminar referencial; no declara decisión final verde.",
}
write_json("dashboard/data/flujo-financiero-preliminar-500.json", flujo_json)

estrategia_json = {
    "proyecto": "Gallinero Nacho",
    "fase": "P45-P46",
    "estado": "recomendacion_preliminar/amarillo",
    "precio_pollona_clp": 12_000,
    "pollonas_faltantes": 352,
    "estrategias": STRATEGIES,
    "comparacion": {
        "comprar_todas": "amarillo/alto riesgo si falta financiamiento; exige equipamiento completo, OPEX y capital de trabajo desde el inicio.",
        "comprar_por_etapas": "menor riesgo financiero y comercial, crecimiento más lento, permite validar ventas y operación.",
    },
    "recomendacion_preliminar": "No recomendar automáticamente comprar 352 de una vez: el CAPEX total base más capital de trabajo supera el máximo propio de $10 millones. Recomendación técnica preliminar: compra por etapas, idealmente 150 primero o 100 primero si la venta todavía no está confirmada por canal; comprar todas solo con financiamiento cerrado y venta de 100 bandejas realmente confirmada al contado.",
}
write_json("dashboard/data/estrategia-compra-pollonas.json", estrategia_json)

# CSVs
write_csv("datos/entrada/capex/cotizaciones-referenciales-equipamiento-avicola.csv", ["item", "producto", "proveedor", "url", "fecha_revision", "precio_unitario_clp", "unidad_compra", "cantidad_usada", "subtotal_clp", "nivel_confianza", "observacion"], RAW_QUOTES)
write_csv(
    "datos/procesados/indicadores/p0-capex-referencial-500.csv",
    ["escenario", "capex_conocido_clp", "equipamiento_clp", "capex_total_referencial_clp", "capacidad_inversion_propia_clp", "deficit_o_excedente_clp", "lectura"],
    [[k, v["capex_conocido_clp"], v["equipamiento_clp"], v["capex_total_referencial_clp"], v["capacidad_inversion_propia_clp"], v["deficit_o_excedente_clp"], v["lectura"]] for k, v in CAPEX_TOTAL.items()],
)
write_csv("datos/procesados/indicadores/p0-opex-proyectado-500.csv", ["indicador", "valor_clp_mes", "observacion"], [["opex_sin_mano_obra", OPEX_SIN_MO, "subtotal mensual proyectado 500 aves"], ["mano_obra_economica", MANO_OBRA, "Nacho solo: $20.000 diarios x 30"], ["opex_con_mano_obra", OPEX_CON_MO, "subtotal con mano de obra económica"], ["imprevistos_5", IMP_5, "5% sobre OPEX sin mano de obra"], ["imprevistos_10", IMP_10, "10% sobre OPEX sin mano de obra"]])
write_csv("datos/procesados/indicadores/p0-flujo-financiero-preliminar-500.csv", ["escenario", "ingreso_mensual_base_clp", "opex_sin_mano_obra_clp", "opex_con_mano_obra_clp", "margen_sin_mano_obra_clp", "margen_con_mano_obra_clp", "payback_sin_mano_obra_meses", "payback_con_mano_obra_meses", "pe_sin_mano_obra_bandejas_semana", "pe_con_mano_obra_bandejas_semana"], [[k, INGRESO_MENSUAL_BASE, OPEX_SIN_MO, OPEX_CON_MO, MARGEN_SIN_MO, MARGEN_CON_MO, v["payback_simple_sin_mano_obra_meses"], v["payback_simple_con_mano_obra_meses"], round(BREAKEVEN_SIN_MO_MES * 12 / 52, 1), round(BREAKEVEN_CON_MO_MES * 12 / 52, 1)] for k, v in PAYBACK.items()])

# Update existing JSONs conservatively
capex_eq = read_json("dashboard/data/capex-equipamiento-avicola.json")
capex_eq.update({
    "fase": "P0 — Diagnóstico real / P45-P46",
    "estado": "referencial_preliminar; requiere cotización final",
    "descripcion": "CAPEX equipamiento avícola referencial bajo/base/alto para 500 aves, con fuentes web cuando existieron y estimaciones internas explícitas cuando no se recuperó precio.",
    "fuentes": SOURCES,
    "escenarios": EQUIPMENT_SCENARIOS,
    "resumen": {
        **capex_eq.get("resumen", {}),
        "capex_equipamiento_bajo_clp": EQUIPMENT_SCENARIOS["bajo"]["total_clp"],
        "capex_equipamiento_base_clp": EQUIPMENT_SCENARIOS["base"]["total_clp"],
        "capex_equipamiento_alto_clp": EQUIPMENT_SCENARIOS["alto"]["total_clp"],
        "estado_capex_total": "referencial preliminar P45-P46; no habilita inversión",
    },
})
capex_eq["items"] = [
    {"id": item_id, "item": item_id.replace("_", " "), "estado": "valorizado_referencial", "requerimiento": value["cantidad"], "bajo_clp": EQUIPMENT_SCENARIOS["bajo"]["items"].get(item_id, {}).get("subtotal_clp"), "base_clp": EQUIPMENT_SCENARIOS["base"]["items"].get(item_id, {}).get("subtotal_clp"), "alto_clp": EQUIPMENT_SCENARIOS["alto"]["items"].get(item_id, {}).get("subtotal_clp"), "observacion": value["observacion"]}
    for item_id, value in EQUIPMENT_SCENARIOS["base"]["items"].items()
]
write_json("dashboard/data/capex-equipamiento-avicola.json", capex_eq)

capex_pre = read_json("dashboard/data/capex-preliminar.json")
capex_pre.update({"fase": "P0 — Diagnóstico real / P45-P46", "estado": "referencial_preliminar/amarillo"})
capex_pre["capex_referencial_500_p45_p46"] = capex_total_json
capex_pre["conclusion"] = f"P45-P46 calcula CAPEX total referencial bajo/base/alto para 500 aves. {MANDATORY_CAPEX_TEXT} No se autoriza compra de aves, construcción ni inversión mayor."
for key in ["capex_equipamiento_avicola", "capex_total_proyecto", "capital_trabajo_inicial"]:
    for ind in capex_pre.get("indicadores_financieros_capex", []):
        if ind.get("id") == key:
            ind["estado"] = "referencial_preliminar" if key != "capital_trabajo_inicial" else "separado_de_capex"
            if key == "capex_equipamiento_avicola":
                ind["valor"] = EQUIPMENT_SCENARIOS["base"]["total_clp"]
                ind["descripcion_corta"] = "CAPEX equipamiento avícola escenario base P45-P46."
            elif key == "capex_total_proyecto":
                ind["valor"] = CAPEX_TOTAL["base"]["capex_total_referencial_clp"]
                ind["descripcion_corta"] = "CAPEX total referencial base: galpón + pollonas + equipamiento base."
            else:
                ind["valor"] = OPEX_CON_MO
                ind["descripcion_corta"] = "Capital de trabajo inicial mínimo: 1 mes de OPEX con mano de obra; no es CAPEX."
write_json("dashboard/data/capex-preliminar.json", capex_pre)

fin = read_json("dashboard/data/finanzas-preliminares.json")
fin.update({"fase": "P0 — Diagnóstico real / P45-P46", "estado": "preliminar_referencial"})
fin["resumen_p45_p46"] = {"capex_total_referencial": CAPEX_TOTAL, "opex": opex_json, "ingresos": INGRESOS, "flujo": {"margenes": flujo_json["margenes"], "payback_simple": PAYBACK, "punto_equilibrio": flujo_json["punto_equilibrio"]}}
existing = {item.get("indicador") for item in fin.get("indicadores", [])}
new_indicators = [
    ("opex_proyectado_500_sin_mano_obra", OPEX_SIN_MO, "CLP/mes", "OPEX proyectado 500 sin mano de obra"),
    ("opex_proyectado_500_con_mano_obra", OPEX_CON_MO, "CLP/mes", "OPEX proyectado 500 con mano de obra económica"),
    ("ingreso_mensual_meta_100_bandejas", INGRESO_MENSUAL_BASE, "CLP/mes", "100 bandejas/semana x $6.107 x 52/12"),
    ("margen_500_sin_mano_obra", MARGEN_SIN_MO, "CLP/mes", "ingreso mensual base - OPEX sin mano de obra"),
    ("margen_500_con_mano_obra", MARGEN_CON_MO, "CLP/mes", "ingreso mensual base - OPEX con mano de obra"),
    ("capex_total_referencial_base_500", CAPEX_TOTAL["base"]["capex_total_referencial_clp"], "CLP", "galpón + pollonas + equipamiento base"),
]
for indicador, valor, unidad, obs in new_indicators:
    if indicador not in existing:
        fin.setdefault("indicadores", []).append({"indicador": indicador, "valor": valor, "unidad": unidad, "formula": obs, "fuente": "P45-P46", "estado": "preliminar_referencial", "observacion": obs})
fin["conclusion"] = "P45-P46 agrega flujo financiero preliminar referencial, payback simple y punto de equilibrio, sin VAN/TIR definitivos. Estado sigue amarillo."
write_json("dashboard/data/finanzas-preliminares.json", fin)

flujo_old = read_json("dashboard/data/flujo-caja-preliminar.json")
flujo_old.update({"fase": "P0 — Diagnóstico real / P45-P46", "estado": "preliminar_referencial/amarillo"})
flujo_old["proyeccion_p45_p46"] = flujo_json
flujo_old["costos_actuales"]["opex_proyectado_500_sin_mano_obra_clp"] = OPEX_SIN_MO
flujo_old["costos_actuales"]["opex_proyectado_500_con_mano_obra_clp"] = OPEX_CON_MO
flujo_old["mano_obra_referencial"] = {"monto_clp": MANO_OBRA, "formula": "20.000 x 30", "nota": "costo económico/referencial; Nacho trabajaría solo"}
flujo_old["margenes_preliminares_500"] = {"sin_mano_obra_clp": MARGEN_SIN_MO, "con_mano_obra_clp": MARGEN_CON_MO}
flujo_old["conclusion"] = "P45-P46 prepara flujo financiero mensual preliminar para 500 aves con CAPEX bajo/base/alto, OPEX actualizado, payback simple y punto de equilibrio. No se calcula VAN/TIR definitivo por falta de tasa, vida útil y calendario definitivo. Estado sigue amarillo."
write_json("dashboard/data/flujo-caja-preliminar.json", flujo_old)

res = read_json("dashboard/data/resumen-ejecutivo-p0.json")
res.update({"fase": "P0 — Diagnóstico real / P45-P46", "estado_general": "amarillo"})
for point in ["P45-P46 calcula CAPEX equipamiento referencial bajo/base/alto.", "OPEX proyectado 500 con mano de obra económica: $1.686.750/mes.", "Ingreso mensual meta 100 bandejas: $2.646.367 aprox.", "Flujo preliminar muestra margen positivo, pero requiere financiamiento y validación comercial."]:
    if point not in res["puntos_favorables"]:
        res["puntos_favorables"].append(point)
for risk in ["El subtotal conocido de galpón + pollonas ya consume casi todo el máximo informado de $10.000.000.", "Comprar 352 pollonas de una vez es amarillo/alto riesgo si no hay financiamiento completo y venta confirmada."]:
    if risk not in res["riesgos_principales"]:
        res["riesgos_principales"].append(risk)
res["capex_total_referencial_p45_p46"] = CAPEX_TOTAL
res["conclusion"] = "P46 preliminar calculado con precios referenciales; requiere validación final antes de ejecutar. Estado sigue amarillo: no se autoriza compra de aves, construcción ni inversión mayor."
write_json("dashboard/data/resumen-ejecutivo-p0.json", res)

alerts = read_json("dashboard/data/alertas-p0.json")
alerts.update({"fase": "P0 — Diagnóstico real / P45-P46"})
for new_alert in [
    {"id": "A22", "titulo": "CAPEX total referencial supera capacidad propia", "severidad": "alta", "dimension": "financiera", "descripcion": MANDATORY_CAPEX_TEXT, "estado": "bloqueante"},
    {"id": "A23", "titulo": "OPEX 500 actualizado sigue preliminar", "severidad": "alta", "dimension": "financiera", "descripcion": OPEX_WARNING, "estado": "abierta"},
    {"id": "A24", "titulo": "Compra 352 pollonas de una vez requiere financiamiento cerrado", "severidad": "alta", "dimension": "decision", "descripcion": "Comprar todas puede ser viable solo si se asegura financiamiento suficiente para equipamiento, alimento inicial y contingencia, y si la venta de 100 bandejas está realmente confirmada al contado.", "estado": "bloqueante"},
]:
    if not any(a.get("id") == new_alert["id"] for a in alerts["alertas"]):
        alerts["alertas"].append(new_alert)
alerts["nota"] = "Alertas P45-P46: CAPEX/OPEX/flujo referenciales calculados; estado amarillo y decisiones mayores bloqueadas."
write_json("dashboard/data/alertas-p0.json", alerts)

falt = read_json("dashboard/data/datos-faltantes.json")
falt.update({"fase": "P0 — Diagnóstico real / P45-P46", "estado": "preliminar_referencial"})
falt["nota"] = "P45-P46 reduce incertidumbre financiera con referencias y estimaciones explícitas, pero faltan cotizaciones formales finales, validación legal/sanitaria/tributaria, confirmación comercial por canal y calendario real de inversión."
falt["grupos"] = [
    {"grupo": "cotizaciones finales", "prioridad": "alta", "items": ["confirmar precios reales de comederos, bebederos y ponederos", "cotizar instalación eléctrica/energía con visita", "cotizar distribución interna de agua", "validar costos logísticos de invierno"]},
    {"grupo": "validación comercial", "prioridad": "alta", "items": ["confirmar compradores para 100 bandejas/semana", "precios netos por canal", "forma de pago al contado por canal", "capacidad de vender 104,1 bandejas si se ocupa producción completa"]},
    {"grupo": "formalización", "prioridad": "alta", "items": ["validar si 500 aves requiere patente/permiso/resolución sanitaria", "validar factura/boleta y costos tributarios reales", "definir trazabilidad mínima"]},
    {"grupo": "ejecución financiera", "prioridad": "alta", "items": ["financiamiento para déficit CAPEX", "capital de trabajo 1-2 meses", "calendario de compra por etapas", "tasa y vida útil para VAN/TIR si se requiere"]},
]
write_json("dashboard/data/datos-faltantes.json", falt)

sem = read_json("dashboard/data/semaforo-decision.json")
sem.update({"fase": "P0 — Diagnóstico real / P45-P46", "estado": "amarillo", "semaforo_general": "amarillo", "conclusion": "P45-P46 entrega cálculo referencial, pero no desbloquea inversión. Comprar todas las pollonas queda amarillo/alto riesgo sin financiamiento y venta confirmada; compra por etapas reduce riesgo."})
sem["dimensiones"]["financiera"] = {"estado": "amarillo/preliminar_referencial", "nota": "CAPEX/OPEX/flujo preliminares calculados; falta cotización final, capital de trabajo y validación comercial/legal."}
sem["condiciones_para_avanzar"] = ["cotizaciones finales de equipamiento e instalaciones", "financiamiento definido para CAPEX + capital de trabajo", "ventas 100 bandejas/semana confirmadas al contado", "validación legal/sanitaria/tributaria", "plan de compra por etapas o justificación financiera para comprar 352 de una vez"]
write_json("dashboard/data/semaforo-decision.json", sem)

estado = read_json("dashboard/data/estado-proyecto.json")
estado.update({"fase": "P0 — Diagnóstico real / P45-P46", "semaforo_general": "amarillo", "decision_actual": "P45-P46 calcula CAPEX/OPEX/flujo y estrategia pollonas en forma preliminar. No habilita P1, compra, construcción ni inversión mayor."})
estado["proximos_pasos"] = ["validar cotizaciones finales de equipamiento", "confirmar financiamiento para déficit y capital de trabajo", "validar venta real de 100 bandejas/semana al contado", "validar obligaciones legales/sanitarias/tributarias", "definir compra por etapas vs 352 de una vez con financiamiento cerrado"]
write_json("dashboard/data/estado-proyecto.json", estado)

# Markdown report/docs
capex_lines = "\n".join([f"- {k}: equipamiento ${v['equipamiento_clp']:,} / total ${v['capex_total_referencial_clp']:,} / diferencia vs $10.000.000: ${v['deficit_o_excedente_clp']:,}" for k, v in CAPEX_TOTAL.items()])
payback_lines = "\n".join([f"- {k}: {v['payback_simple_sin_mano_obra_meses']} meses sin mano de obra / {v['payback_simple_con_mano_obra_meses']} meses con mano de obra" for k, v in PAYBACK.items()])
report = f"""# P45-P46 — CAPEX, OPEX, flujo preliminar y estrategia de pollonas

Estado general: **AMARILLO**. No se desbloquea compra de aves, construcción ni inversión mayor.

## Fuentes principales usadas

- Sodimac Chile: mallas gallinero, polines impregnados, racks/estantes, mangueras, válvulas, conduit y protecciones menores.
- MercadoLibre Chile: referencias de productos avícolas (bebedero nipple y ponedero Copele), pero el sitio redirigió a verificación y no entregó precio; esos montos quedan como **estimación interna, requiere cotización**.

## CAPEX conocido

- Galpón COT-GN-0035: **$5.547.765**.
- Pollonas faltantes: **352 x $12.000 = $4.224.000**.
- Subtotal conocido: **$9.771.765**.

{MANDATORY_CAPEX_TEXT}

## CAPEX equipamiento referencial

- Bajo: **${EQUIPMENT_SCENARIOS['bajo']['total_clp']:,}**.
- Base: **${EQUIPMENT_SCENARIOS['base']['total_clp']:,}**.
- Alto: **${EQUIPMENT_SCENARIOS['alto']['total_clp']:,}**.

## CAPEX total referencial 500 aves

{capex_lines}

## Capital de trabajo inicial separado de CAPEX

- 1 mes OPEX con mano de obra: **${OPEX_CON_MO:,}**.
- 2 meses OPEX con mano de obra: **${OPEX_CON_MO * 2:,}**.

## OPEX proyectado 500 aves

- Sin mano de obra: **${OPEX_SIN_MO:,}/mes**.
- Mano de obra económica Nacho: **${MANO_OBRA:,}/mes**.
- Con mano de obra: **${OPEX_CON_MO:,}/mes**.
- Imprevistos 5% sobre OPEX sin mano de obra: **${IMP_5:,}**.
- Imprevistos 10% sobre OPEX sin mano de obra: **${IMP_10:,}**.

> {OPEX_WARNING}

## Ingresos proyectados

- Base 100 bandejas/semana a $6.107: **${INGRESO_MENSUAL_BASE:,}/mes**.
- Conservador 90 bandejas/semana: **${INGRESOS['conservador_90']['ingreso_mensual_clp']:,}/mes**.
- Descuento almacenes 10% sobre 30 bandejas/semana: **${INGRESOS['descuento_almacenes']['ingreso_mensual_clp']:,}/mes**.
- Alto 104,1 bandejas/semana: **${INGRESOS['alto_104_1']['ingreso_mensual_clp']:,}/mes**.

## Flujo financiero preliminar

- Margen mensual sin mano de obra: **${MARGEN_SIN_MO:,}**.
- Margen mensual con mano de obra: **${MARGEN_CON_MO:,}**.
- Punto equilibrio sin mano de obra: **{round(BREAKEVEN_SIN_MO_MES, 1)} bandejas/mes** / **{round(BREAKEVEN_SIN_MO_MES * 12 / 52, 1)} bandejas/semana**.
- Punto equilibrio con mano de obra: **{round(BREAKEVEN_CON_MO_MES, 1)} bandejas/mes** / **{round(BREAKEVEN_CON_MO_MES * 12 / 52, 1)} bandejas/semana**.

### Payback simple

{payback_lines}

VAN/TIR: **no calculado** por falta de tasa, vida útil y calendario definitivo.

## Estrategia de compra de pollonas

- 100 primero: **$1.200.000**.
- 150 primero: **$1.800.000**.
- 200 primero: **$2.400.000**.
- 352 de una vez: **$4.224.000**.

Comprar todas puede ser viable solo si se asegura financiamiento suficiente para equipamiento, alimento inicial y contingencia, y si la venta de 100 bandejas está realmente confirmada al contado.

**Recomendación técnica preliminar:** no comprar automáticamente las 352 de una vez. Con los números actuales, el CAPEX total base + capital de trabajo supera el máximo propio de $10.000.000. Conviene compra por etapas (100-150 primero; 200 solo con compradores más confirmados), salvo financiamiento cerrado y venta confirmada.

## Pendientes para pasar a verde

- Cotizaciones finales de equipamiento avícola, agua, energía e instalación.
- Confirmar venta real de 100 bandejas/semana al contado y por canal.
- Validación legal/sanitaria/tributaria: informado por Nacho, pendiente de validación.
- Financiamiento para déficit CAPEX + capital de trabajo.
- Plan logístico de invierno.
- Calendario real de inversión y compra de aves.
"""
for rel in [
    "reports/p45_p46_capex_opex_flujo_y_estrategia_pollonas.md",
    "docs/01-p0-diagnostico/capex-preliminar.md",
    "docs/01-p0-diagnostico/flujo-caja-preliminar.md",
    "docs/02-informes/informe-ejecutivo-nacho-500.md",
]:
    (ROOT / rel).write_text(report, encoding="utf-8")

faltantes_md = f"""# Datos faltantes P45-P46 — Proyecto Gallinero Nacho

P45-P46 calcula CAPEX/OPEX/flujo preliminar, pero el estado sigue **AMARILLO**.

## Ya calculado

- CAPEX equipamiento bajo/base/alto: ${EQUIPMENT_SCENARIOS['bajo']['total_clp']:,} / ${EQUIPMENT_SCENARIOS['base']['total_clp']:,} / ${EQUIPMENT_SCENARIOS['alto']['total_clp']:,}.
- CAPEX total bajo/base/alto: ${CAPEX_TOTAL['bajo']['capex_total_referencial_clp']:,} / ${CAPEX_TOTAL['base']['capex_total_referencial_clp']:,} / ${CAPEX_TOTAL['alto']['capex_total_referencial_clp']:,}.
- OPEX sin mano de obra: ${OPEX_SIN_MO:,}/mes.
- OPEX con mano de obra: ${OPEX_CON_MO:,}/mes.
- Ingreso mensual meta: ${INGRESO_MENSUAL_BASE:,}.
- Payback simple y punto de equilibrio preliminares.
- Estrategia 352 de una vez vs 100/150/200 por etapas.

## Sigue faltando

- Cotización formal final de comederos, bebederos, nidos/ponederos e instalación.
- Validación legal/sanitaria/tributaria: Nacho informa que cree no requerir patente/permiso/resolución para 500, pero queda pendiente de validación.
- Confirmación comercial por canal para 100 bandejas/semana al contado.
- Financiamiento para CAPEX total + capital de trabajo.
- Logística/acceso invierno con costo real.
- Calendario real de compra por etapas.
"""
(ROOT / "docs/01-p0-diagnostico/datos-faltantes.md").write_text(faltantes_md, encoding="utf-8")

print("P45-P46 data generated")

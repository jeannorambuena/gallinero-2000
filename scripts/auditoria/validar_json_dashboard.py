#!/usr/bin/env python3
"""Valida existencia, sintaxis y estructura mínima de JSON del dashboard P0."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path.cwd()

SPECS = {
    "dashboard/data/resumen-ejecutivo-p0.json": {
        "required": ["proyecto", "fase", "estado_general", "avance_p0_estimado", "decision_actual", "conclusion"],
        "non_empty_lists": ["puntos_favorables", "riesgos_principales", "decisiones_bloqueadas", "faltantes_para_p1_preliminar", "acciones_recomendadas"],
    },
    "dashboard/data/desbloqueo-p1-preliminar.json": {
        "required": ["proyecto", "fase_actual", "estado_desbloqueo", "objetivo", "proximo_paso_recomendado", "conclusion"],
        "non_empty_lists": ["tareas_por_dimension", "documentos_creados", "plantillas_csv", "criterios_para_habilitar_p1_preliminar", "decisiones_bloqueadas"],
    },
    "dashboard/data/replanteo-escala.json": {
        "required": ["proyecto", "fase", "escenario_anterior", "escenario_base_actual", "regla_decision_inversion", "resumen_impactos", "conclusion"],
        "non_empty_lists": ["escenarios_comparativos"],
    },
    "dashboard/data/matriz-decision-inversion.json": {
        "required": ["proyecto", "regla_general", "decision_actual", "inversion_mayor_autorizada", "compra_aves_autorizada", "conclusion"],
        "non_empty_lists": ["colores"],
    },
    "dashboard/data/estimacion-galpones.json": {
        "required": ["proyecto", "supuestos", "densidad_ref_aves_m2", "conclusion"],
        "non_empty_lists": ["escenarios", "categorias_pendientes"],
    },
    "dashboard/data/estado-proyecto.json": {
        "required_any": [("fase", "fase_actual")],
        "required": ["proyecto", "avance_p0_estimado", "semaforo_general"],
        "non_empty_lists": ["proximos_pasos"],
    },
    "dashboard/data/indicadores-productivos.json": {
        "required": ["proyecto", "fase", "estado"],
        "non_empty_lists": ["indicadores"],
    },
    "dashboard/data/indicadores-comerciales.json": {
        "required": ["proyecto", "fase", "estado", "resumen"],
        "non_empty_lists": ["indicadores"],
    },
    "dashboard/data/finanzas-preliminares.json": {
        "required": ["proyecto", "fase", "estado", "resumen"],
        "non_empty_lists": ["indicadores", "indicadores_bloqueados"],
    },
    "dashboard/data/semaforo-decision.json": {
        "required": ["proyecto", "fase", "estado", "semaforo_general", "dimensiones", "decisiones"],
        "non_empty_lists": ["condiciones_para_avanzar"],
    },
    "dashboard/data/alertas-p0.json": {
        "required": ["proyecto", "fase", "estado"],
        "non_empty_lists": ["alertas"],
    },
    "dashboard/data/datos-faltantes.json": {
        "required": ["proyecto", "fase", "estado"],
        "non_empty_lists": ["grupos"],
    },
    "dashboard/data/subproyectos-criticos.json": {
        "required": ["proyecto", "fase", "estado", "subproyectos"],
    },
    "dashboard/data/logistica-construccion.json": {
        "required": ["proyecto", "fase", "estado", "constructivo", "logistico"],
    },
    "dashboard/data/validacion-comercial.json": {
        "required": ["proyecto", "fase", "estado", "conclusion"],
        "non_empty_lists": ["canales_actuales", "canales_potenciales", "riesgos", "plan_validacion", "criterios_para_avanzar"],
    },
    "dashboard/data/referencias_mercado.json": {
        "required": ["proyecto", "tipo", "uso", "no_es_evidencia_de_ventas_nacho", "periodo", "fuente", "privacidad", "advertencia_publica"],
        "non_empty_lists": ["referencias", "productos"],
    },
    "dashboard/data/legal-contable.json": {
        "required": ["proyecto", "fase", "estado", "advertencia"],
        "non_empty_lists": ["temas_a_revisar", "riesgos", "datos_faltantes", "criterios_para_avanzar"],
    },
    "dashboard/data/capex-preliminar.json": {
        "required": ["proyecto", "fase", "estado", "capex_conocido", "capex_pendiente", "conclusion"],
        "non_empty_lists": ["categorias", "riesgos", "criterios_para_avanzar"],
    },
    "dashboard/data/capex-equipamiento-avicola.json": {
        "required": ["proyecto", "fase", "estado", "objetivo_aves", "descripcion", "resumen"],
        "non_empty_lists": ["items"],
    },
    "dashboard/data/escenario-proporcional-500.json": {
        "required": ["proyecto", "fase", "estado", "objetivo_aves", "base_actual_aves", "factor_escala", "densidad", "alimento", "envases_meta", "viruta", "agua", "opex_minimo_proporcional"],
    },
    "dashboard/data/requerimientos-equipamiento-avicola.json": {
        "required": ["proyecto", "fase", "estado", "objetivo_aves", "advertencia", "resumen"],
        "non_empty_lists": ["requerimientos"],
    },
    "dashboard/data/cotizacion-referencial-equipamiento-avicola.json": {
        "required": ["proyecto", "fase", "estado", "fecha_revision", "advertencia", "fuentes", "cotizaciones", "escenarios"],
    },
    "dashboard/data/capex-total-referencial-500.json": {
        "required": ["proyecto", "fase", "estado", "capex_conocido", "equipamiento_escenarios", "capex_total_referencial", "capital_trabajo_inicial", "texto_obligatorio", "decision"],
    },
    "dashboard/data/opex-proyectado-500.json": {
        "required": ["proyecto", "fase", "estado", "objetivo_aves", "componentes_sin_mano_obra", "subtotal_sin_mano_obra_clp_mes", "mano_obra_economica", "subtotal_con_mano_obra_clp_mes", "imprevistos_operativos", "advertencia"],
    },
    "dashboard/data/ingresos-proyectados-500.json": {
        "required": ["proyecto", "fase", "estado", "precio_promedio_actual_clp_bandeja", "mix_actual", "precios_confirmados_clp", "sensibilidades", "nota"],
    },
    "dashboard/data/flujo-financiero-preliminar-500.json": {
        "required": ["proyecto", "fase", "estado", "base_calculo", "margenes", "payback_simple", "punto_equilibrio", "flujo_12_meses", "van_tir", "advertencia"],
    },
    "dashboard/data/estrategia-compra-pollonas.json": {
        "required": ["proyecto", "fase", "estado", "precio_pollona_clp", "pollonas_faltantes", "estrategias", "comparacion", "recomendacion_preliminar"],
    },
    "dashboard/data/flujo-caja-preliminar.json": {
        "required": ["proyecto", "fase", "estado", "ingresos_actuales", "costos_actuales", "mano_obra_referencial", "margenes_actuales", "escenario_500", "escenario_648", "conclusion"],
        "non_empty_lists": ["datos_faltantes", "riesgos", "criterios_para_avanzar", "indicadores_bloqueados"],
    },
    "dashboard/data/criterios-p1.json": {
        "required": ["proyecto", "fase_actual", "estado_p1_preliminar", "estado_p1_definitivo", "compra_pollonas", "decision_actual", "conclusion"],
        "non_empty_lists": ["criterios_minimos", "bloqueos_p1_definitivo", "bloqueos_compra_pollonas"],
    },
}


def is_non_empty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, (str, list, dict, tuple, set)):
        return len(value) > 0
    return True


def validate_file(rel_path: str, spec: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    path = ROOT / rel_path

    if not path.exists():
        return [f"no existe: {rel_path}"]
    if path.stat().st_size == 0:
        return [f"archivo vacío: {rel_path}"]

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"JSON inválido en {rel_path}: {exc}"]

    if not isinstance(data, dict):
        return [f"raíz no es objeto JSON: {rel_path}"]

    for key in spec.get("required", []):
        if key not in data or not is_non_empty(data.get(key)):
            errors.append(f"{rel_path}: falta campo requerido o está vacío: {key}")

    for alternatives in spec.get("required_any", []):
        if not any(is_non_empty(data.get(key)) for key in alternatives):
            errors.append(f"{rel_path}: falta uno de estos campos: {', '.join(alternatives)}")

    for key in spec.get("non_empty_lists", []):
        value = data.get(key)
        if not isinstance(value, list) or not value:
            errors.append(f"{rel_path}: {key} debe ser lista no vacía")

    return errors


def main() -> int:
    errors: list[str] = []
    for rel_path, spec in SPECS.items():
        errors.extend(validate_file(rel_path, spec))

    if errors:
        print("ERROR JSON dashboard")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"OK JSON dashboard: {len(SPECS)} archivos válidos")
    return 0


if __name__ == "__main__":
    sys.exit(main())

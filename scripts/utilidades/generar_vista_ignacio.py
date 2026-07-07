#!/usr/bin/env python3
"""Genera vista ejecutiva en lenguaje simple para Ignacio Moraga."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


def clp(n: int | float) -> str:
    return "$" + f"{round(n):,}".replace(",", ".")


def write_json(rel: str, data: dict[str, Any]) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(rel: str) -> dict[str, Any]:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

# Valores cerrados P45-P47, expresados para la vista pública de Ignacio.
ACTUAL = {
    "gallinas_actuales": 148,
    "produccion_promedio_huevos_dia": 132,
    "rango_junio_huevos_dia": "120–142",
    "produccion_semanal_huevos": 924,
    "bandejas_producidas_semana": 30.8,
    "venta_actual_bandejas_semana": 28,
    "precio_promedio_bandeja_clp": 6107,
    "precios_categoria_clp": {"segunda": 5000, "primera": 6000, "extra": 7000},
    "ingreso_actual_semana_clp": 171000,
    "ingreso_actual_mes_clp": 741000,
    "postura_promedio_porcentaje": 89.2,
    "mortalidad_acumulada_porcentaje": 1.3,
    "alimento_mensual_kg": 550,
    "alimento_gallina_g_dia": 124,
    "costo_mensual_parcial_actual_clp": 343640,
    "resultado_parcial_actual_clp": 397360,
    "agua_actual_litros_dia": 34,
    "gallinero_actual_m2": 27,
    "terreno_disponible_m2": 133,
}
OBJETIVO = {
    "objetivo_gallinas_totales": 500,
    "pollonas_faltantes": 352,
    "produccion_estimada_huevos_dia": 446,
    "bandejas_estimadas_semana": 104.1,
    "meta_venta_bandejas_semana": 100,
    "diferencia_tecnica_bandejas_semana": 4.1,
    "agua_estimada_litros_dia": "115 a 154,3",
    "galpon_considerado_m2": 72,
    "densidad_gallinas_m2": 7,
    "nota_meta": "La meta de 100 bandejas por semana fue usada como base de cálculo porque Ignacio indicó que sería una venta segura o casi segura y al contado.",
}
INVERSION = {
    "galpon_mas_pollonas_faltantes_clp": 9771765,
    "equipamiento_estimado_base_clp": 3572000,
    "inversion_total_estimada_base_clp": 13343765,
    "caja_minima_primer_mes_clp": 1686750,
    "total_base_con_un_mes_operacion_clp": 15030515,
    "maximo_informado_ignacio_clp": 10000000,
    "diferencia_faltante_clp": 5030515,
}
VENTAS = {
    "ingreso_mensual_estimado_clp": 2646367,
    "costo_mensual_sin_valorar_trabajo_clp": 1086750,
    "trabajo_ignacio_valorizado_clp": 600000,
    "costo_mensual_total_con_trabajo_clp": 1686750,
    "resultado_mensual_preliminar_con_trabajo_clp": 959617,
    "venta_minima_no_perder_bandejas_semana": 63.7,
    "tiempo_recuperar_inversion_base_meses": 13.91,
}
ALTERNATIVAS = [
    {
        "id": "mas_100",
        "titulo": "+100 pollonas",
        "texto": "Reduce riesgo y presión de caja.",
        "inversion_inicial_con_caja_clp": 3053801,
        "resultado_mensual_estimado_clp": 473570,
        "nivel_cautela": "bajo",
        "condicion": "Usar solo si la infraestructura actual alcanza.",
        "titulo_visible": "+100 pollonas: opción más conservadora",
    },
    {
        "id": "mas_150",
        "titulo": "+150 pollonas",
        "texto": "Permite crecer, medir y mantener caja disponible.",
        "inversion_inicial_con_caja_clp": 4369862,
        "resultado_mensual_estimado_clp": 529532,
        "nivel_cautela": "medio",
        "condicion": "Validar infraestructura, comederos, bebederos y compradores.",
        "titulo_visible": "+150 pollonas: alternativa recomendada",
    },
    {
        "id": "mas_200",
        "titulo": "+200 pollonas",
        "texto": "Acelera el crecimiento, pero aumenta la presión financiera y operativa.",
        "inversion_inicial_con_caja_clp": 5685923,
        "resultado_mensual_estimado_clp": 585493,
        "nivel_cautela": "alto",
        "condicion": "Avanzar solo con compradores y caja más confirmados.",
        "titulo_visible": "+200 pollonas: crecimiento más rápido",
    },
    {
        "id": "mas_352",
        "titulo": "+352 pollonas",
        "texto": "No se recomienda todavía sin financiamiento cerrado.",
        "inversion_inicial_con_caja_clp": 15030515,
        "resultado_mensual_estimado_clp": 959617,
        "nivel_cautela": "alto",
        "condicion": "Ejecutar solo con financiamiento cerrado, equipamiento listo y venta confirmada.",
        "titulo_visible": "+352 pollonas: llegar directo a 500 gallinas",
    },
]

vista = {
    "proyecto": "Evaluación del proyecto avícola de Ignacio Moraga",
    "subtitulo": "Análisis preliminar para decidir si conviene crecer desde 148 gallinas hacia 500 gallinas.",
    "estado_visible": "ANALIZAR CON CAUTELA",
    "estado_interno": "amarillo",
    "mensaje_estado": "El proyecto muestra potencial, pero todavía no está listo para una inversión grande. La recomendación actual es avanzar por etapas, validar ventas y costos reales, y no comprar todas las pollonas de una vez sin financiamiento, equipamiento y compradores confirmados.",
    "recomendacion_principal": "La recomendación actual no es llegar inmediatamente a 500 gallinas. La alternativa más prudente es comenzar con +150 pollonas, medir ventas, consumo, costos y trabajo real durante 30 a 60 días, y luego decidir si conviene seguir creciendo.",
    "atencion_ignacio": "Atención Ignacio: no se recomienda comprar las 352 pollonas de una vez todavía. Para llegar directo a 500 gallinas se necesita más dinero que los $10.000.000 informados, además de equipamiento, caja para operar y compradores confirmados.",
    "resumen_decision": [
        {"titulo": "Estado", "valor": "Analizar con cautela", "detalle": "Puede ser interesante, pero faltan confirmaciones."},
        {"titulo": "Recomendación", "valor": "Avanzar por etapas", "detalle": "Medir ventas, costos y trabajo real antes de crecer completo."},
        {"titulo": "Alternativa recomendada", "valor": "+150 pollonas", "detalle": "Equilibra crecimiento y riesgo."},
        {"titulo": "Opción conservadora", "valor": "+100 pollonas", "detalle": "Menor presión de caja."},
        {"titulo": "No recomendado ahora", "valor": "+352 pollonas de una vez", "detalle": "Solo con financiamiento cerrado."},
        {"titulo": "Condición para llegar a 500", "valor": "Cerrar financiamiento y ventas", "detalle": "Equipamiento, compradores y validación formal listos."},
    ],
    "situacion_actual": ACTUAL,
    "objetivo_evaluado": OBJETIVO,
    "inversion_necesaria": INVERSION,
    "ventas_resultado": VENTAS,
    "alternativas_crecimiento": ALTERNATIVAS,
    "conclusion_alternativas": "La alternativa recomendada es +150 pollonas porque permite crecer, medir resultados reales y mantener caja disponible. +100 es más conservadora. +352 no debe ejecutarse todavía sin financiamiento cerrado.",
    "estado_visible_texto": "Estado: analizar con cautela",
    "proximos_pasos": [
        "Revisar estos números con Ignacio.",
        "Confirmar dinero disponible real.",
        "Pedir cotizaciones finales de equipamiento.",
        "Confirmar compradores por canal.",
        "Validar situación legal, sanitaria y tributaria.",
        "Revisar infraestructura actual para +100 o +150 pollonas.",
        "Definir fecha de primera compra.",
        "Partir por +150 pollonas solo si lo anterior está resuelto.",
    ],
}

supuestos = {
    "proyecto": vista["proyecto"],
    "uso": "Supuestos simples usados para explicar el análisis a Ignacio.",
    "supuestos": [
        {"titulo": "Precios de venta usados", "estado": "Confirmado por Ignacio", "detalle": "Segunda $5.000, primera $6.000 y extra $7.000 por bandeja."},
        {"titulo": "Venta usada para el cálculo", "estado": "Confirmado por Ignacio", "detalle": "100 bandejas por semana, con pago al contado."},
        {"titulo": "Alimento", "estado": "Estimado para el análisis / validado como razonable por Ignacio", "detalle": "75 sacos por mes para 500 gallinas, a $12.950 por saco."},
        {"titulo": "Trabajo de Ignacio", "estado": "Confirmado por Ignacio / estimado económico", "detalle": "Ignacio trabajaría solo. Se valoró su trabajo en $20.000 diarios, equivalente a $600.000 mensuales."},
        {"titulo": "Caja mínima para partir", "estado": "Estimado para el análisis", "detalle": "Se considera al menos 1 mes de costos como caja mínima para partir."},
        {"titulo": "Equipamiento", "estado": "Pendiente de validar", "detalle": "Los precios son referenciales. Faltan cotizaciones finales."},
        {"titulo": "Situación legal, sanitaria y tributaria", "estado": "Pendiente de validar", "detalle": "Ignacio informa que tiene inicio de actividades. Aun así, falta validar permisos, venta con boleta/factura y exigencias sanitarias antes de invertir fuerte."},
    ],
}

alertas = {
    "proyecto": vista["proyecto"],
    "uso": "Alertas importantes para Ignacio antes de invertir.",
    "grupos": [
        {
            "titulo": "Dinero",
            "etiqueta": "ALTA ATENCIÓN",
            "items": [
                "El proyecto completo base supera los $10.000.000 disponibles.",
                "Falta financiar inversión, equipamiento y caja inicial.",
                "No comprar todas las pollonas si no está cerrado el dinero total.",
            ],
        },
        {
            "titulo": "Ventas",
            "etiqueta": "VALIDAR ANTES DE INVERTIR",
            "items": [
                "La meta de 100 bandejas/semana debe confirmarse por canal.",
                "Aunque se informó venta segura, conviene respaldarla con compradores concretos.",
                "La venta mínima para no perder considerando trabajo es 63,7 bandejas/semana.",
            ],
        },
        {
            "titulo": "Operación",
            "etiqueta": "VALIDAR ANTES DE INVERTIR",
            "items": [
                "Confirmar que la infraestructura actual soporta +100 o +150 pollonas.",
                "Confirmar comederos, bebederos, nidos, agua, energía y bodega.",
                "Medir 30 a 60 días antes de una segunda expansión.",
            ],
        },
        {
            "titulo": "Legal / sanitario / tributario",
            "etiqueta": "VALIDAR ANTES DE INVERTIR",
            "items": [
                "Aunque Ignacio tenga inicio de actividades, falta validar si corresponde patente, permiso, resolución, factura, boleta u otra exigencia para vender formalmente.",
            ],
        },
    ],
}

pasos = {
    "proyecto": vista["proyecto"],
    "uso": "Pasos simples para Ignacio antes de invertir.",
    "pasos": vista["proximos_pasos"],
}

write_json("dashboard/data/vista-ignacio-resumen-ejecutivo.json", vista)
write_json("dashboard/data/supuestos-para-ignacio.json", supuestos)
write_json("dashboard/data/alertas-para-ignacio.json", alertas)
write_json("dashboard/data/proximos-pasos-ignacio.json", pasos)

# Actualizaciones de textos ejecutivos existentes, sin tocar cálculos.
estado = read_json("dashboard/data/estado-proyecto.json")
estado["fase"] = "Evaluación ejecutiva para Ignacio"
estado["decision_actual"] = "Analizar con cautela: avanzar por etapas, con +150 pollonas como alternativa recomendada y +352 solo con financiamiento cerrado."
write_json("dashboard/data/estado-proyecto.json", estado)

resumen = read_json("dashboard/data/resumen-ejecutivo-p0.json")
resumen["fase"] = "Evaluación ejecutiva para Ignacio"
resumen["estado_general"] = "analizar con cautela"
resumen["conclusion"] = "El proyecto puede ser interesante, pero todavía faltan confirmaciones antes de invertir fuerte. La lectura recomendada para Ignacio es avanzar por etapas: +150 pollonas como alternativa base prudente, +100 como opción conservadora y +352 solo con financiamiento cerrado."
write_json("dashboard/data/resumen-ejecutivo-p0.json", resumen)

semaforo = read_json("dashboard/data/semaforo-decision.json")
semaforo["fase"] = "Evaluación ejecutiva para Ignacio"
semaforo["estado"] = "analizar con cautela"
semaforo["semaforo_general"] = "amarillo"
semaforo["conclusion"] = "Analizar con cautela: no comprar aves todavía, no construir todavía y no hacer inversión grande hasta cerrar financiamiento, equipamiento, compradores y validación formal."
write_json("dashboard/data/semaforo-decision.json", semaforo)

faltantes = read_json("dashboard/data/datos-faltantes.json")
faltantes["fase"] = "Evaluación ejecutiva para Ignacio"
faltantes["nota"] = "Faltan cotizaciones finales, financiamiento, caja inicial para operar, compradores por canal, validación legal/sanitaria/tributaria e infraestructura actual validada antes de invertir fuerte."
write_json("dashboard/data/datos-faltantes.json", faltantes)

report = f"""# Ajuste de lenguaje para Ignacio y narrativa ejecutiva

## Cambios de lenguaje realizados

- La vista principal dejó de hablar en lenguaje interno y ahora se presenta como **Evaluación del proyecto avícola de Ignacio Moraga**.
- El estado visible se cambió a **Analizar con cautela**.
- La recomendación queda escrita en lenguaje directo: no comprar las 352 pollonas de una vez todavía; partir preferentemente con +150 pollonas o +100 si se quiere reducir más el riesgo.

## Términos técnicos reemplazados

- CAPEX → Inversión inicial / inversión estimada.
- OPEX → Costo mensual de operación.
- Payback → Tiempo estimado para recuperar la inversión.
- Punto de equilibrio → Venta mínima necesaria para no perder.
- Capital de trabajo → Caja mínima para partir / dinero mínimo para operar el primer mes.
- Margen → Resultado mensual preliminar, aclarando que no es utilidad final.
- Flujo → Caja mensual estimada / resultado mensual estimado.
- Semáforo → Nivel de cautela.
- Estado amarillo → Analizar con cautela.
- Bloqueado / no habilitado → No ejecutar todavía / no aprobado todavía.
- Dashboard → Informe visual / eliminado de la lectura principal.
- Hito → Etapa del análisis / eliminado de la lectura principal.
- ROI, VAN y TIR → No se muestran en portada; quedan como indicadores financieros avanzados no calculados por falta de datos finales.

## Nueva estructura narrativa

1. Resumen de decisión.
2. Situación actual del gallinero.
3. Objetivo evaluado: crecer hacia 500 gallinas.
4. Supuestos usados para calcular.
5. Inversión necesaria.
6. Costos mensuales y ventas esperadas.
7. Alternativas de crecimiento.
8. Alertas importantes.
9. Qué hacer antes de invertir.
10. Detalle técnico para revisión.

## Supuestos destacados

- Venta usada para el cálculo: 100 bandejas/semana, pago al contado.
- Precios usados: segunda {clp(5000)}, primera {clp(6000)}, extra {clp(7000)}.
- Alimento: 75 sacos/mes a {clp(12950)} por saco.
- Trabajo de Ignacio valorizado: {clp(600000)} mensuales.
- Caja mínima para partir: 1 mes de costos.
- Equipamiento: referencial, falta cotización final.
- Permisos/formalización: pendiente de validación aunque Ignacio informe inicio de actividades.

## Alertas importantes para Ignacio

- Con {clp(10000000)} no alcanza para partir directo a 500 gallinas en el caso base.
- Total base con un mes de operación: {clp(15030515)}.
- Diferencia faltante: {clp(5030515)}.
- La venta mínima para no perder considerando trabajo es 63,7 bandejas/semana.
- No comprar 352 pollonas de una vez sin financiamiento cerrado, equipamiento listo y venta confirmada.

## Confirmación de coherencia numérica

- Galpón + pollonas: {clp(9771765)}.
- Equipamiento base: {clp(3572000)}.
- Inversión total base: {clp(13343765)}.
- Caja mínima primer mes: {clp(1686750)}.
- Total base con 1 mes de operación: {clp(15030515)}.
- Diferencia contra {clp(10000000)}: {clp(5030515)}.
- Ingreso mensual meta: {clp(2646367)}.
- Costo mensual con trabajo: {clp(1686750)}.
- Resultado mensual preliminar: {clp(959617)}.
- Venta mínima para no perder con trabajo: 63,7 bandejas/semana.
- Tiempo estimado para recuperar inversión base con trabajo: 13,91 meses.
- +100: {clp(3053801)} / {clp(473570)}.
- +150: {clp(4369862)} / {clp(529532)}.
- +200: {clp(5685923)} / {clp(585493)}.
- +352: {clp(15030515)} / {clp(959617)}.

## Qué quedó en detalle técnico

- Rangos de inversión más amplios y referencias de respaldo.
- Indicadores financieros avanzados no calculados todavía porque faltan datos finales.
- Comparaciones históricas de escala y trazabilidad de archivos internos.
- Alertas históricas largas que no deben dominar la lectura principal de Ignacio.

## Base para informe final posterior

- Se creó `reports/base_informe_final_ignacio_decision_avicola.md`.
- Consolida datos cerrados, supuestos confirmados, supuestos estimados, pendientes, números principales, alternativas, recomendación vigente y alertas críticas.
- No se redactó todavía el informe final completo.

## Pendientes que impiden pasar a verde

- Cotizaciones finales.
- Financiamiento completo.
- Caja inicial cubierta.
- Compradores confirmados por canal.
- Validación legal, sanitaria y tributaria.
- Infraestructura actual validada para +100 o +150 pollonas.
- Logística y calendario real definidos.
"""
(ROOT / "reports/p47_r2_lenguaje_ignacio_y_narrativa_ejecutiva.md").write_text(report, encoding="utf-8")

print("Vista Ignacio generada")

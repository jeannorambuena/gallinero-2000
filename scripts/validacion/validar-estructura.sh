#!/usr/bin/env bash
set -Eeuo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${RAIZ}"

requeridos=(
  README.md
  ROADMAP.md
  CHANGELOG.md
  config/proyecto.yml
  docs/01-p0-diagnostico/README.md
  datos/reales/produccion/produccion-diaria.csv
  datos/reales/gastos/gastos-mensuales.csv
  datos/reales/ventas/ventas.csv
  datos/referencias/fuentes/catalogo-fuentes.csv
  datos/precios/materiales/precios-materiales.csv
  freecad/parametros/parametros.yml
  openclaw/reglas/REGLAS.md
  openclaw/prompts/prompt-maestro.md
  templates/formularios/levantamiento-p0.md
)

faltantes=0
for elemento in "${requeridos[@]}"; do
  if [[ ! -e "${elemento}" ]]; then
    echo "FALTA: ${elemento}"
    faltantes=$((faltantes + 1))
  fi
done

if (( faltantes > 0 )); then
  echo "Validación fallida: ${faltantes} faltantes."
  exit 1
fi

echo "Validación correcta: estructura base completa."

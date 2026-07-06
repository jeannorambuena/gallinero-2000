#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-https://jeannorambuena.github.io/gallinero-2000}"
CACHE_TAG="${2:-$(git rev-parse --short HEAD)}"

PUBLIC_URL="$BASE_URL/public/?v=$CACHE_TAG-$(date +%s)"
APP_URL="$BASE_URL/public/app.js?v=$CACHE_TAG-$(date +%s)"
DATA_URL="$BASE_URL/data/finanzas-preliminares.json?v=$CACHE_TAG-$(date +%s)"
SEMAFORO_URL="$BASE_URL/data/semaforo-decision.json?v=$CACHE_TAG-$(date +%s)"

echo "=== GIT LOCAL ==="
git status -sb
git log --oneline --decorate -5

echo
echo "=== GITHUB ACTIONS PAGES ==="
if command -v gh >/dev/null 2>&1; then
  gh run list --workflow pages.yml --branch dashboard/v2-ejecutivo-500 -L 3 || true
  echo
  LAST_RUN="$(gh run list --workflow pages.yml --branch dashboard/v2-ejecutivo-500 -L 1 --json databaseId --jq '.[0].databaseId' 2>/dev/null || true)"
  if [ -n "${LAST_RUN:-}" ]; then
    gh run view "$LAST_RUN" --json status,conclusion,headSha,createdAt,updatedAt,url || true
  fi
else
  echo "gh no disponible"
fi

echo
echo "=== HTTP STATUS ==="
for url in "$PUBLIC_URL" "$APP_URL" "$DATA_URL" "$SEMAFORO_URL"; do
  code="$(curl -sL -o /dev/null -w "%{http_code}" "$url")"
  echo "$code $url"
done

echo
echo "=== MARCAS EN HTML PUBLICADO ==="
curl -sL "$PUBLIC_URL" | grep -Ei \
  "id=\"finanzas\"|indicadores-financieros|Pendientes visibles|Decisión final|p1-preliminar|compra-aves|inversion-mayor|dashboard" \
  | head -80 || true

echo
echo "=== MARCAS EN APP.JS PUBLICADO ==="
curl -sL "$APP_URL" | grep -Ei \
  "renderFinancialIndicators|catalogo_indicadores_financieros|indicator-help|financial-card|decisionFinal|no disponible|bloqueada|no autorizada|DATA|/data|../data" \
  | head -120 || true

echo
echo "=== MARCAS EN DATA FINANZAS PUBLICADO ==="
curl -sL "$DATA_URL" | grep -Ei \
  "catalogo_indicadores_financieros|capex_galpon_500|EBITDA|VAN|TIR|ROI|Payback|Pendiente|COT-GN-0035|5547765|9771765|4224000|171000|741000|6107" \
  | head -120 || true

echo
echo "=== MARCAS EN SEMAFORO PUBLICADO ==="
curl -sL "$SEMAFORO_URL" | grep -Ei \
  "p1_preliminar_habilitado|puede_comprar_aves|puede_construir|inversion_mayor_autorizada|decision_final_disponible|false|amarillo" \
  | head -120 || true

echo
echo "=== BUSCAR RUTAS ABSOLUTAS SOSPECHOSAS EN APP LOCAL ==="
grep -RniE "['\"]/[a-zA-Z0-9_-]+/|['\"]/data/" dashboard/public/app.js || true

echo
echo "=== BUSCAR RESIDUOS ANTIGUOS ==="
grep -RniE "100 m²|100 m2|5 aves|7705200|15410400|30820800|7\.705\.200|15\.410\.400|30\.820\.800|extrapolado 100|superficie_util_m2.*100" dashboard docs README.md ROADMAP.md 2>/dev/null || true

echo
echo "=== MARCAS P42 ESPERADAS EN DATA PUBLICADO ==="
curl -sL "$DATA_URL" | grep -Ei "171000|741000|6107|352|12000|4224000|1232000|9771765|343640" | head -120 || true

echo
echo "=== RESULTADO ESPERADO ==="
echo "Debe aparecer:"
echo "- HTML: id=\"finanzas\" e indicadores-financieros"
echo "- APP: renderFinancialIndicators e indicator-help"
echo "- DATA: catalogo_indicadores_financieros, VAN, TIR, EBITDA"
echo "- HTTP: todos 200"
echo "- Rutas absolutas sospechosas: idealmente ninguna ruta /data desde app.js"

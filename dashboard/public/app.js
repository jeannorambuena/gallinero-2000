const DATA_BASE = new URL('../data/', window.location.href);

const DATA_FILES = {
  vista: new URL('vista-ignacio-resumen-ejecutivo.json', DATA_BASE).href,
  supuestos: new URL('supuestos-para-ignacio.json', DATA_BASE).href,
  alertas: new URL('alertas-para-ignacio.json', DATA_BASE).href,
  pasos: new URL('proximos-pasos-ignacio.json', DATA_BASE).href,
  detalleFinanciero: new URL('flujo-financiero-preliminar-500.json', DATA_BASE).href,
  detalleInversion: new URL('capex-total-referencial-500.json', DATA_BASE).href
};

function $(id) {
  return document.getElementById(id);
}

function setText(id, value) {
  const node = $(id);
  if (node) node.textContent = value ?? '';
}

function formatCurrency(value) {
  if (value === undefined || value === null || value === '') return 'pendiente';
  if (Number.isNaN(Number(value))) return String(value);
  return `$${Number(value).toLocaleString('es-CL')}`;
}

function formatNumber(value) {
  if (value === undefined || value === null || value === '') return 'pendiente';
  if (Number.isNaN(Number(value))) return String(value);
  return Number(value).toLocaleString('es-CL');
}

function metricCard({ label, value, detail = '', tone = '' }) {
  const article = document.createElement('article');
  article.className = `metric-card ${tone}`.trim();
  article.innerHTML = `
    <span>${label}</span>
    <strong>${value}</strong>
    ${detail ? `<small>${detail}</small>` : ''}
  `;
  return article;
}

function renderMetrics(containerId, metrics) {
  const container = $(containerId);
  if (!container) return;
  container.innerHTML = '';
  metrics.forEach((metric) => container.appendChild(metricCard(metric)));
}

function renderRows(containerId, rows) {
  const container = $(containerId);
  if (!container) return;
  container.innerHTML = '';
  rows.forEach((row) => {
    const card = document.createElement('article');
    card.className = `financial-card ${row.tone ?? ''}`.trim();
    card.innerHTML = `
      <div class="financial-card-head">
        <span>${row.kicker ?? ''}</span>
        <strong>${row.title}</strong>
      </div>
      <div class="financial-value">${row.value}</div>
      ${row.detail ? `<p>${row.detail}</p>` : ''}
      ${row.small ? `<small>${row.small}</small>` : ''}
    `;
    container.appendChild(card);
  });
}

function renderResumen(vista) {
  setText('mensaje-estado', vista?.mensaje_estado);
  setText('recomendacion-principal', vista?.recomendacion_principal);
  setText('atencion-ignacio', vista?.atencion_ignacio);
  renderMetrics('resumen-decision', (vista?.resumen_decision ?? []).map((item) => ({
    label: item.titulo,
    value: item.valor,
    detail: item.detalle,
    tone: item.titulo === 'No recomendado ahora' ? 'risk' : item.titulo === 'Alternativa recomendada' ? 'accent' : 'pending'
  })));
}

function renderSituacionActual(actual = {}) {
  renderMetrics('situacion-actual', [
    { label: 'Gallinas actuales', value: formatNumber(actual.gallinas_actuales), detail: 'aves' },
    { label: 'Producción promedio', value: `${formatNumber(actual.produccion_promedio_huevos_dia)} huevos/día`, detail: `rango junio: ${actual.rango_junio_huevos_dia} huevos/día` },
    { label: 'Venta actual', value: `${formatNumber(actual.venta_actual_bandejas_semana)} bandejas/semana`, detail: `${formatNumber(actual.bandejas_producidas_semana)} bandejas producidas aprox.` },
    { label: 'Ingreso actual', value: `${formatCurrency(actual.ingreso_actual_semana_clp)}/semana`, detail: `${formatCurrency(actual.ingreso_actual_mes_clp)} mensual aprox.` },
    { label: 'Costo mensual parcial actual', value: formatCurrency(actual.costo_mensual_parcial_actual_clp), detail: 'no incluye todos los costos de crecer' },
    { label: 'Resultado parcial actual', value: formatCurrency(actual.resultado_parcial_actual_clp), detail: 'antes de completar costos de escala', tone: 'pending' },
    { label: 'Gallinero actual', value: `${formatNumber(actual.gallinero_actual_m2)} m²`, detail: `terreno disponible: ${formatNumber(actual.terreno_disponible_m2)} m²` },
    { label: 'Agua actual', value: `${formatNumber(actual.agua_actual_litros_dia)} L/día`, detail: 'validar para crecer' }
  ]);
}

function renderObjetivo(objetivo = {}) {
  renderMetrics('objetivo-evaluado', [
    { label: 'Objetivo', value: `${formatNumber(objetivo.objetivo_gallinas_totales)} gallinas`, detail: 'caso evaluado' },
    { label: 'Pollonas faltantes', value: formatNumber(objetivo.pollonas_faltantes), detail: 'para llegar a 500 gallinas' },
    { label: 'Producción estimada', value: `${formatNumber(objetivo.produccion_estimada_huevos_dia)} huevos/día`, detail: `${formatNumber(objetivo.bandejas_estimadas_semana)} bandejas/semana` },
    { label: 'Meta de venta usada', value: `${formatNumber(objetivo.meta_venta_bandejas_semana)} bandejas/semana`, detail: 'base del cálculo', tone: 'accent' },
    { label: 'Agua estimada', value: `${objetivo.agua_estimada_litros_dia} L/día`, detail: 'requiere validación' },
    { label: 'Galpón considerado', value: `${formatNumber(objetivo.galpon_considerado_m2)} m²`, detail: `${formatNumber(objetivo.densidad_gallinas_m2)} gallinas/m² aprox.` }
  ]);
  setText('nota-meta', objetivo.nota_meta);
}

function renderSupuestos(supuestos = {}) {
  const container = $('supuestos-calculo');
  if (!container) return;
  container.innerHTML = '';
  (supuestos.supuestos ?? []).forEach((item) => {
    const card = document.createElement('article');
    const statusClass = item.estado === 'Confirmado por Ignacio' ? 'confirmed' : item.estado === 'Pendiente de validar' ? 'validate' : 'estimated';
    card.className = `assumption-card ${statusClass}`;
    card.innerHTML = `
      <span>${item.estado}</span>
      <strong>${item.titulo}</strong>
      <p>${item.detalle}</p>
    `;
    container.appendChild(card);
  });
}

function renderInversion(inversion = {}) {
  renderMetrics('inversion-necesaria', [
    { label: 'Galpón + pollonas faltantes', value: formatCurrency(inversion.galpon_mas_pollonas_faltantes_clp), detail: 'subtotal ya conocido' },
    { label: 'Equipamiento estimado', value: formatCurrency(inversion.equipamiento_estimado_base_clp), detail: 'precio referencial, falta cotización final' },
    { label: 'Inversión total estimada base', value: formatCurrency(inversion.inversion_total_estimada_base_clp), detail: 'sin caja inicial' },
    { label: 'Caja mínima para operar el primer mes', value: formatCurrency(inversion.caja_minima_primer_mes_clp), detail: 'dinero para partir' },
    { label: 'Total necesario base con 1 mes de operación', value: formatCurrency(inversion.total_base_con_un_mes_operacion_clp), detail: 'inversión + caja inicial', tone: 'risk' },
    { label: 'Máximo informado por Ignacio', value: formatCurrency(inversion.maximo_informado_ignacio_clp), detail: 'referencia de caja disponible' },
    { label: 'Diferencia faltante', value: formatCurrency(inversion.diferencia_faltante_clp), detail: 'para partir directo a 500', tone: 'risk' }
  ]);
  setText('alerta-inversion', `Atención: con ${formatCurrency(inversion.maximo_informado_ignacio_clp)} no alcanza para partir directo a 500 gallinas en el caso base. Falta financiar aproximadamente ${formatCurrency(inversion.diferencia_faltante_clp)} si se considera inversión base más un mes de operación.`);
}

function renderVentas(ventas = {}) {
  renderMetrics('ventas-resultado', [
    { label: 'Ingreso mensual estimado', value: formatCurrency(ventas.ingreso_mensual_estimado_clp), detail: '100 bandejas/semana' },
    { label: 'Costo mensual sin valorar trabajo de Ignacio', value: formatCurrency(ventas.costo_mensual_sin_valorar_trabajo_clp), detail: 'alimento, envases, viruta, reparto y otros' },
    { label: 'Trabajo de Ignacio valorizado', value: formatCurrency(ventas.trabajo_ignacio_valorizado_clp), detail: '$20.000 diarios' },
    { label: 'Costo mensual total considerando trabajo', value: formatCurrency(ventas.costo_mensual_total_con_trabajo_clp), detail: 'costo mensual de operación prudente' },
    { label: 'Resultado mensual preliminar considerando trabajo', value: formatCurrency(ventas.resultado_mensual_preliminar_con_trabajo_clp), detail: 'no es utilidad final', tone: 'accent' },
    { label: 'Venta mínima necesaria para no perder', value: `${formatNumber(ventas.venta_minima_no_perder_bandejas_semana)} bandejas/semana`, detail: 'considerando trabajo valorizado' },
    { label: 'Tiempo estimado para recuperar la inversión base', value: `${formatNumber(ventas.tiempo_recuperar_inversion_base_meses)} meses`, detail: 'considerando trabajo valorizado' }
  ]);
}

function renderAlternativas(vista = {}) {
  const toneByLevel = { bajo: 'accent', medio: 'pending', alto: 'risk' };
  renderRows('alternativas-crecimiento', (vista.alternativas_crecimiento ?? []).map((alt) => ({
    kicker: `Nivel de cautela: ${alt.nivel_cautela}`,
    title: alt.titulo_visible ?? alt.titulo,
    value: formatCurrency(alt.inversion_inicial_con_caja_clp),
    detail: `${alt.texto} Resultado mensual estimado: ${formatCurrency(alt.resultado_mensual_estimado_clp)}.`,
    small: `Condición: ${alt.condicion}`,
    tone: toneByLevel[alt.nivel_cautela] ?? 'pending'
  })));
  setText('conclusion-alternativas', vista.conclusion_alternativas);
}

function renderAlertas(alertas = {}) {
  const container = $('alertas-ignacio');
  if (!container) return;
  container.innerHTML = '';
  (alertas.grupos ?? []).forEach((grupo) => {
    const card = document.createElement('article');
    card.className = 'critical-card';
    card.innerHTML = `
      <div class="critical-head">
        <span>${grupo.etiqueta}</span>
        <strong>${grupo.titulo}</strong>
      </div>
      <ul>${(grupo.items ?? []).map((item) => `<li>${item}</li>`).join('')}</ul>
    `;
    container.appendChild(card);
  });
}

function renderPasos(pasos = {}, vista = {}) {
  const container = $('proximos-pasos');
  if (!container) return;
  container.innerHTML = '';
  const items = pasos.pasos ?? vista.proximos_pasos ?? [];
  items.forEach((item, index) => {
    const row = document.createElement('div');
    row.className = 'step-item';
    row.innerHTML = `<span>${index + 1}</span><strong>${item}</strong>`;
    container.appendChild(row);
  });
}

function renderDetalle({ detalleFinanciero, detalleInversion }) {
  renderRows('detalle-tecnico', [
    {
      kicker: 'Inversión estimada',
      title: 'Rangos de inversión para 500 gallinas',
      value: `${formatCurrency(detalleInversion?.capex_total_referencial?.bajo?.capex_total_referencial_clp)} a ${formatCurrency(detalleInversion?.capex_total_referencial?.alto?.capex_total_referencial_clp)}`,
      detail: 'Rango bajo a alto. La lectura principal usa el caso base.',
      small: 'Detalle para revisión, no autorización de inversión.'
    },
    {
      kicker: 'Caja mensual estimada',
      title: 'Resultado mensual antes de otros gastos',
      value: formatCurrency(detalleFinanciero?.margenes?.con_mano_obra_clp_mes),
      detail: 'Resultado preliminar con trabajo de Ignacio valorizado.',
      small: 'Faltan costos formales y cotizaciones finales.'
    },
    {
      kicker: 'Indicadores avanzados',
      title: 'No calculados todavía',
      value: 'pendiente',
      detail: 'No se calculan indicadores financieros avanzados porque todavía faltan datos finales.',
      small: 'Se requiere tasa, vida útil, calendario definitivo y validación comercial/legal.'
    }
  ]);
}

async function loadJson(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`No se pudo cargar ${path}`);
  return response.json();
}

async function loadData() {
  const entries = await Promise.all(Object.entries(DATA_FILES).map(async ([key, path]) => {
    try {
      return [key, await loadJson(path)];
    } catch (error) {
      console.warn(error);
      return [key, null];
    }
  }));
  return Object.fromEntries(entries);
}

async function init() {
  const data = await loadData();
  const vista = data.vista ?? {};
  renderResumen(vista);
  renderSituacionActual(vista.situacion_actual);
  renderObjetivo(vista.objetivo_evaluado);
  renderSupuestos(data.supuestos);
  renderInversion(vista.inversion_necesaria);
  renderVentas(vista.ventas_resultado);
  renderAlternativas(vista);
  renderAlertas(data.alertas);
  renderPasos(data.pasos, vista);
  renderDetalle(data);
}

document.addEventListener('DOMContentLoaded', init);

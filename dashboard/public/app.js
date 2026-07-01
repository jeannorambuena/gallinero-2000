const DATA_BASE = new URL('../data/', window.location.href);

const DATA_FILES = {
  resumen: new URL('resumen-ejecutivo-p0.json', DATA_BASE).href,
  estado: new URL('estado-proyecto.json', DATA_BASE).href,
  productivos: new URL('indicadores-productivos.json', DATA_BASE).href,
  comerciales: new URL('indicadores-comerciales.json', DATA_BASE).href,
  validacionComercial: new URL('validacion-comercial.json', DATA_BASE).href,
  logisticaConstruccion: new URL('logistica-construccion.json', DATA_BASE).href,
  referenciasMercado: new URL('referencias_mercado.json', DATA_BASE).href,
  finanzas: new URL('finanzas-preliminares.json', DATA_BASE).href,
  flujoCaja: new URL('flujo-caja-preliminar.json', DATA_BASE).href,
  semaforo: new URL('semaforo-decision.json', DATA_BASE).href,
  criteriosP1: new URL('criterios-p1.json', DATA_BASE).href,
  galpones: new URL('estimacion-galpones.json', DATA_BASE).href,
  alertas: new URL('alertas-p0.json', DATA_BASE).href
};

const FALLBACKS = {
  operacion: {
    gallinas: 148,
    huevosDia: 132,
    bandejasSemana: 28,
    postura: 89.2,
    mortalidad: 1.3,
    aguaDia: 34,
    edad: 37,
    raza: 'Hy-Line W80'
  },
  escenario500: {
    aves: 500,
    huevosDia: 446,
    bandejasSemana: 104.1,
    ventaActual: 28,
    brecha: 76.1,
    agua: '115.7–154.3 L/día',
    superficie: 72,
    densidadGalpon: 7,
    costoM2Galpon: 77052,
    costoGalponEscenario: 5547765,
    referenciaV8: {
      superficie_m2: 72,
      total_general_clp: 5547765,
      costo_m2_aprox_clp: 77052
    }
  }
};

const RISK_COPY = {
  comercial: 'Nacho debe validar clientes, cantidades, precios, frecuencia, pago y boleta/factura.',
  financiera: 'CAPEX referencial del galpón disponible; CAPEX total y flujo siguen incompletos.',
  logistica: 'Acceso rural e invierno afectan materiales y operación.',
  sanitaria: 'Humedad, calor y manejo de agua aún requieren mejoras.',
  agua: 'Falta dimensionamiento definitivo de caudal, presión y respaldo.',
  energia: 'El sistema solar aún requiere cálculo y cotización.',
  legal: 'Formalización, permisos y trazabilidad siguen pendientes.',
  contable: 'Registro, impuestos y operación formal siguen pendientes.'
};

const TRAFFIC_RULES = [
  {
    color: 'rojo',
    title: 'ROJO',
    decision: 'No invertir',
    detail: 'Corregir datos críticos antes de avanzar.',
    active: false
  },
  {
    color: 'amarillo',
    title: 'AMARILLO',
    decision: 'Solo desbloqueo menor/controlado',
    detail: 'Cotizar, medir, validar mercado y levantar evidencia.',
    active: true
  },
  {
    color: 'verde',
    title: 'VERDE',
    decision: 'Inversión habilitable con evidencias completas',
    detail: 'Solo con mercado, CAPEX, flujo y riesgos completos.',
    active: false
  }
];

const BLOCKERS = [
  'Amarillo no significa no viable; significa información crítica pendiente',
  'Mercado no validado para 104.1 bandejas/semana',
  'Faltan cerca de 76.1 bandejas/semana adicionales validadas',
  'CAPEX referencial del galpón disponible, pero CAPEX total del proyecto sigue incompleto',
  'Flujo proyectado incompleto',
  'Agua sin dimensionamiento definitivo',
  'Energía solar sin dimensionamiento definitivo',
  'Logística rural/invierno pendiente',
  'Legal/contable pendiente',
  'P1 preliminar no habilitado'
];

const ALLOWED_ACTIONS = [
  'Levantar cotizaciones',
  'Línea comercial: Nacho valida ventas, clientes y canales',
  'Línea constructiva: Jean debe validar la cotización formal V8 y ajustar su aplicabilidad al escenario 500 aves, sin autorizar construcción.',
  'Medir agua y energía',
  'Preparar croquis',
  'Avanzar en CAPEX',
  'Mejorar dashboard y trazabilidad'
];

const BLOCKED_ACTIONS = [
  'No comprar 500 pollonas',
  'No construir el galpón',
  'No hacer inversión mayor',
  'No asumir rentabilidad cerrada',
  'No pasar a P1 preliminar como habilitado'
];

const MARKET_REFERENCE_FALLBACK = 'Referencia externa de precios de mercado: abril-mayo 2026, datos anonimizados. No es evidencia de ventas, compras ni clientes de Nacho.';

function $(id) {
  return document.getElementById(id);
}

function setText(id, value) {
  const node = $(id);
  if (node) node.textContent = value ?? 'pendiente';
}

function normalizeStatus(value) {
  return String(value ?? 'pendiente').replaceAll('_', '-').replaceAll('/', '-').toLowerCase();
}

function findIndicator(data, key) {
  const items = Array.isArray(data?.indicadores) ? data.indicadores : [];
  return items.find((item) => item?.indicador === key)?.valor;
}

function formatValue(value, unit = '') {
  if (value === undefined || value === null || value === '') return 'pendiente';
  return `${value}${unit ? ` ${unit}` : ''}`;
}

function formatCurrency(value) {
  if (value === undefined || value === null || value === '' || value === 'pendiente') return 'pendiente';
  if (Number.isNaN(Number(value))) return String(value);
  return `$${Number(value).toLocaleString('es-CL')}`;
}

function formatFinancialValue(indicator) {
  const value = indicator?.valor;
  if (value === undefined || value === null || value === '') return 'Pendiente';
  const unit = indicator?.unidad ?? '';
  if (unit.startsWith('CLP')) return formatCurrency(value);
  if (unit === '%') return `${Number(value).toLocaleString('es-CL')}%`;
  return `${Number(value).toLocaleString('es-CL')}${unit ? ` ${unit}` : ''}`;
}

function formatIndicatorState(state) {
  const labels = {
    cotizado_final_referencial: 'Cotizado final referencial',
    referencial_proporcional: 'Referencial proporcional',
    parcial: 'Parcial',
    pendiente: 'Pendiente',
    bloqueado_por_datos: 'Bloqueado por datos',
    no_aplica_aun: 'No aplica aún'
  };
  return labels[state] ?? 'Pendiente';
}

function createMetric({ label, value, detail = '', tone = '' }) {
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
  metrics.forEach((metric) => container.appendChild(createMetric(metric)));
}

function renderList(containerId, items, className = '') {
  const container = $(containerId);
  if (!container) return;
  container.innerHTML = '';
  items.forEach((item) => {
    const li = document.createElement('li');
    li.className = className;
    li.textContent = item;
    container.appendChild(li);
  });
}

function renderDecisionState({ resumen, estado, criteriosP1, semaforo }) {
  const escenarioBase = resumen?.escenario_base_actual?.aves ?? estado?.escenario_base_actual ?? 500;
  const estadoGeneral = resumen?.estado_general ?? semaforo?.semaforo_general ?? estado?.semaforo_general ?? 'amarillo';
  const decision = resumen?.decision_actual ?? {};
  const criterioDecision = criteriosP1?.decision_actual ?? {};
  const semaforoDecision = semaforo?.decisiones ?? {};

  const p1Preliminar = decision.p1_preliminar
    ?? (criterioDecision.p1_preliminar === false || estado?.p1_preliminar_habilitado === false || semaforo?.p1_preliminar_habilitado === false ? 'no habilitado' : 'pendiente');
  const compraAves = decision.compra_aves
    ?? decision.compra_500_pollonas
    ?? (criterioDecision.compra_aves === false || estado?.compra_aves_autorizada === false || semaforoDecision.puede_comprar_aves === false ? 'bloqueada' : 'pendiente');
  const construccion = decision.construccion
    ?? (criterioDecision.construccion === false || estado?.construccion_autorizada === false || semaforoDecision.puede_construir === false ? 'no autorizada' : 'pendiente');
  const inversionMayor = criterioDecision.inversion_mayor === false || estado?.inversion_mayor_autorizada === false || semaforoDecision.inversion_mayor_autorizada === false
    ? 'bloqueada'
    : (decision.inversion_mayor ?? 'pendiente');
  const decisionFinal = semaforoDecision.decision_final_disponible === false ? 'no disponible' : 'pendiente';

  setText('header-escenario', `${escenarioBase} aves`);
  setText('header-estado', estadoGeneral);
  setText('estado-general', estadoGeneral);
  setText('p1-preliminar', p1Preliminar);
  setText('compra-aves', compraAves);
  setText('construccion', construccion);
  setText('inversion-mayor', inversionMayor);
  setText('decision-final', decisionFinal);
}

function renderOperacion({ productivos, comerciales }) {
  const current = FALLBACKS.operacion;
  const metrics = [
    { label: 'Gallinas actuales', value: findIndicator(productivos, 'gallinas_actuales') ?? current.gallinas, detail: 'aves' },
    { label: 'Producción promedio', value: findIndicator(productivos, 'produccion_promedio_huevos_dia') ?? current.huevosDia, detail: 'huevos/día' },
    { label: 'Venta actual', value: findIndicator(comerciales, 'venta_actual_bandejas_semana') ?? current.bandejasSemana, detail: 'bandejas/semana' },
    { label: 'Postura promedio', value: findIndicator(productivos, 'postura_promedio_porcentaje') ?? current.postura, detail: '%' },
    { label: 'Mortalidad acumulada', value: findIndicator(productivos, 'mortalidad_acumulada_porcentaje') ?? current.mortalidad, detail: '%' },
    { label: 'Agua actual', value: findIndicator(productivos, 'consumo_agua_litros_dia') ?? current.aguaDia, detail: 'L/día' },
    { label: 'Edad lote', value: current.edad, detail: 'semanas' },
    { label: 'Raza', value: current.raza }
  ];
  renderMetrics('operacion-metricas', metrics);
}

function renderEscenario500({ validacionComercial, comerciales, flujoCaja, galpones }) {
  const escenario = validacionComercial?.escenario_500 ?? flujoCaja?.escenario_500 ?? {};
  const galpon500 = (galpones?.escenarios || []).find((item) => Number(item?.aves) === 500) ?? {};
  const base = FALLBACKS.escenario500;
  const referenciaV8 = galpones?.capex_referencial_formal ?? base.referenciaV8;

  const metrics = [
    { label: 'Escenario base vigente', value: formatValue(escenario.aves ?? base.aves, 'aves totales'), tone: 'accent' },
    { label: 'Producción estimada', value: formatValue(escenario.huevos_dia_estimados ?? base.huevosDia, 'huevos/día') },
    { label: 'Bandejas estimadas', value: formatValue(escenario.bandejas_semana_estimadas ?? findIndicator(comerciales, 'bandejas_semana_estimadas_500_aves') ?? base.bandejasSemana, 'bandejas/semana') },
    { label: 'Venta actual', value: formatValue(validacionComercial?.venta_actual_bandejas_semana ?? findIndicator(comerciales, 'venta_actual_bandejas_semana') ?? base.ventaActual, 'bandejas/semana') },
    { label: 'Brecha comercial', value: formatValue(escenario.brecha_bandejas_semana ?? findIndicator(comerciales, 'brecha_bandejas_semana_para_500') ?? base.brecha, 'bandejas/semana'), tone: 'risk' },
    { label: 'Agua estimada', value: base.agua },
    { label: 'Galpón 500 base cotizado', value: formatCurrency(galpon500.costo_total ?? base.costoGalponEscenario), detail: `${galpon500.superficie_util_m2 ?? referenciaV8.superficie_m2 ?? base.superficie} m² · ${formatCurrency(galpon500.costo_m2 ?? referenciaV8.costo_m2_aprox_clp ?? base.costoM2Galpon)}/m²`, tone: 'pending' },
    { label: 'Densidad galpón 500', value: `${galpon500.densidad_aprox_aves_m2 ?? base.densidadGalpon} gallinas/m² aprox.`, detail: '500 gallinas / 72 m²', tone: 'pending' }
  ];

  renderMetrics('escenario-500-metricas', metrics);
}

function renderEscalas(galpones) {
  const container = $('comparativo-escalas');
  if (!container) return;
  container.innerHTML = '';

  const defaults = [
    { aves: 500, superficie_util_m2: 72, costo_m2: 77052, costo_total: 5547765, estado: 'base financiero con cotización formal final COT-GN-0035; no autoriza construcción' },
    { aves: 1000, superficie_util_m2: 144, costo_m2: 77052, costo_total: 11095530, estado: 'proporcional referencial; no habilita inversión' },
    { aves: 2000, superficie_util_m2: 288, costo_m2: 77052, costo_total: 22191060, estado: 'proporcional referencial; no habilita inversión' }
  ];

  const scenarios = defaults.map((fallback) => {
    const source = (galpones?.escenarios || []).find((item) => Number(item?.aves) === fallback.aves) ?? {};
    return { ...fallback, ...source };
  });

  scenarios.forEach((scenario) => {
    const isBase = Number(scenario.aves) === 500;
    const card = document.createElement('article');
    card.className = `scale-card ${isBase ? 'base' : ''}`;
    card.innerHTML = `
      <div class="scale-head">
        <strong>${scenario.aves} aves</strong>
        <span>${isBase ? 'evaluándose' : 'comparativo futuro'}</span>
      </div>
      <dl>
        <div><dt>Superficie útil</dt><dd>${scenario.superficie_util_m2} m2</dd></div>
        <div><dt>Costo por m2</dt><dd>${formatCurrency(scenario.costo_m2)}</dd></div>
        <div><dt>Costo total galpón</dt><dd>${formatCurrency(scenario.costo_total)}</dd></div>
      </dl>
      <small>${scenario.estado ?? 'referencial; no autoriza inversión'}</small>
    `;
    container.appendChild(card);
  });
}

function renderFinancialIndicators({ finanzas, flujoCaja }) {
  const container = $('indicadores-financieros');
  if (!container) return;
  container.innerHTML = '';

  const indicators = finanzas?.catalogo_indicadores_financieros
    ?? flujoCaja?.catalogo_indicadores_financieros
    ?? [];

  indicators.forEach((indicator) => {
    const card = document.createElement('article');
    card.className = `financial-card state-${normalizeStatus(indicator.estado)}`;
    const helpText = indicator.descripcion_corta || indicator.formula || 'Indicador financiero del proyecto.';
    card.innerHTML = `
      <button class="indicator-help" type="button" title="${helpText}" aria-label="${helpText}">?</button>
      <div class="financial-card-head">
        <span>${indicator.escenario ?? '500 aves'}</span>
        <strong>${indicator.nombre}</strong>
      </div>
      <div class="financial-value">${formatFinancialValue(indicator)}</div>
      <div class="indicator-status">${formatIndicatorState(indicator.estado)}</div>
      <p>${indicator.estado_analisis ?? 'Pendiente de análisis financiero.'}</p>
      <small>${indicator.formula ? `Fórmula: ${indicator.formula}` : 'Fórmula: pendiente'} · Fuente: ${indicator.fuente ?? 'pendiente'}</small>
    `;
    container.appendChild(card);
  });
}

function renderWorkstreams({ resumen, validacionComercial, logisticaConstruccion }) {
  const container = $('lineas-trabajo');
  if (!container) return;
  container.innerHTML = '';

  const workstreams = resumen?.lineas_paralelas ?? [
    {
      linea: 'comercial',
      responsable: validacionComercial?.responsable ?? 'Nacho',
      objetivo: 'validar ventas, clientes y canales suficientes para el escenario 500 aves',
      evidencia_requerida: validacionComercial?.datos_que_debe_levantar_nacho ?? []
    },
    {
      linea: 'constructiva',
      responsable: logisticaConstruccion?.constructivo?.responsable_estudio ?? 'Jean',
      objetivo: 'validar la cotización formal V8 y ajustar su aplicabilidad al escenario 500 aves, sin autorizar construcción',
      evidencia_requerida: logisticaConstruccion?.constructivo?.datos_faltantes ?? [],
      advertencia: logisticaConstruccion?.constructivo?.advertencia_autorizacion
    }
  ];

  workstreams.forEach((stream) => {
    const card = document.createElement('article');
    card.className = 'workstream-card';
    const evidence = (stream.evidencia_requerida ?? []).slice(0, 6).map((item) => `<li>${item}</li>`).join('');
    card.innerHTML = `
      <div class="section-kicker">Línea ${stream.linea}</div>
      <h3>${stream.responsable}</h3>
      <p>${stream.objetivo}</p>
      ${evidence ? `<ul>${evidence}</ul>` : ''}
      ${stream.advertencia ? `<div class="alert-callout compact">${stream.advertencia}</div>` : ''}
    `;
    container.appendChild(card);
  });

  const greenCriteria = $('criterio-verde');
  if (greenCriteria) {
    greenCriteria.textContent = 'El proyecto solo podría pasar a verde si se validan con evidencia suficiente la línea comercial y la línea constructiva.';
  }
}

function renderMarketReferences(referenciasMercado) {
  const summary = $('referencia-mercado-resumen');
  const container = $('referencias-mercado');
  if (summary) summary.textContent = referenciasMercado?.advertencia_publica ?? MARKET_REFERENCE_FALLBACK;
  if (!container) return;
  container.innerHTML = '';

  const references = referenciasMercado?.referencias ?? [];
  references.forEach((reference) => {
    const card = document.createElement('article');
    card.className = 'market-card';
    const products = (reference.productos ?? []).map((item) => `
      <li><strong>${item.producto}</strong>: ${item.cantidad_cajas} cajas · $${Number(item.precio_neto_unitario_aprox_clp).toLocaleString('es-CL')} neto unitario aprox.</li>
    `).join('');
    card.innerHTML = `
      <span>${reference.periodo}</span>
      <strong>${reference.proveedor}</strong>
      <ul>${products}</ul>
      <small>Total IVA incluido: $${Number(reference.total_factura_iva_incluido_clp).toLocaleString('es-CL')}</small>
    `;
    container.appendChild(card);
  });
}

function renderSemaforo() {
  const container = $('semaforo-inversion');
  if (!container) return;
  container.innerHTML = '';

  TRAFFIC_RULES.forEach((rule) => {
    const card = document.createElement('article');
    card.className = `traffic-card ${rule.color} ${rule.active ? 'active' : ''}`;
    card.innerHTML = `
      <span>${rule.title}</span>
      <strong>${rule.decision}</strong>
      <p>${rule.detail}</p>
      ${rule.active ? '<em>Estado actual del proyecto</em>' : ''}
    `;
    container.appendChild(card);
  });
}

function renderBlockers() {
  const container = $('bloqueadores');
  if (!container) return;
  container.innerHTML = '';
  BLOCKERS.forEach((blocker) => {
    const item = document.createElement('div');
    item.className = 'blocker-item';
    item.innerHTML = `<span aria-hidden="true">!</span><strong>${blocker}</strong>`;
    container.appendChild(item);
  });
}

function renderActionLists() {
  renderList('acciones-permitidas', ALLOWED_ACTIONS);
  renderList('acciones-bloqueadas', BLOCKED_ACTIONS);
}

function renderRisks(semaforo) {
  const container = $('riesgos-clave');
  if (!container) return;
  container.innerHTML = '';

  const dimensions = semaforo?.dimensiones ?? {};
  const orderedKeys = ['comercial', 'financiera', 'logistica', 'sanitaria', 'agua', 'energia', 'legal', 'contable'];

  orderedKeys.forEach((key) => {
    const estado = dimensions[key]?.estado ?? 'pendiente';
    const card = document.createElement('article');
    card.className = `risk-card state-${normalizeStatus(estado)}`;
    card.innerHTML = `
      <div class="risk-topline">
        <strong>${labelForRisk(key)}</strong>
        <span>${estado}</span>
      </div>
      <p>${RISK_COPY[key]}</p>
    `;
    container.appendChild(card);
  });
}

function labelForRisk(key) {
  const labels = {
    comercial: 'Comercial',
    financiera: 'Financiero',
    logistica: 'Logístico',
    sanitaria: 'Sanitario',
    agua: 'Agua',
    energia: 'Energía',
    legal: 'Legal',
    contable: 'Contable'
  };
  return labels[key] ?? key;
}

function renderConclusion(resumen, semaforo) {
  const fallback = 'P0 amarillo. No se autoriza compra, construcción ni inversión mayor.';
  const conclusion = resumen?.conclusion || semaforo?.conclusion || fallback;
  setText('conclusion-ejecutiva', conclusion);
}

async function loadJson(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`No se pudo cargar ${path}`);
  return response.json();
}

async function loadData() {
  const entries = await Promise.all(
    Object.entries(DATA_FILES).map(async ([key, path]) => {
      try {
        return [key, await loadJson(path)];
      } catch (error) {
        console.warn(error);
        return [key, null];
      }
    })
  );
  return Object.fromEntries(entries);
}

async function init() {
  const data = await loadData();
  renderDecisionState(data);
  renderOperacion(data);
  renderEscenario500(data);
  renderEscalas(data.galpones);
  renderFinancialIndicators(data);
  renderWorkstreams(data);
  renderMarketReferences(data.referenciasMercado);
  renderSemaforo();
  renderBlockers();
  renderActionLists();
  renderRisks(data.semaforo);
  renderConclusion(data.resumen, data.semaforo);
}

document.addEventListener('DOMContentLoaded', init);

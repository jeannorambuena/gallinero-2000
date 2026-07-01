const DATA_FILES = {
  resumen: '/data/resumen-ejecutivo-p0.json',
  estado: '/data/estado-proyecto.json',
  productivos: '/data/indicadores-productivos.json',
  comerciales: '/data/indicadores-comerciales.json',
  validacionComercial: '/data/validacion-comercial.json',
  logisticaConstruccion: '/data/logistica-construccion.json',
  referenciasMercado: '/data/referencias_mercado.json',
  flujoCaja: '/data/flujo-caja-preliminar.json',
  semaforo: '/data/semaforo-decision.json',
  criteriosP1: '/data/criterios-p1.json',
  galpones: '/data/estimacion-galpones.json',
  alertas: '/data/alertas-p0.json'
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
    superficie: 100,
    costoGalpon: '$5.547.765 ref. 72 m2'
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
  'Línea constructiva: Jean usa cotización formal V8 como estudio técnico trazable',
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

  setText('header-escenario', `${escenarioBase} aves`);
  setText('header-estado', estadoGeneral);
  setText('estado-general', estadoGeneral);
  setText('p1-preliminar', decision.p1_preliminar ?? (criterioDecision.p1_preliminar === false ? 'no habilitado' : 'pendiente'));
  setText('compra-aves', decision.compra_500_pollonas ?? (criterioDecision.compra_aves === false ? 'bloqueada' : 'pendiente'));
  setText('construccion', decision.construccion ?? (criterioDecision.construccion === false ? 'no autorizada' : 'pendiente'));
  setText('inversion-mayor', decision.inversion_mayor ?? (criterioDecision.inversion_mayor === false ? 'no autorizada' : 'pendiente'));
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

  const metrics = [
    { label: 'Escenario base vigente', value: formatValue(escenario.aves ?? base.aves, 'aves totales'), tone: 'accent' },
    { label: 'Producción estimada', value: formatValue(escenario.huevos_dia_estimados ?? base.huevosDia, 'huevos/día') },
    { label: 'Bandejas estimadas', value: formatValue(escenario.bandejas_semana_estimadas ?? findIndicator(comerciales, 'bandejas_semana_estimadas_500_aves') ?? base.bandejasSemana, 'bandejas/semana') },
    { label: 'Venta actual', value: formatValue(validacionComercial?.venta_actual_bandejas_semana ?? findIndicator(comerciales, 'venta_actual_bandejas_semana') ?? base.ventaActual, 'bandejas/semana') },
    { label: 'Brecha comercial', value: formatValue(escenario.brecha_bandejas_semana ?? findIndicator(comerciales, 'brecha_bandejas_semana_para_500') ?? base.brecha, 'bandejas/semana'), tone: 'risk' },
    { label: 'Agua estimada', value: base.agua },
    { label: 'Superficie útil galpón', value: formatValue(galpon500.superficie_util_m2 ?? base.superficie, 'm2') },
    { label: 'Costo estimado galpón', value: galpon500.costo_total === 'pendiente' ? base.costoGalpon : formatCurrency(galpon500.costo_total ?? base.costoGalpon), detail: galpon500.fuente_costo_m2 ?? 'referencial formal V8', tone: 'pending' }
  ];

  renderMetrics('escenario-500-metricas', metrics);
}

function renderEscalas(galpones) {
  const container = $('comparativo-escalas');
  if (!container) return;
  container.innerHTML = '';

  const defaults = [
    { aves: 500, superficie_util_m2: 100, estado: 'evaluándose' },
    { aves: 1000, superficie_util_m2: 200, estado: 'comparativo futuro' },
    { aves: 2000, superficie_util_m2: 400, estado: 'comparativo futuro' }
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
      objetivo: 'cotizar y diseñar técnicamente el galpón como estudio constructivo',
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
  renderWorkstreams(data);
  renderMarketReferences(data.referenciasMercado);
  renderSemaforo();
  renderBlockers();
  renderActionLists();
  renderRisks(data.semaforo);
  renderConclusion(data.resumen, data.semaforo);
}

document.addEventListener('DOMContentLoaded', init);

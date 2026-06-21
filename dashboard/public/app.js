const DATA_FILES = {
  estado: '/data/estado-proyecto.json',
  productivos: '/data/indicadores-productivos.json',
  comerciales: '/data/indicadores-comerciales.json',
  finanzas: '/data/finanzas-preliminares.json',
  semaforo: '/data/semaforo-decision.json',
  alertas: '/data/alertas-p0.json',
  datosFaltantes: '/data/datos-faltantes.json',
  subproyectos: '/data/subproyectos-criticos.json',
  logisticaConstruccion: '/data/logistica-construccion.json'
};

const DIMENSION_ORDER = [
  'productiva',
  'comercial',
  'financiera',
  'constructiva',
  'logistica',
  'agua',
  'energia',
  'sanitaria',
  'legal',
  'contable',
  'escalabilidad'
];

const DIMENSION_LABELS = {
  productiva: 'Productiva',
  comercial: 'Comercial',
  financiera: 'Financiera',
  constructiva: 'Constructiva',
  logistica: 'Logística',
  agua: 'Agua',
  energia: 'Energía',
  sanitaria: 'Sanitaria',
  legal: 'Legal',
  contable: 'Contable',
  escalabilidad: 'Escalabilidad'
};

const estadoLabel = (value, enabledText = 'habilitado') => value ? enabledText : 'no habilitado';
const autorizadoLabel = (value) => value ? 'autorizada' : 'no autorizada';
const disponibleLabel = (value) => value ? 'disponible' : 'no disponible';

const formatClp = (value) => `$${Number(value).toLocaleString('es-CL')}`;
const text = (id, value) => {
  const node = document.getElementById(id);
  if (node) node.textContent = value;
};

function indexIndicators(data) {
  return Object.fromEntries((data.indicadores || []).map((item) => [item.indicador, item]));
}

function indicatorValue(index, key) {
  return index[key]?.valor ?? '—';
}

function renderList(containerId, rows) {
  const container = document.getElementById(containerId);
  container.innerHTML = '';

  rows.forEach(([label, value]) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'data-row';

    const term = document.createElement('dt');
    term.textContent = label;

    const description = document.createElement('dd');
    description.textContent = value;

    wrapper.append(term, description);
    container.appendChild(wrapper);
  });
}

function badgeClass(estado) {
  if (estado === 'verde') return 'badge-verde';
  if (estado === 'amarillo_rojo') return 'badge-amarillo-rojo';
  if (estado === 'pendiente/amarillo') return 'badge-amarillo';
  if (estado === 'amarillo') return 'badge-amarillo';
  return 'badge-pendiente';
}

function severityClass(severidad) {
  if (severidad === 'alta') return 'severity-alta';
  if (severidad === 'media') return 'severity-media';
  return 'severity-pendiente';
}

async function loadJson(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`No se pudo cargar ${path}`);
  return response.json();
}

function renderAlertas(alertasData) {
  const container = document.getElementById('alertas-p0');
  container.innerHTML = '';

  (alertasData.alertas || []).forEach((alerta) => {
    const item = document.createElement('article');
    item.className = `alert-card ${severityClass(alerta.severidad)}`;

    const meta = document.createElement('div');
    meta.className = 'alert-meta';

    const id = document.createElement('span');
    id.textContent = alerta.id;

    const severity = document.createElement('span');
    severity.className = 'alert-severity';
    severity.textContent = alerta.severidad;

    meta.append(id, severity);

    const title = document.createElement('h3');
    title.textContent = alerta.titulo;

    const description = document.createElement('p');
    description.textContent = alerta.descripcion;

    const footer = document.createElement('p');
    footer.className = 'alert-footer';
    footer.textContent = `${alerta.dimension} · ${alerta.estado}`;

    item.append(meta, title, description, footer);
    container.appendChild(item);
  });
}

function renderDatosFaltantes(datosData) {
  const container = document.getElementById('datos-faltantes');
  container.innerHTML = '';

  (datosData.grupos || []).forEach((grupo) => {
    const item = document.createElement('article');
    item.className = `missing-group priority-${grupo.prioridad}`;

    const header = document.createElement('div');
    header.className = 'missing-header';

    const title = document.createElement('h3');
    title.textContent = grupo.grupo;

    const priority = document.createElement('span');
    priority.className = 'missing-priority';
    priority.textContent = grupo.prioridad;

    header.append(title, priority);

    const list = document.createElement('ul');
    (grupo.items || []).forEach((dato) => {
      const li = document.createElement('li');
      li.textContent = dato;
      list.appendChild(li);
    });

    item.append(header, list);
    container.appendChild(item);
  });
}

function renderBlockCard(container, label, bloque, className = 'subproject-card') {
  const card = document.createElement('article');
  card.className = className;

  const header = document.createElement('div');
  header.className = 'subproject-header';

  const title = document.createElement('h3');
  title.textContent = label;

  const badge = document.createElement('span');
  badge.className = `badge ${badgeClass(bloque.estado)}`;
  badge.textContent = bloque.estado;

  header.append(title, badge);

  const knownTitle = document.createElement('h4');
  knownTitle.textContent = 'Datos conocidos principales';
  const knownList = document.createElement('ul');
  (bloque.datos_conocidos || []).slice(0, 5).forEach((dato) => {
    const li = document.createElement('li');
    li.textContent = dato;
    knownList.appendChild(li);
  });

  const risksTitle = document.createElement('h4');
  risksTitle.textContent = 'Riesgos principales';
  const risksList = document.createElement('ul');
  (bloque.riesgos || []).slice(0, 5).forEach((riesgo) => {
    const li = document.createElement('li');
    li.textContent = riesgo;
    risksList.appendChild(li);
  });

  const missingTitle = document.createElement('h4');
  missingTitle.textContent = 'Faltantes principales';
  const missingList = document.createElement('ul');
  (bloque.datos_faltantes || []).slice(0, 6).forEach((dato) => {
    const li = document.createElement('li');
    li.textContent = dato;
    missingList.appendChild(li);
  });

  const condition = document.createElement('p');
  condition.className = 'subproject-condition';
  condition.textContent = bloque.condicion_para_avanzar;

  card.append(header, knownTitle, knownList, risksTitle, risksList, missingTitle, missingList, condition);
  container.appendChild(card);
}

function renderSubproyectos(subproyectosData) {
  const container = document.getElementById('subproyectos-criticos');
  container.innerHTML = '';

  const labels = {
    agua: 'Agua',
    energia_solar: 'Energía solar'
  };

  Object.entries(subproyectosData.subproyectos || {}).forEach(([key, subproyecto]) => {
    renderBlockCard(container, labels[key] || key, subproyecto);
  });

  text('subproyectos-advertencia', subproyectosData.advertencia || 'Los subproyectos críticos no habilitan compra todavía.');
}

function renderLogisticaConstruccion(logisticaData) {
  const container = document.getElementById('logistica-construccion');
  container.innerHTML = '';

  renderBlockCard(container, 'Construcción', logisticaData.constructivo, 'logistics-card');
  renderBlockCard(container, 'Logística', logisticaData.logistico, 'logistics-card');

  text('logistica-advertencia', logisticaData.advertencia || 'No se puede cerrar P0 ni iniciar P1 definitivo sin resolver este bloque.');
}

async function init() {
  try {
    const [estado, productivos, comerciales, finanzas, semaforo, alertas, datosFaltantes, subproyectos, logisticaConstruccion] = await Promise.all([
      loadJson(DATA_FILES.estado),
      loadJson(DATA_FILES.productivos),
      loadJson(DATA_FILES.comerciales),
      loadJson(DATA_FILES.finanzas),
      loadJson(DATA_FILES.semaforo),
      loadJson(DATA_FILES.alertas),
      loadJson(DATA_FILES.datosFaltantes),
      loadJson(DATA_FILES.subproyectos),
      loadJson(DATA_FILES.logisticaConstruccion)
    ]);

    const prod = indexIndicators(productivos);
    const com = indexIndicators(comerciales);
    const fin = indexIndicators(finanzas);

    text('semaforo-general', `Semáforo general: ${semaforo.semaforo_general || estado.semaforo_general}`);
    text('avance-p0', `Avance P0: ${semaforo.avance_p0_estimado || estado.avance_p0_estimado}%`);
    text('fase-actual', semaforo.fase || estado.fase_actual);
    text('card-avance-p0', `${semaforo.avance_p0_estimado || estado.avance_p0_estimado}%`);
    text('p1-preliminar', estadoLabel(semaforo.p1_preliminar_habilitado, 'habilitado'));
    text('p1-definitivo', estadoLabel(semaforo.p1_definitivo_habilitado, 'habilitado'));
    text('compra-pollonas', autorizadoLabel(semaforo.decisiones?.puede_comprar_500_pollonas));
    text('decision-final', disponibleLabel(semaforo.decisiones?.decision_final_disponible));

    renderList('indicadores-productivos', [
      ['Gallinas actuales', `${indicatorValue(prod, 'gallinas_actuales')}`],
      ['Producción promedio', `${indicatorValue(prod, 'produccion_promedio_huevos_dia')} huevos/día`],
      ['Postura promedio', `${indicatorValue(prod, 'postura_promedio_porcentaje')}%`],
      ['Mortalidad acumulada', `${indicatorValue(prod, 'mortalidad_acumulada_porcentaje')}%`],
      ['Densidad', `${indicatorValue(prod, 'densidad_actual_aves_m2')} aves/m2`],
      ['Agua por ave/día', `${indicatorValue(prod, 'agua_litros_ave_dia')} L`]
    ]);

    renderList('indicadores-comerciales', [
      ['Venta actual', `${indicatorValue(com, 'venta_actual_bandejas_semana')} bandejas/semana`],
      ['Ingreso semanal', formatClp(indicatorValue(com, 'ingreso_semanal_actual'))],
      ['Ingreso mensual estimado', formatClp(indicatorValue(com, 'ingreso_mensual_estimado'))],
      ['Venta requerida para 648 aves', `${indicatorValue(com, 'bandejas_semana_proyectadas_648_aves')} bandejas/semana`],
      ['Brecha actual', `${indicatorValue(com, 'brecha_bandejas_semana_para_648')} bandejas/semana`],
      ['Crecimiento requerido', `${indicatorValue(com, 'crecimiento_requerido_veces')} veces`]
    ]);

    renderList('finanzas-preliminares', [
      ['Costos conocidos mensuales', formatClp(indicatorValue(fin, 'costos_conocidos_mensuales'))],
      ['Margen sin mano de obra', formatClp(indicatorValue(fin, 'margen_preliminar_sin_mano_obra'))],
      ['Mano de obra valorizada', formatClp(indicatorValue(fin, 'mano_obra_valorizada_mensual'))],
      ['Margen con mano de obra', formatClp(indicatorValue(fin, 'margen_preliminar_con_mano_obra'))],
      ['CAPEX conocido pollonas', formatClp(indicatorValue(fin, 'capex_conocido_pollonas'))]
    ]);

    const bloqueados = (finanzas.indicadores_bloqueados || []).map((item) => item.indicador).join(', ');
    text('indicadores-bloqueados', bloqueados ? `${bloqueados}: pendientes` : 'ROI, VAN, TIR y Payback: pendientes');

    const semaforoContainer = document.getElementById('semaforo-dimensiones');
    semaforoContainer.innerHTML = '';
    DIMENSION_ORDER.forEach((key) => {
      const dimension = semaforo.dimensiones?.[key];
      if (!dimension) return;

      const item = document.createElement('div');
      item.className = 'dimension';

      const label = document.createElement('strong');
      label.textContent = DIMENSION_LABELS[key] || key;

      const badge = document.createElement('span');
      badge.className = `badge ${badgeClass(dimension.estado)}`;
      badge.textContent = dimension.estado;

      item.append(label, badge);
      semaforoContainer.appendChild(item);
    });

    renderAlertas(alertas);
    renderDatosFaltantes(datosFaltantes);
    renderSubproyectos(subproyectos);
    renderLogisticaConstruccion(logisticaConstruccion);

    const condiciones = document.getElementById('condiciones-avanzar');
    condiciones.innerHTML = '';
    (semaforo.condiciones_para_avanzar || []).forEach((condition) => {
      const item = document.createElement('li');
      item.textContent = condition;
      condiciones.appendChild(item);
    });

    text('estado-carga', 'Datos cargados desde JSON locales.');
  } catch (error) {
    console.error(error);
    text('estado-carga', 'Error al cargar datos del dashboard.');
    document.getElementById('estado-carga')?.classList.add('error');
  }
}

init();

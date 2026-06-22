const DATA_FILES = {
  resumenEjecutivo: '/data/resumen-ejecutivo-p0.json',
  estado: '/data/estado-proyecto.json',
  productivos: '/data/indicadores-productivos.json',
  comerciales: '/data/indicadores-comerciales.json',
  finanzas: '/data/finanzas-preliminares.json',
  semaforo: '/data/semaforo-decision.json',
  alertas: '/data/alertas-p0.json',
  datosFaltantes: '/data/datos-faltantes.json',
  subproyectos: '/data/subproyectos-criticos.json',
  logisticaConstruccion: '/data/logistica-construccion.json',
  validacionComercial: '/data/validacion-comercial.json',
  legalContable: '/data/legal-contable.json',
  capex: '/data/capex-preliminar.json',
  flujoCaja: '/data/flujo-caja-preliminar.json',
  criteriosP1: '/data/criterios-p1.json',
  desbloqueoP1: '/data/desbloqueo-p1-preliminar.json'
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

function renderUl(containerId, items, limit = items?.length ?? 0) {
  const container = document.getElementById(containerId);
  container.innerHTML = '';

  (items || []).slice(0, limit).forEach((text) => {
    const li = document.createElement('li');
    li.textContent = text;
    container.appendChild(li);
  });
}

function badgeClass(estado) {
  if (estado === 'verde' || estado === 'cumplido') return 'badge-verde';
  if (estado === 'amarillo_rojo' || estado === 'bloqueante') return 'badge-amarillo-rojo';
  if (estado === 'pendiente/amarillo' || estado === 'amarillo' || estado === 'parcial') return 'badge-amarillo';
  return 'badge-pendiente';
}

function stateClass(estado) {
  if (!estado) return 'state-pendiente';
  return `state-${String(estado).replace('/', '-').replace('_', '-')}`;
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

function renderResumenEjecutivo(resumenData) {
  const badge = document.getElementById('resumen-ejecutivo-estado');
  if (badge) {
    badge.className = `badge ${badgeClass(resumenData.estado_general)}`;
    badge.textContent = `Estado general: ${resumenData.estado_general}`;
  }

  renderList('resumen-ejecutivo-decision', [
    ['Avance P0', `${resumenData.avance_p0_estimado}%`],
    ['P1 preliminar', resumenData.decision_actual?.p1_preliminar || '—'],
    ['P1 definitivo', resumenData.decision_actual?.p1_definitivo || '—'],
    ['Compra 500 pollonas', resumenData.decision_actual?.compra_500_pollonas || '—'],
    ['Construcción', resumenData.decision_actual?.construccion || '—'],
    ['Inversión mayor', resumenData.decision_actual?.inversion_mayor || '—']
  ]);

  renderUl('resumen-puntos-favorables', resumenData.puntos_favorables, 7);
  renderUl('resumen-riesgos-principales', resumenData.riesgos_principales, 8);
  renderUl('resumen-acciones-recomendadas', resumenData.acciones_recomendadas, 7);
  text('resumen-ejecutivo-conclusion', resumenData.conclusion || 'Resumen ejecutivo no disponible.');
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

function renderValidacionComercial(comercialData) {
  const badge = document.getElementById('validacion-comercial-estado');
  if (badge) {
    badge.className = `badge ${badgeClass(comercialData.estado)}`;
    badge.textContent = comercialData.estado;
  }

  renderList('validacion-comercial-metricas', [
    ['Venta actual', `${comercialData.venta_actual_bandejas_semana} bandejas/semana`],
    ['Venta requerida', `${comercialData.venta_requerida_648_bandejas_semana} bandejas/semana`],
    ['Brecha', `${comercialData.brecha_bandejas_semana} bandejas/semana`],
    ['Crecimiento requerido', `${comercialData.crecimiento_requerido_veces} veces`]
  ]);

  renderUl('canales-actuales', comercialData.canales_actuales);
  renderUl('canales-potenciales', comercialData.canales_potenciales);
  text('validacion-comercial-conclusion', comercialData.conclusion || 'No comprar sin validar mercado.');
}

function renderLegalContable(legalData) {
  const badge = document.getElementById('legal-contable-estado');
  if (badge) {
    badge.className = `badge ${badgeClass(legalData.estado)}`;
    badge.textContent = legalData.estado;
  }

  renderUl('legal-temas', legalData.temas_a_revisar, 8);
  renderUl('legal-riesgos', legalData.riesgos, 6);
  text('legal-contable-advertencia', legalData.advertencia || 'No reemplaza revisión profesional.');
}

function renderCapex(capexData) {
  const badge = document.getElementById('capex-estado');
  if (badge) {
    badge.className = `badge ${badgeClass(capexData.estado)}`;
    badge.textContent = capexData.estado;
  }

  const montoPollonas = capexData.capex_conocido?.pollonas?.monto_clp ?? 0;
  const montoTotalConocido = capexData.capex_conocido?.monto_total_conocido_clp ?? 0;
  const montoPendiente = capexData.capex_pendiente?.monto_total_pendiente;

  renderList('capex-resumen', [
    ['CAPEX conocido pollonas', formatClp(montoPollonas)],
    ['CAPEX total conocido', formatClp(montoTotalConocido)],
    ['CAPEX total pendiente', montoPendiente === null || montoPendiente === undefined ? 'pendiente' : formatClp(montoPendiente)]
  ]);

  renderUl('capex-categorias-pendientes', capexData.capex_pendiente?.categorias_pendientes, 10);
  renderUl('capex-riesgos', capexData.riesgos, 6);
  text('capex-conclusion', capexData.conclusion || 'No comprar ni invertir sin CAPEX completo.');
}

function renderFlujoCaja(flujoData) {
  const badge = document.getElementById('flujo-estado');
  if (badge) {
    badge.className = `badge ${badgeClass(flujoData.estado)}`;
    badge.textContent = flujoData.estado;
  }

  renderList('flujo-resumen', [
    ['Ingreso mensual actual', formatClp(flujoData.ingresos_actuales?.ingreso_mensual_estimado_clp ?? 0)],
    ['Costos conocidos', formatClp(flujoData.costos_actuales?.total_costos_conocidos_clp ?? 0)],
    ['Margen sin mano de obra', formatClp(flujoData.margenes_actuales?.margen_sin_mano_obra_clp ?? 0)],
    ['Mano de obra referencial', formatClp(flujoData.mano_obra_referencial?.monto_clp ?? 0)],
    ['Margen con mano de obra', formatClp(flujoData.margenes_actuales?.margen_con_mano_obra_clp ?? 0)],
    ['CAPEX conocido', formatClp(flujoData.capex?.capex_conocido_pollonas_clp ?? 0)]
  ]);

  renderUl(
    'flujo-indicadores-bloqueados',
    (flujoData.indicadores_bloqueados || []).map((item) => `${item.indicador}: ${item.estado}`)
  );
  renderUl('flujo-riesgos', flujoData.riesgos, 6);
  text('flujo-conclusion', flujoData.conclusion || 'No autoriza inversión todavía.');
}

function renderDesbloqueoP1(desbloqueoData) {
  const badge = document.getElementById('desbloqueo-p1-estado');
  if (badge) {
    badge.className = `badge ${badgeClass(desbloqueoData.estado_desbloqueo)}`;
    badge.textContent = desbloqueoData.estado_desbloqueo;
  }

  text('desbloqueo-p1-objetivo', desbloqueoData.objetivo || '—');
  renderUl(
    'desbloqueo-tareas',
    (desbloqueoData.tareas_por_dimension || []).map((item) => `${item.dimension}: ${item.tarea} (${item.estado})`),
    12
  );
  renderUl(
    'desbloqueo-instrumentos',
    [
      ...(desbloqueoData.documentos_creados || []).map((item) => `doc: ${item}`),
      ...(desbloqueoData.plantillas_csv || []).map((item) => `csv: ${item}`)
    ],
    12
  );
  renderUl('desbloqueo-decisiones', desbloqueoData.decisiones_bloqueadas, 8);
  text('desbloqueo-proximo-paso', desbloqueoData.proximo_paso_recomendado || desbloqueoData.conclusion || 'Pendiente.');
}

function renderCriteriosP1(criteriosData) {
  const badge = document.getElementById('criterios-p1-estado');
  if (badge) {
    badge.className = 'badge badge-pendiente';
    badge.textContent = criteriosData.estado_p1_preliminar;
  }

  renderList('criterios-p1-resumen', [
    ['P1 preliminar', criteriosData.estado_p1_preliminar],
    ['P1 definitivo', criteriosData.estado_p1_definitivo],
    ['Compra pollonas', criteriosData.compra_pollonas]
  ]);

  const container = document.getElementById('criterios-p1-checklist');
  container.innerHTML = '';
  (criteriosData.criterios_minimos || []).forEach((criterio) => {
    const item = document.createElement('article');
    item.className = `diagnostic-block ${stateClass(criterio.estado)}`;

    const title = document.createElement('h3');
    title.textContent = `${criterio.id} · ${criterio.dimension} · ${criterio.estado}`;

    const description = document.createElement('p');
    description.textContent = criterio.criterio;

    const evidence = document.createElement('p');
    evidence.textContent = `Evidencia: ${criterio.evidencia}`;

    const action = document.createElement('p');
    action.textContent = `Acción requerida: ${criterio.accion_requerida}`;

    item.append(title, description, evidence, action);
    container.appendChild(item);
  });

  renderUl('bloqueos-p1-definitivo', criteriosData.bloqueos_p1_definitivo, 9);
  renderUl('bloqueos-compra-pollonas', criteriosData.bloqueos_compra_pollonas, 7);
  text('criterios-p1-conclusion', criteriosData.conclusion || 'P1 preliminar no habilitado.');
}

async function init() {
  try {
    const [resumenEjecutivo, estado, productivos, comerciales, finanzas, semaforo, alertas, datosFaltantes, subproyectos, logisticaConstruccion, validacionComercial, legalContable, capex, flujoCaja, criteriosP1, desbloqueoP1] = await Promise.all([
      loadJson(DATA_FILES.resumenEjecutivo),
      loadJson(DATA_FILES.estado),
      loadJson(DATA_FILES.productivos),
      loadJson(DATA_FILES.comerciales),
      loadJson(DATA_FILES.finanzas),
      loadJson(DATA_FILES.semaforo),
      loadJson(DATA_FILES.alertas),
      loadJson(DATA_FILES.datosFaltantes),
      loadJson(DATA_FILES.subproyectos),
      loadJson(DATA_FILES.logisticaConstruccion),
      loadJson(DATA_FILES.validacionComercial),
      loadJson(DATA_FILES.legalContable),
      loadJson(DATA_FILES.capex),
      loadJson(DATA_FILES.flujoCaja),
      loadJson(DATA_FILES.criteriosP1),
      loadJson(DATA_FILES.desbloqueoP1)
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

    renderResumenEjecutivo(resumenEjecutivo);
    renderAlertas(alertas);
    renderDatosFaltantes(datosFaltantes);
    renderSubproyectos(subproyectos);
    renderLogisticaConstruccion(logisticaConstruccion);
    renderValidacionComercial(validacionComercial);
    renderLegalContable(legalContable);
    renderCapex(capex);
    renderFlujoCaja(flujoCaja);
    renderDesbloqueoP1(desbloqueoP1);
    renderCriteriosP1(criteriosP1);

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

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
  alertas: new URL('alertas-p0.json', DATA_BASE).href,
  capexEquipamiento: new URL('capex-equipamiento-avicola.json', DATA_BASE).href,
  escenarioProporcional: new URL('escenario-proporcional-500.json', DATA_BASE).href,
  requerimientosEquipamiento: new URL('requerimientos-equipamiento-avicola.json', DATA_BASE).href,
  cotizacionEquipamiento: new URL('cotizacion-referencial-equipamiento-avicola.json', DATA_BASE).href,
  capexTotal500: new URL('capex-total-referencial-500.json', DATA_BASE).href,
  opex500: new URL('opex-proyectado-500.json', DATA_BASE).href,
  ingresos500: new URL('ingresos-proyectados-500.json', DATA_BASE).href,
  flujo500: new URL('flujo-financiero-preliminar-500.json', DATA_BASE).href,
  estrategiaPollonas: new URL('estrategia-compra-pollonas.json', DATA_BASE).href,
  decisionP47: new URL('decision-ejecutiva-p47.json', DATA_BASE).href,
  alternativasP47: new URL('alternativas-crecimiento-p47.json', DATA_BASE).href,
  planP47: new URL('plan-implementacion-6-meses.json', DATA_BASE).href,
  reglasP47: new URL('reglas-decision-semaforo-p47.json', DATA_BASE).href
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
    brecha: 4.1,
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
  comercial: 'Meta 100 bandejas/semana usada como escenario comercial base; faltan precios netos, forma de pago y estabilidad por canal.',
  productiva: 'Base actual parcialmente confirmada y con alto avance: 148 gallinas, 132 huevos/día y postura aprox. 89,2%.',
  financiera: 'P45-P47 ya tienen CAPEX/OPEX/flujo preliminares. Siguen faltando cotizaciones finales, financiamiento y capital de trabajo para invertir.',
  logistica: 'Acceso rural e invierno afectan materiales y operación; reparto actual 6 veces/mes con $10.000 de bencina.',
  sanitaria: 'Humedad, calor y manejo de agua aún requieren mejoras; $0 informado en medicamentos adicionales no elimina riesgo sanitario.',
  agua: 'Falta dimensionamiento definitivo de caudal, presión, bomba y respaldo.',
  energia: 'Panel solar comprado por $300.000, considerado paquete completo informado para bomba, luces y cámaras; pendiente solo verificación operativa en terreno.',
  legal: 'Intención de boleta/factura confirmada si escala; ruta, costos y trazabilidad siguen pendientes.',
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
  'AMARILLO no significa inviable; significa evidencia crítica pendiente antes de invertir',
  'Falta documentar compradores por canal, precios netos, forma de pago y estabilidad para sostener 100 bandejas/semana',
  'Diferencia técnica producción/meta: 4,1 bandejas/semana para merma, autoconsumo, stock o venta adicional',
  'CAPEX equipamiento avícola ya tiene estimación referencial; faltan selección y cotización final',
  'Indicadores avanzados ROI, VAN y TIR siguen pendientes; margen, payback simple y punto de equilibrio preliminares ya existen',
  'Mix actual confirmado: segunda 6, primera 13, extra 9',
  'Meta 100 bandejas/semana usada como escenario comercial base',
  'OPEX parcial confirmado no equivale a OPEX total',
  'Agua/bomba e instalaciones internas pendientes de cotización o verificación',
  'Panel solar comprado por $300.000 como paquete completo; verificar operación en terreno',
  'Logística rural/invierno pendiente',
  'Legal/contable pendiente',
  'P1 preliminar no habilitado'
];

const ALLOWED_ACTIONS = [
  'Levantar cotizaciones',
  'Línea comercial: Nacho valida precios netos, forma de pago y estabilidad por canal',
  'Línea constructiva: Jean debe validar la cotización formal V8 y ajustar su aplicabilidad al escenario 500 aves, sin autorizar construcción.',
  'Cotizar equipamiento avícola y verificar agua/energía en terreno',
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

function renderCompactRows(containerId, rows) {
  const container = $(containerId);
  if (!container) return;
  container.innerHTML = '';
  rows.forEach((row) => {
    const card = document.createElement('article');
    card.className = `financial-card ${row.tone ?? ''}`.trim();
    card.innerHTML = `
      <div class="financial-card-head">
        <span>${row.kicker ?? 'P45-P46'}</span>
        <strong>${row.title}</strong>
      </div>
      <div class="financial-value">${row.value}</div>
      ${row.detail ? `<p>${row.detail}</p>` : ''}
      ${row.small ? `<small>${row.small}</small>` : ''}
    `;
    container.appendChild(card);
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

function renderOperacion({ productivos, comerciales, finanzas, flujoCaja }) {
  const current = FALLBACKS.operacion;
  const metrics = [
    { label: 'Gallinas actuales', value: findIndicator(productivos, 'gallinas_actuales') ?? current.gallinas, detail: 'aves' },
    { label: 'Producción promedio', value: findIndicator(productivos, 'produccion_promedio_huevos_dia') ?? current.huevosDia, detail: 'huevos/día' },
    { label: 'Bandejas producidas aprox.', value: findIndicator(productivos, 'produccion_semanal_bandejas_aprox') ?? 30.8, detail: 'bandejas/semana' },
    { label: 'Venta actual', value: findIndicator(comerciales, 'venta_actual_bandejas_semana') ?? current.bandejasSemana, detail: 'bandejas/semana' },
    { label: 'Precio promedio actual', value: formatCurrency(findIndicator(comerciales, 'precio_promedio_por_bandeja') ?? 6107), detail: 'mix 6 segunda · 13 primera · 9 extra' },
    { label: 'Ingreso actual', value: formatCurrency(findIndicator(comerciales, 'ingreso_semanal_actual') ?? 171000), detail: '$741.000/mes aprox.' },
    { label: 'OPEX parcial', value: formatCurrency(findIndicator(finanzas, 'opex_parcial_confirmado') ?? 343640), detail: 'alimento + agua + vitaminas + envases + viruta + bencina', tone: 'pending' },
    { label: 'Margen parcial sin MO', value: formatCurrency(flujoCaja?.margenes_actuales?.margen_sin_mano_obra_clp ?? 397360), detail: 'no equivale a margen final 500 aves', tone: 'pending' },
    { label: 'Agua actual', value: findIndicator(productivos, 'consumo_agua_litros_dia') ?? current.aguaDia, detail: 'L/día' },
    { label: 'Infraestructura actual', value: '27 m²', detail: 'gallinero actual · terreno 133 m²' }
  ];
  renderMetrics('operacion-metricas', metrics);
}

function renderEscenario500({ validacionComercial, comerciales, flujoCaja, galpones, capexEquipamiento, ingresos500 }) {
  const escenario = validacionComercial?.escenario_500 ?? flujoCaja?.escenario_500 ?? {};
  const galpon500 = (galpones?.escenarios || []).find((item) => Number(item?.aves) === 500) ?? {};
  const base = FALLBACKS.escenario500;
  const referenciaV8 = galpones?.capex_referencial_formal ?? base.referenciaV8;

  const metrics = [
    { label: 'Escenario base vigente', value: formatValue(escenario.aves ?? base.aves, 'aves totales'), tone: 'accent' },
    { label: 'Bandejas estimadas', value: formatValue(escenario.bandejas_semana_estimadas ?? findIndicator(comerciales, 'bandejas_semana_estimadas_500_aves') ?? base.bandejasSemana, 'bandejas/semana') },
    { label: 'Meta comercial base', value: formatValue(validacionComercial?.meta_comercial_base_bandejas_semana ?? findIndicator(comerciales, 'meta_comercial_bandejas_semana') ?? 100, 'bandejas/semana'), detail: 'escenario base de análisis P43', tone: 'accent' },
    { label: 'Ingreso meta mensual', value: formatCurrency(ingresos500?.sensibilidades?.base?.ingreso_mensual_clp ?? 2646367), detail: '100 bandejas/semana' },
    { label: 'Diferencia técnica', value: formatValue(escenario.diferencia_tecnica_bandejas_semana ?? escenario.brecha_bandejas_semana ?? findIndicator(comerciales, 'diferencia_tecnica_produccion_meta_bandejas_semana') ?? base.brecha, 'bandejas/semana'), detail: 'merma · autoconsumo · stock · venta adicional', tone: 'pending' },
    { label: 'Agua estimada', value: base.agua },
    { label: 'Galpón 500 base cotizado', value: formatCurrency(galpon500.costo_total ?? base.costoGalponEscenario), detail: `${galpon500.superficie_util_m2 ?? referenciaV8.superficie_m2 ?? base.superficie} m² · ${formatCurrency(galpon500.costo_m2 ?? referenciaV8.costo_m2_aprox_clp ?? base.costoM2Galpon)}/m²`, tone: 'pending' },
    { label: 'Densidad galpón 500', value: `${galpon500.densidad_aprox_aves_m2 ?? base.densidadGalpon} gallinas/m² aprox.`, detail: '500 gallinas / 72 m²', tone: 'pending' },
    { label: 'CAPEX equipamiento avícola', value: formatCurrency(capexEquipamiento?.resumen?.capex_equipamiento_base_clp) ?? 'Referencial', detail: 'escenario base P45-P46 · requiere cotización final', tone: 'risk' },
    { label: 'Panel solar', value: formatCurrency(300000), detail: 'comprado · verificar operación', tone: 'pending' }
  ];

  renderMetrics('escenario-500-metricas', metrics);
}

function renderResumenFinancieroEjecutivo({ capexTotal500, opex500, flujo500, decisionP47 }) {
  const capexBase = capexTotal500?.capex_total_referencial?.base ?? {};
  const fullMoney = decisionP47?.respuestas_clave?.dinero_faltante_escenario_base ?? {};
  const paybackBase = flujo500?.payback_simple?.base ?? {};
  const pe = flujo500?.punto_equilibrio ?? {};
  const metrics = [
    { label: 'Galpón + pollonas', value: formatCurrency(capexTotal500?.capex_conocido?.subtotal_conocido_clp ?? 9771765), detail: 'CAPEX conocido' },
    { label: 'CAPEX total base', value: formatCurrency(capexBase.capex_total_referencial_clp ?? 13343765), detail: 'galpón + pollonas + equipamiento base', tone: 'risk' },
    { label: 'Capital trabajo mínimo', value: formatCurrency(decisionP47?.capital_trabajo?.minimo_1_mes_clp ?? 1686750), detail: '1 mes OPEX con mano de obra' },
    { label: 'Déficit base con CT', value: formatCurrency(Math.abs(fullMoney.deficit_base_con_1_mes_ct_vs_10m_clp ?? -5030515)), detail: 'contra $10.000.000 disponibles', tone: 'risk' },
    { label: 'OPEX con mano obra', value: formatCurrency(opex500?.subtotal_con_mano_obra_clp_mes ?? 1686750), detail: '$600.000 mano de obra incluida' },
    { label: 'Margen mensual con MO', value: formatCurrency(flujo500?.margenes?.con_mano_obra_clp_mes ?? 959617), detail: 'preliminar 100 bandejas/semana', tone: 'accent' },
    { label: 'Punto equilibrio con MO', value: `${pe.con_mano_obra_bandejas_semana ?? 63.7} bandejas/sem`, detail: `${pe.con_mano_obra_bandejas_mes ?? 276.2} bandejas/mes` },
    { label: 'Payback base', value: `${paybackBase.payback_simple_sin_mano_obra_meses ?? 8.56} / ${paybackBase.payback_simple_con_mano_obra_meses ?? 13.91} meses`, detail: 'sin MO / con MO' }
  ];
  renderMetrics('resumen-financiero-metricas', metrics);
}

function renderEscenarioProporcional({ escenarioProporcional, requerimientosEquipamiento }) {
  const escenario = escenarioProporcional ?? {};
  const alimento = escenario.alimento ?? {};
  const envases = escenario.envases_meta ?? {};
  const viruta = escenario.viruta ?? {};
  const agua = escenario.agua ?? {};
  const densidad = escenario.densidad ?? {};
  const opex = escenario.opex_minimo_proporcional ?? {};
  const req = requerimientosEquipamiento?.resumen ?? {};

  const metrics = [
    { label: 'Densidad', value: formatValue(densidad.aves_m2 ?? 6.94, 'aves/m²'), detail: densidad.mostrar ?? 'aprox. 7 aves/m²', tone: 'accent' },
    { label: 'Alimento proyectado', value: formatValue(alimento.proyeccion_sacos_mes_redondeada ?? 75, 'sacos/mes'), detail: `${alimento.proyeccion_kg_mes ?? 1860} kg/mes` },
    { label: 'Costo alimento proyectado', value: formatCurrency(alimento.costo_proyectado_clp_mes ?? 971250), detail: '75 sacos x $12.950', tone: 'pending' },
    { label: 'Envases meta', value: formatCurrency(envases.costo_mensual_clp ?? 45500), detail: '100 bandejas/semana x $105' },
    { label: 'Viruta proyectada', value: formatCurrency(viruta.proyeccion_redondeada_clp_mes ?? 34000), detail: 'proporcional desde $10.000/mes' },
    { label: 'Agua estimada', value: agua.rango_litros_dia ?? '115 a 154 L/día', detail: 'validar estanque y bomba', tone: 'pending' },
    { label: 'OPEX mínimo proporcional', value: formatCurrency(opex.total_clp_mes ?? 1060750), detail: 'parcial · no OPEX total', tone: 'risk' },
    { label: 'Comederos', value: req.comederos ?? '40-50 m lineales o 22-24 unidades', detail: 'según producto a cotizar' },
    { label: 'Bebederos', value: req.bebederos ?? '60 nipples aprox.', detail: 'o sistema equivalente' },
    { label: 'Nidos', value: req.nidos ?? '72 individuales o 5 m² comunitario', detail: 'dos alternativas para cotizar' },
    { label: 'Perchas', value: req.perchas ?? '75 m lineales', detail: 'ajustable según diseño final' },
    { label: 'Bodega alimento', value: req.bodega_alimento ?? '19 sacos/semana o 38 sacos/2 semanas', detail: 'capacidad mínima recomendada' }
  ];

  renderMetrics('escenario-proporcional-metricas', metrics);
}

function renderCapexP45P46({ capexTotal500, capexEquipamiento }) {
  const totals = capexTotal500?.capex_total_referencial ?? {};
  const equipment = capexTotal500?.equipamiento_escenarios ?? capexEquipamiento?.escenarios ?? {};
  const known = capexTotal500?.capex_conocido ?? {};
  const metrics = [
    { label: 'Conocido galpón + pollonas', value: formatCurrency(known.subtotal_conocido_clp ?? 9771765), detail: 'ya consume casi todo el máximo propio', tone: 'risk' },
    { label: 'Equipamiento bajo', value: formatCurrency(equipment.bajo?.total_clp), detail: equipment.bajo?.descripcion ?? 'mínimo funcional' },
    { label: 'Equipamiento base', value: formatCurrency(equipment.base?.total_clp), detail: equipment.base?.descripcion ?? 'prudente realista', tone: 'pending' },
    { label: 'Equipamiento alto', value: formatCurrency(equipment.alto?.total_clp), detail: equipment.alto?.descripcion ?? 'mayor holgura' },
    { label: 'Total bajo', value: formatCurrency(totals.bajo?.capex_total_referencial_clp), detail: `déficit vs $10M: ${formatCurrency(Math.abs(totals.bajo?.deficit_o_excedente_clp ?? 0))}`, tone: 'risk' },
    { label: 'Total base', value: formatCurrency(totals.base?.capex_total_referencial_clp), detail: `déficit vs $10M: ${formatCurrency(Math.abs(totals.base?.deficit_o_excedente_clp ?? 0))}`, tone: 'risk' },
    { label: 'Total alto', value: formatCurrency(totals.alto?.capex_total_referencial_clp), detail: `déficit vs $10M: ${formatCurrency(Math.abs(totals.alto?.deficit_o_excedente_clp ?? 0))}`, tone: 'risk' },
    { label: 'Capital trabajo mínimo', value: formatCurrency(capexTotal500?.capital_trabajo_inicial?.un_mes_opex_con_mano_obra_clp), detail: '1 mes OPEX con mano de obra · separado de CAPEX', tone: 'pending' }
  ];
  renderMetrics('capex-referencial-metricas', metrics);
  renderCompactRows('capex-equipamiento-detalle', Object.entries(equipment).map(([key, value]) => ({
    kicker: `Escenario ${key}`,
    title: `CAPEX equipamiento ${key}`,
    value: formatCurrency(value?.total_clp),
    detail: Object.entries(value?.items ?? {}).map(([item, data]) => `${item.replaceAll('_', ' ')}: ${formatCurrency(data.subtotal_clp)}`).join(' · '),
    small: key === 'base' ? 'Escenario recomendado para lectura financiera preliminar.' : 'Referencial; requiere cotización final.'
  })));
}

function renderOpexP45P46({ opex500 }) {
  const imp = opex500?.imprevistos_operativos ?? {};
  const metrics = [
    { label: 'OPEX sin mano de obra', value: formatCurrency(opex500?.subtotal_sin_mano_obra_clp_mes), detail: 'alimento + envases + viruta + reparto + vitaminas + agua' },
    { label: 'Mano de obra económica', value: formatCurrency(opex500?.mano_obra_economica?.subtotal_clp_mes), detail: '$20.000 diarios x 30' },
    { label: 'OPEX con mano de obra', value: formatCurrency(opex500?.subtotal_con_mano_obra_clp_mes), detail: 'base para capital de trabajo', tone: 'pending' },
    { label: 'Imprevistos 5%', value: formatCurrency(imp.cinco_por_ciento_sobre_opex_sin_mano_obra_clp), detail: `total con MO + 5%: ${formatCurrency(imp.total_con_mano_obra_mas_5_clp)}` },
    { label: 'Imprevistos 10%', value: formatCurrency(imp.diez_por_ciento_sobre_opex_sin_mano_obra_clp), detail: `total con MO + 10%: ${formatCurrency(imp.total_con_mano_obra_mas_10_clp)}` }
  ];
  renderMetrics('opex-proyectado-metricas', metrics);
}

function renderIngresosP45P46({ ingresos500 }) {
  const sens = ingresos500?.sensibilidades ?? {};
  const metrics = [
    { label: 'Precio promedio', value: formatCurrency(ingresos500?.precio_promedio_actual_clp_bandeja ?? 6107), detail: 'mix actual segunda/primera/extra' },
    { label: 'Base 100 bandejas', value: formatCurrency(sens.base?.ingreso_mensual_clp), detail: `${formatCurrency(sens.base?.ingreso_semanal_clp)}/semana`, tone: 'accent' },
    { label: 'Conservador 90', value: formatCurrency(sens.conservador_90?.ingreso_mensual_clp), detail: 'misma mezcla de precios' },
    { label: 'Descuento almacenes', value: formatCurrency(sens.descuento_almacenes?.ingreso_mensual_clp), detail: '10% solo sobre 30 bandejas/semana' },
    { label: 'Alto 104,1', value: formatCurrency(sens.alto_104_1?.ingreso_mensual_clp), detail: 'vende toda la producción técnica estimada' }
  ];
  renderMetrics('ingresos-proyectados-metricas', metrics);
}

function renderFlujoP45P46({ flujo500 }) {
  const margins = flujo500?.margenes ?? {};
  const pe = flujo500?.punto_equilibrio ?? {};
  const payback = flujo500?.payback_simple ?? {};
  const metrics = [
    { label: 'Margen sin mano obra', value: formatCurrency(margins.sin_mano_obra_clp_mes), detail: 'ingreso mensual base - OPEX sin MO', tone: 'accent' },
    { label: 'Margen con mano obra', value: formatCurrency(margins.con_mano_obra_clp_mes), detail: 'ingreso mensual base - OPEX con MO', tone: 'pending' },
    { label: 'Equilibrio sin MO', value: `${pe.sin_mano_obra_bandejas_semana ?? '—'} bandejas/sem`, detail: `${pe.sin_mano_obra_bandejas_mes ?? '—'} bandejas/mes` },
    { label: 'Equilibrio con MO', value: `${pe.con_mano_obra_bandejas_semana ?? '—'} bandejas/sem`, detail: `${pe.con_mano_obra_bandejas_mes ?? '—'} bandejas/mes`, tone: 'pending' }
  ];
  renderMetrics('flujo-preliminar-metricas', metrics);
  renderCompactRows('flujo-payback-detalle', Object.entries(payback).map(([key, value]) => ({
    kicker: `CAPEX ${key}`,
    title: `Payback simple ${key}`,
    value: `${value.payback_simple_sin_mano_obra_meses} / ${value.payback_simple_con_mano_obra_meses} meses`,
    detail: 'sin mano de obra / con mano de obra económica',
    small: `CAPEX: ${formatCurrency(value.capex_total_referencial_clp)}`
  })));
}

function renderEstrategiaPollonas({ estrategiaPollonas }) {
  const estrategias = estrategiaPollonas?.estrategias ?? {};
  const rows = Object.entries(estrategias).map(([key, value]) => ({
    kicker: value.semaforo ?? 'estrategia',
    title: key.replaceAll('_', ' '),
    value: formatCurrency(value.capex_pollonas_clp),
    detail: value.lectura,
    small: `${value.pollonas} pollonas x ${formatCurrency(estrategiaPollonas?.precio_pollona_clp ?? 12000)}`
  }));
  renderCompactRows('estrategia-pollonas-detalle', rows);
  setText('estrategia-pollonas-recomendacion', estrategiaPollonas?.recomendacion_preliminar ?? 'Compra por etapas reduce riesgo financiero; comprar todas solo con financiamiento y venta confirmada.');
}

function renderDecisionP47({ decisionP47, alternativasP47, planP47 }) {
  const decision = decisionP47 ?? {};
  const alternatives = alternativasP47?.alternativas ?? [];
  const capital = decision.capital_trabajo ?? {};

  setText('p47-recomendacion-principal', decision.recomendacion_ejecutiva ?? 'Mantener AMARILLO y avanzar solo por etapas.');
  setText('p47-alternativa-recomendada', decision.respuestas_clave?.etapa_inicial_mas_prudente ?? '+150 pollonas como base prudente.');

  renderMetrics('p47-decision-metricas', [
    { label: 'Estado P47', value: decision.estado_general ?? 'AMARILLO', detail: 'no aprueba inversión', tone: 'risk' },
    { label: 'Alternativa base prudente', value: '+150 pollonas', detail: 'AMARILLO MEDIO' },
    { label: 'Alternativa conservadora', value: '+100 pollonas', detail: 'AMARILLO BAJO' },
    { label: 'Escala completa', value: '+352 pollonas', detail: 'AMARILLO ALTO · solo con financiamiento cerrado', tone: 'risk' },
    { label: 'Capital trabajo mínimo', value: formatCurrency(capital.minimo_1_mes_clp), detail: '1 mes OPEX con mano de obra' },
    { label: 'Capital trabajo prudente', value: formatCurrency(capital.prudente_2_meses_clp), detail: '2 meses OPEX con mano de obra' }
  ]);

  renderCompactRows('p47-alternativas-detalle', alternatives.map((alt) => {
    const partial = alt.lectura_parcial_infraestructura_actual ?? {};
    const full = alt.lectura_con_galpon_completo_desde_inicio ?? {};
    const primaryRequirement = partial.aplica ? partial.requerimiento_total_inicial_clp : full.requerimiento_total_inicial_1_mes_ct_clp;
    const primaryDelta = partial.aplica ? partial.deficit_o_excedente_vs_10m_clp : full.deficit_o_excedente_vs_10m_1_mes_ct_clp;
    const deltaLabel = Number(primaryDelta) >= 0 ? 'excedente' : 'déficit';
    return {
      kicker: alt.semaforo,
      title: `${alt.pollonas_a_comprar} pollonas · ${alt.plantel_total_aves} aves`,
      value: formatCurrency(primaryRequirement),
      detail: `${alt.bandejas_semana_estimadas} bandejas/sem · ingreso ${formatCurrency(alt.ingreso_mensual_estimado_clp)} · margen c/MO ${formatCurrency(alt.margen_mensual_con_mano_obra_clp)}`,
      small: `${deltaLabel} vs $10M: ${formatCurrency(Math.abs(primaryDelta ?? 0))}. Condición: ${alt.condicion_para_ejecutar}`,
      tone: alt.semaforo?.includes('ALTO') ? 'risk' : 'pending'
    };
  }));

  renderCompactRows('p47-plan-6m', (planP47?.fases ?? []).map((phase) => ({
    kicker: phase.periodo,
    title: `${phase.fase} · ${phase.nombre}`,
    value: `${(phase.acciones ?? []).length} acciones`,
    detail: (phase.acciones ?? []).join(' · '),
    small: 'Plan por etapas; no habilita inversión por sí solo.'
  })));
}

function renderCriticalBlockers() {
  const groups = [
    {
      title: 'Comerciales',
      status: 'pendiente',
      items: ['Documentar compradores por canal', 'Confirmar venta mínima de 63,7 bandejas/semana con mano de obra', 'Validar estabilidad de 100 bandejas/semana al contado']
    },
    {
      title: 'Financieros',
      status: 'pendiente',
      items: ['Cotizaciones finales de equipamiento, agua y energía', 'Cubrir déficit base con 1 mes CT: $5.030.515', 'Cubrir capital de trabajo mínimo: $1.686.750']
    },
    {
      title: 'Operativos / legales',
      status: 'pendiente',
      items: ['Validar infraestructura actual para +100/+150', 'Cerrar permisos/formalización sanitaria y tributaria', 'Definir logística de invierno y calendario real']
    }
  ];
  const container = $('bloqueos-criticos-grupos');
  if (!container) return;
  container.innerHTML = '';
  groups.forEach((group) => {
    const card = document.createElement('article');
    card.className = 'critical-card';
    card.innerHTML = `
      <div class="critical-head">
        <span>${group.status}</span>
        <strong>${group.title}</strong>
      </div>
      <ul>${group.items.map((item) => `<li>${item}</li>`).join('')}</ul>
    `;
    container.appendChild(card);
  });
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

  const extendedOnly = indicators.filter((indicator) => {
    const name = String(indicator?.nombre ?? indicator?.indicador ?? '').toLowerCase();
    return ['roi', 'van', 'tir', 'ebitda'].some((token) => name.includes(token));
  });

  extendedOnly.forEach((indicator) => {
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

function renderAlerts(alertas) {
  const container = $('alertas-p0');
  if (!container) return;
  container.innerHTML = '';

  const items = (alertas?.alertas ?? []).filter((alert) => ['A12', 'A13', 'A15', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27'].includes(alert.id));
  items.forEach((alert) => {
    const card = document.createElement('article');
    card.className = `alert-card severity-${normalizeStatus(alert.severidad)}`;
    card.innerHTML = `
      <div class="alert-card-head">
        <span>${alert.id} · ${alert.dimension}</span>
        <strong>${alert.titulo}</strong>
      </div>
      <p>${alert.descripcion}</p>
      <small>Estado: ${alert.estado}</small>
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
  const orderedKeys = ['productiva', 'comercial', 'financiera', 'logistica', 'sanitaria', 'agua', 'energia', 'legal', 'contable'];

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
    productiva: 'Productivo',
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
  renderResumenFinancieroEjecutivo(data);
  renderEscenarioProporcional(data);
  renderCapexP45P46(data);
  renderOpexP45P46(data);
  renderIngresosP45P46(data);
  renderFlujoP45P46(data);
  renderEstrategiaPollonas(data);
  renderDecisionP47(data);
  renderCriticalBlockers(data);
  renderEscalas(data.galpones);
  renderFinancialIndicators(data);
  renderAlerts(data.alertas);
  renderWorkstreams(data);
  renderMarketReferences(data.referenciasMercado);
  renderSemaforo();
  renderBlockers();
  renderActionLists();
  renderRisks(data.semaforo);
  renderConclusion(data.resumen, data.semaforo);
}

document.addEventListener('DOMContentLoaded', init);

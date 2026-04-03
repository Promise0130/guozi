/**
 * 地方国资信息采集与分析 — 数据加载与渲染核心
 *
 * 数据接口约定:
 *   data/entity_list.csv      → 模块A: 21字段, entity_id 主键
 *   data/monthly_operation.csv → 模块B: 28字段, record_id 主键
 *   data/policy_briefing.csv   → 模块C: 15字段, id 主键
 *   data/budget_rules.csv      → 模块D: 21字段, record_id 主键
 *   data/budget_transfer.csv   → 模块D: 3字段, province 主键
 *
 * 字段映射关系 (底表→页面):
 *   A: entity_name_full→企业名称, province→省份, list_caliber→口径
 *   B: indicator_name→指标, value→数值, yoy_pct→同比
 *   C: title→政策名称, doc_type→文种, level→层级
 *   D: ratio_value→比例, budget_income→收入, scope_label→范围
 */
'use strict';

const APP_VERSION = '20260403-2';

/* ========== CSV Parser ========== */
function parseCSV(text) {
  const lines = text.trim().split('\n');
  if (lines.length < 2) return [];
  const headers = parseCSVLine(lines[0]);
  const rows = [];
  for (let i = 1; i < lines.length; i++) {
    const vals = parseCSVLine(lines[i]);
    if (vals.length === 0) continue;
    const obj = {};
    headers.forEach((h, idx) => { obj[h.trim()] = (vals[idx] || '').trim(); });
    rows.push(obj);
  }
  return rows;
}

function parseCSVLine(line) {
  const result = [];
  let current = '';
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (inQuotes) {
      if (ch === '"' && line[i + 1] === '"') { current += '"'; i++; }
      else if (ch === '"') { inQuotes = false; }
      else { current += ch; }
    } else {
      if (ch === '"') { inQuotes = true; }
      else if (ch === ',') { result.push(current); current = ''; }
      else { current += ch; }
    }
  }
  result.push(current);
  return result;
}

/* ========== Data Loader ========== */
async function loadCSV(path) {
  const embeddedText = getEmbeddedCSVText(path);
  if (window.location.protocol === 'file:' && embeddedText) {
    return parseCSV(embeddedText);
  }

  const resolvedPath = withCacheBuster(resolveDataPath(path));
  try {
    const resp = await fetch(resolvedPath, {
      cache: 'no-store',
      headers: {
        'Cache-Control': 'no-cache'
      }
    });
    if (!resp.ok) throw new Error(`Failed to load ${resolvedPath}: ${resp.status}`);
    const text = await resp.text();
    return parseCSV(text);
  } catch (error) {
    if (embeddedText) {
      return parseCSV(embeddedText);
    }
    throw error;
  }
}

function resolveDataPath(path) {
  if (/^(?:[a-z]+:)?\/\//i.test(path) || path.startsWith('/')) return path;
  const currentPath = window.location.pathname.replace(/\\/g, '/');
  if (currentPath.includes('/pages/')) return `../${path}`;
  return path;
}

function withCacheBuster(path) {
  const sep = path.includes('?') ? '&' : '?';
  return `${path}${sep}v=${APP_VERSION}`;
}

function getEmbeddedCSVText(path) {
  const embedded = window.EMBEDDED_CSV_DATA || {};
  return embedded[path] || null;
}

const DataStore = {
  entities: null,
  monthly: null,
  policies: null,
  budgetRules: null,
  budgetTransfer: null,

  async loadAll() {
    const [e, m, p, b, t] = await Promise.all([
      loadCSV('data/entity_list.csv'),
      loadCSV('data/monthly_operation.csv'),
      loadCSV('data/policy_briefing.csv'),
      loadCSV('data/budget_rules.csv'),
      loadCSV('data/budget_transfer.csv'),
    ]);
    this.entities = e;
    this.monthly = m;
    this.policies = p;
    this.budgetRules = b;
    this.budgetTransfer = t;
    return this;
  }
};

/* ========== Evidence Helper ========== */
/**
 * 生成证据回链HTML
 * @param {object} row - 数据行 (含 source_url, evidence_strength|uev_level, source_doc|source_title|source_institution)
 * @returns {string} HTML
 *
 * 证据回链机制:
 *   底表字段 → 回链字段映射:
 *     模块A: source_url + uev_level + source_institution
 *     模块B: source_url + uev_level + source_title + source_institution
 *     模块C: evidence_url + evidence_strength + issuer
 *     模块D: source_url + evidence_strength + source_doc
 */
function evidenceBadge(strength) {
  const s = String(strength || '').replace(/[^1-4sS]/g, '');
  const level = s.match(/[1-4]/)?.[0] || '4';
  const labels = { '1': 'S1 官方全文', '2': 'S2 官方解读', '3': 'S3 部分确认', '4': 'S4 未识别' };
  return `<span class="ev-badge s${level}">${labels[level]}</span>`;
}

function evidenceLink(row) {
  const url = row.source_url || row.evidence_url || '';
  const doc = row.source_doc || row.source_title || row.title || '';
  const inst = row.source_institution || row.issuer || '';
  const strength = row.evidence_strength || row.uev_level || '';
  const date = row.source_date || row.publish_date || row.extraction_date || '';
  if (!url) return '<span class="text-muted">—</span>';
  // Sanitize URL to prevent XSS - only allow http(s) protocols
  let safeUrl = '';
  try {
    const parsed = new URL(url);
    if (parsed.protocol === 'http:' || parsed.protocol === 'https:') {
      safeUrl = parsed.href;
    }
  } catch (e) {
    safeUrl = '';
  }
  const linkHtml = safeUrl
    ? `<a href="${escapeHtml(safeUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(doc || '查看来源')}</a>`
    : `<span>${escapeHtml(doc || '—')}</span>`;
  return `
    <div class="evidence-panel">
      <dl>
        <dt>来源机构</dt><dd>${escapeHtml(inst)}</dd>
        <dt>来源文件</dt><dd>${linkHtml}</dd>
        <dt>证据等级</dt><dd>${evidenceBadge(strength)}</dd>
        <dt>日期</dt><dd>${escapeHtml(date)}</dd>
      </dl>
    </div>`;
}

/* ========== Rendering Helpers ========== */
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function fmtNum(v, unit) {
  if (!v || v === 'UNIDENTIFIED') return '<span style="color:var(--evidence-s4)">未识别</span>';
  const n = parseFloat(v);
  if (isNaN(n)) return escapeHtml(v);
  if (unit === '%' || unit === '百分点') return n.toFixed(1) + unit;
  if (Math.abs(n) >= 10000) return (n / 10000).toFixed(2) + '万亿元';
  return n.toLocaleString('zh-CN', { maximumFractionDigits: 2 }) + (unit === '100M_CNY' ? '亿元' : (unit || ''));
}

function yoyTag(val) {
  if (!val) return '';
  const s = String(val);
  const isDown = s.startsWith('-') || s.includes('下降');
  return `<span class="kpi-yoy ${isDown ? 'down' : 'up'}">${escapeHtml(s)}</span>`;
}

/* ========== Page-Specific Renderers ========== */

/** Page 1: 国资企业主体 — Maps to Module A entity_list.csv */
function renderEntityPage(entities) {
  const container = document.getElementById('entity-content');
  if (!container) return;

  // KPI
  const provinces = [...new Set(entities.map(e => e.province))];
  const supervised = entities.filter(e => e.list_caliber === 'supervised');
  document.getElementById('kpi-total').textContent = entities.length;
  document.getElementById('kpi-provinces').textContent = provinces.length;
  document.getElementById('kpi-supervised').textContent = supervised.length;
  document.getElementById('kpi-avg-conf').textContent =
    (entities.reduce((s, e) => s + parseFloat(e.confidence || 0), 0) / entities.length).toFixed(2);

  // Table — field mapping: entity_name_full, province, admin_level, list_caliber, sector, confidence, uev_level, source_url
  let html = `<table class="data-table"><thead><tr>
    <th>企业名称</th><th>省份</th><th>层级</th><th>口径</th>
    <th>行业</th><th>置信度</th><th>证据</th><th>来源</th>
  </tr></thead><tbody>`;
  entities.forEach(e => {
    html += `<tr>
      <td>${escapeHtml(e.entity_name_full)}</td>
      <td>${escapeHtml(e.province)}</td>
      <td>${escapeHtml(e.admin_level)}</td>
      <td>${escapeHtml(e.list_caliber_label || e.list_caliber)}</td>
      <td>${escapeHtml(e.sector || '—')}</td>
      <td class="num">${parseFloat(e.confidence || 0).toFixed(2)}</td>
      <td>${evidenceBadge(e.uev_level)}</td>
      <td><a class="evidence-link" onclick="toggleEvidence(this, ${JSON.stringify(JSON.stringify(e)).slice(1,-1)})">详情</a></td>
    </tr>`;
  });
  html += '</tbody></table>';
  container.innerHTML = html;
}

/** Page 2: 企业经营数据分析 — Maps to Module B monthly_operation.csv */
function renderMonthlyPage(monthly, allMonthly = monthly) {
  const container = document.getElementById('monthly-content');
  if (!container) return;

  // KPI from latest national cumulative
  const national2026 = allMonthly.filter(r => r.province_code === 'CN' && r.year === '2026' && r.period_type === 'cumulative');
  const rev = national2026.find(r => r.indicator_name === '营业总收入');
  const profit = national2026.find(r => r.indicator_name === '利润总额');
  const tax = national2026.find(r => r.indicator_name === '应交税费');
  const dar = allMonthly.find(r => r.province_code === 'CN' && r.year === '2026' && r.indicator_name === '资产负债率');

  if (rev) { document.getElementById('kpi-rev').textContent = fmtNum(rev.value, '亿元'); document.getElementById('kpi-rev-yoy').innerHTML = yoyTag(rev.yoy_pct + '%'); }
  if (profit) { document.getElementById('kpi-profit').textContent = fmtNum(profit.value, '亿元'); document.getElementById('kpi-profit-yoy').innerHTML = yoyTag(profit.yoy_pct + '%'); }
  if (tax) { document.getElementById('kpi-tax').textContent = fmtNum(tax.value, '亿元'); document.getElementById('kpi-tax-yoy').innerHTML = yoyTag(tax.yoy_pct + '%'); }
  if (dar) { document.getElementById('kpi-dar').textContent = dar.value + '%'; document.getElementById('kpi-dar-yoy').innerHTML = yoyTag(dar.yoy_pct + '个百分点'); }

  // Table — field mapping: period_label, province, scope, indicator_name, value, unit, yoy_pct, source_url
  let html = `<table class="data-table"><thead><tr>
    <th>期间</th><th>省份</th><th>口径</th><th>指标</th>
    <th>数值</th><th>同比</th><th>证据</th><th>来源</th>
  </tr></thead><tbody>`;
  monthly.forEach(r => {
    html += `<tr>
      <td>${escapeHtml(r.year + '年' + r.period_label)}</td>
      <td>${escapeHtml(r.province)}</td>
      <td>${escapeHtml(r.scope)}</td>
      <td>${escapeHtml(r.indicator_name)}</td>
      <td class="num">${fmtNum(r.value, r.unit)}</td>
      <td class="num">${r.yoy_pct ? r.yoy_pct + '%' : '—'}</td>
      <td>${evidenceBadge(r.uev_level)}</td>
      <td><a class="evidence-link" onclick="toggleEvidence(this, ${JSON.stringify(JSON.stringify(r)).slice(1,-1)})">详情</a></td>
    </tr>`;
  });
  html += '</tbody></table>';
  container.innerHTML = html;

  // Chart: latest provincial profit ranking, excluding national/central rollups.
  renderProvinceProfitChart('chart-rev-profit', getLatestProvinceProfitRows(allMonthly));
}

/** Page 3: 收益管理规则动态 — Maps to Module C policy_briefing.csv + Module D budget_rules (RULE type) */
function renderPolicyPage(policies, budgetRules) {
  const container = document.getElementById('policy-content');
  if (!container) return;

  // Policy table — field mapping: title, issuer, doc_date, doc_type, level, topic_primary, evidence_url, evidence_strength
  let html = '<h3>政策文件</h3>';
  html += `<table class="data-table"><thead><tr>
    <th>政策名称</th><th>发文机构</th><th>日期</th><th>文种</th>
    <th>层级</th><th>主题</th><th>证据</th><th>来源</th>
  </tr></thead><tbody>`;
  policies.forEach(p => {
    html += `<tr>
      <td>${escapeHtml(p.title)}</td>
      <td>${escapeHtml(p.issuer)}</td>
      <td>${escapeHtml(p.doc_date)}</td>
      <td>${escapeHtml(p.doc_type)}</td>
      <td>${escapeHtml(p.level)}</td>
      <td>${escapeHtml(p.topic_primary)}</td>
      <td>${evidenceBadge(p.evidence_strength)}</td>
      <td><a class="evidence-link" onclick="toggleEvidence(this, ${JSON.stringify(JSON.stringify(p)).slice(1,-1)})">详情</a></td>
    </tr>`;
  });
  html += '</tbody></table>';

  // Budget RULE records — field mapping: rule_description_zh, ratio_value, ratio_type, scope_label, source_url, evidence_strength
  const rules = budgetRules.filter(r => r.record_type === 'RULE');
  html += '<h3 style="margin-top:24px">收益收取比例规则</h3>';
  html += `<table class="data-table"><thead><tr>
    <th>规则说明</th><th>比例</th><th>类型</th><th>范围</th>
    <th>年度</th><th>证据</th><th>来源</th>
  </tr></thead><tbody>`;
  rules.forEach(r => {
    html += `<tr>
      <td>${escapeHtml(r.rule_description_zh)}</td>
      <td class="num">${r.ratio_value === 'UNIDENTIFIED' ? '<span style="color:var(--evidence-s4)">未识别</span>' : escapeHtml(r.ratio_value)}</td>
      <td>${escapeHtml(r.ratio_type)}</td>
      <td>${escapeHtml(r.scope_label)}</td>
      <td>${escapeHtml(r.effective_year)}</td>
      <td>${evidenceBadge(r.evidence_strength)}</td>
      <td><a class="evidence-link" onclick="toggleEvidence(this, ${JSON.stringify(JSON.stringify(r)).slice(1,-1)})">详情</a></td>
    </tr>`;
  });
  html += '</tbody></table>';
  container.innerHTML = html;
}

/** Page 4: 财政统筹结果 — Maps to Module D budget_rules (BUDGET_FIGURE + TRANSFER) + budget_transfer.csv */
function renderBudgetPage(budgetRules, budgetTransfer) {
  const container = document.getElementById('budget-content');
  if (!container) return;

  const figures = budgetRules.filter(r => r.record_type === 'BUDGET_FIGURE');
  const transfers = budgetRules.filter(r => r.record_type === 'TRANSFER');

  // KPI
  const centralIncome = figures.find(r => r.scope === 'central' && r.budget_income);
  const localIncome = figures.find(r => r.scope === 'local' && r.budget_income);
  const nationalIncome = figures.find(r => r.scope === 'national' && r.budget_income);
  const transferGPB = budgetRules.find(r => r.rule_name === 'central_transfer_to_gpb');

  if (centralIncome) document.getElementById('kpi-central-inc').textContent = fmtNum(centralIncome.budget_income, '100M_CNY');
  if (localIncome) document.getElementById('kpi-local-inc').textContent = fmtNum(localIncome.budget_income, '100M_CNY');
  if (nationalIncome) document.getElementById('kpi-national-inc').textContent = fmtNum(nationalIncome.budget_income, '100M_CNY');
  if (transferGPB) document.getElementById('kpi-gpb-transfer').textContent = fmtNum(transferGPB.budget_transfer_to_gpb, '100M_CNY');

  // Budget figures table — field mapping: record_id, scope_label, budget_income, budget_expenditure, budget_transfer_to_gpb, yoy, evidence_strength, source_url
  let html = '<h3>预算收支概览</h3>';
  html += `<table class="data-table"><thead><tr>
    <th>范围</th><th>收入(亿元)</th><th>支出(亿元)</th><th>调入一般公共预算(亿元)</th>
    <th>同比</th><th>证据</th><th>来源</th>
  </tr></thead><tbody>`;
  figures.forEach(f => {
    html += `<tr>
      <td>${escapeHtml(f.scope_label)}</td>
      <td class="num">${fmtNum(f.budget_income, '100M_CNY')}</td>
      <td class="num">${fmtNum(f.budget_expenditure, '100M_CNY')}</td>
      <td class="num">${fmtNum(f.budget_transfer_to_gpb, '100M_CNY')}</td>
      <td class="num">${yoyTag(f.yoy)}</td>
      <td>${evidenceBadge(f.evidence_strength)}</td>
      <td><a class="evidence-link" onclick="toggleEvidence(this, ${JSON.stringify(JSON.stringify(f)).slice(1,-1)})">详情</a></td>
    </tr>`;
  });
  html += '</tbody></table>';

  // Transfer table — field mapping from budget_transfer.csv: province, 2025_execution_100M_CNY, 2026_budget_100M_CNY
  html += '<h3 style="margin-top:24px">中央对地方转移支付（分省）</h3>';
  html += `<table class="data-table"><thead><tr>
    <th>省份</th><th>2025执行数(亿元)</th><th>2026预算数(亿元)</th>
  </tr></thead><tbody>`;
  // Sort by 2026 budget descending
  const sorted = [...budgetTransfer].sort((a, b) =>
    parseFloat(b['2026_budget_100M_CNY'] || 0) - parseFloat(a['2026_budget_100M_CNY'] || 0));
  sorted.forEach(t => {
    html += `<tr>
      <td>${escapeHtml(t.province)}</td>
      <td class="num">${fmtNum(t['2025_execution_100M_CNY'], '100M_CNY')}</td>
      <td class="num">${fmtNum(t['2026_budget_100M_CNY'], '100M_CNY')}</td>
    </tr>`;
  });
  html += '</tbody></table>';
  container.innerHTML = html;

  renderTransferChart('chart-transfer', sorted.slice(0, 10));
}

/* ========== Charts (lightweight canvas) ========== */
function getLatestProvinceProfitRows(monthly) {
  const rows = monthly.filter(r =>
    r.province_code &&
    r.province_code !== 'CN' &&
    r.indicator_name === '利润总额' &&
    r.value &&
    !isNaN(parseFloat(r.value))
  );
  const periodPriority = {
    annual: 4,
    cumulative: 3,
    quarterly: 2,
    single_month: 1,
  };
  const latestByProvince = new Map();

  rows.forEach(row => {
    const current = latestByProvince.get(row.province_code);
    if (!current) {
      latestByProvince.set(row.province_code, row);
      return;
    }

    const year = parseInt(row.year || '0', 10);
    const currentYear = parseInt(current.year || '0', 10);
    const monthEnd = parseInt(row.month_end || '0', 10);
    const currentMonthEnd = parseInt(current.month_end || '0', 10);
    const priority = periodPriority[row.period_type] || 0;
    const currentPriority = periodPriority[current.period_type] || 0;

    const isNewer =
      year > currentYear ||
      (year === currentYear && monthEnd > currentMonthEnd) ||
      (year === currentYear && monthEnd === currentMonthEnd && priority > currentPriority);

    if (isNewer) latestByProvince.set(row.province_code, row);
  });

  return [...latestByProvince.values()].sort((a, b) => parseFloat(b.value) - parseFloat(a.value));
}

function renderProvinceProfitChart(canvasId, rows) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  canvas.width = canvas.parentElement.clientWidth - 40;
  canvas.height = Math.max(260, rows.length * 30 + 50);
  const W = canvas.width, H = canvas.height;

  ctx.fillStyle = '#ecf0f1';
  ctx.fillRect(0, 0, W, H);

  if (!rows.length) {
    ctx.fillStyle = '#2c3e50';
    ctx.font = '14px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('暂无省级利润总额数据', W / 2, H / 2);
    return;
  }

  const maxVal = Math.max(...rows.map(r => parseFloat(r.value || '0'))) * 1.15;
  const barH = 20;
  const gap = 10;
  const startY = 20;
  const labelW = 72;
  const periodW = 90;

  rows.forEach((row, index) => {
    const y = startY + index * (barH + gap);
    const value = parseFloat(row.value || '0');
    const barWidth = (value / maxVal) * (W - labelW - periodW - 80);

    ctx.fillStyle = '#2980b9';
    ctx.fillRect(labelW + periodW, y, barWidth, barH);

    ctx.fillStyle = '#2c3e50';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText(row.province, labelW - 8, y + 14);
    ctx.textAlign = 'left';
    ctx.fillText(row.year + '年' + row.period_label, labelW, y + 14);
    ctx.fillText(fmtNum(row.value, row.unit).replace(/<[^>]+>/g, ''), labelW + periodW + barWidth + 6, y + 14);
  });
}

function renderTransferChart(canvasId, top10) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  canvas.width = canvas.parentElement.clientWidth - 40;
  canvas.height = 300;
  const W = canvas.width, H = canvas.height;

  const maxVal = Math.max(...top10.map(t => parseFloat(t['2026_budget_100M_CNY'] || 0))) * 1.2;
  const barH = 24, gap = 6, startY = 20, labelW = 100;

  ctx.fillStyle = '#ecf0f1';
  ctx.fillRect(0, 0, W, H);

  top10.forEach((t, i) => {
    const y = startY + i * (barH + gap);
    const v = parseFloat(t['2026_budget_100M_CNY'] || 0);
    const barWidth = (v / maxVal) * (W - labelW - 60);

    ctx.fillStyle = '#2980b9';
    ctx.fillRect(labelW, y, barWidth, barH);

    ctx.fillStyle = '#2c3e50';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText(t.province, labelW - 8, y + barH - 6);
    ctx.textAlign = 'left';
    ctx.fillText(v.toFixed(2) + '亿', labelW + barWidth + 6, y + barH - 6);
  });
}

/* ========== Evidence Toggle ========== */
function toggleEvidence(el, rowJson) {
  const existing = el.parentElement.querySelector('.evidence-panel');
  if (existing) { existing.remove(); return; }
  const row = JSON.parse(rowJson);
  el.parentElement.insertAdjacentHTML('beforeend', evidenceLink(row));
}

/* ========== Global Init ========== */
window.DataStore = DataStore;
window.toggleEvidence = toggleEvidence;

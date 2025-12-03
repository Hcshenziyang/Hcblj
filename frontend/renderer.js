const $ = (id) => document.getElementById(id);

// 全局状态
let cat1 = [];
let cat2 = [];
let tags = [];
let records = [];

function setOptions(selectEl, data, placeholder) {
  if (!selectEl) return;
  selectEl.innerHTML = '';
  if (placeholder !== undefined) {
    const opt = document.createElement('option');
    opt.value = '';
    opt.textContent = placeholder;
    selectEl.appendChild(opt);
  }
  data.forEach((item) => {
    const opt = document.createElement('option');
    opt.value = item.id;
    opt.textContent = item.name;
    selectEl.appendChild(opt);
  });
}

function renderCats() {
  const catList = $('cat-list');
  if (catList) {
    const l1 = cat1.map((c) => `${c.id}.${c.name}`).join('，') || '暂无一级';
    const l2 = cat2.map((c) => `${c.id}.${c.name}(L1:${c.level1_id})`).join('，') || '暂无二级';
    catList.textContent = `一级：${l1} | 二级：${l2}`;
  }

  setOptions(document.querySelector('select[name="category1"]'), cat1, '一级分类');
  setOptions(document.querySelector('select[name="category1_filter"]'), cat1, '一级分类');
  setOptions(document.querySelector('select[name="level1"]'), cat1, '选择一级');
  setOptions(document.querySelector('select[name="category2"]'), cat2, '二级分类');
  setOptions(document.querySelector('select[name="category2_filter"]'), cat2, '二级分类');
}

function renderTags() {
  const tagList = $('tag-list');
  if (tagList) {
    tagList.textContent = tags.length
      ? tags.map((t) => `${t.id}.${t.name}`).join('，')
      : '暂无标签';
  }
}

function renderRecords(list) {
  const container = $('records');
  if (!container) return;
  if (!list.length) {
    container.innerHTML = '<div class="item muted">暂无记录</div>';
    return;
  }
  container.innerHTML = list
    .map((r) => {
      const tagHtml = (r.tags || []).map((t) => `<span class="badge">${t}</span>`).join('');
      return `<div class="item">
        <div>
          <div><strong>¥${r.amount}</strong> · ${new Date(r.happened_at).toLocaleString()}</div>
          <div class="muted">${r.note || ''}</div>
          <div>${tagHtml}</div>
        </div>
        <button class="secondary" data-id="${r.id}">删除</button>
      </div>`;
    })
    .join('');
  container.querySelectorAll('button[data-id]').forEach((btn) => {
    btn.addEventListener('click', async () => {
      try {
        await window.ledgerApi.deleteRecord(btn.dataset.id);
        await loadRecords();
      } catch (e) {
        alert(e.message);
      }
    });
  });
}

function renderReport(report, chart) {
  const reportEl = $('report');
  const chartEl = $('chart');
  if (reportEl) {
    reportEl.innerHTML = `
      <div>月份：${report.month}</div>
      <div>总金额：${report.total}</div>
      <div>按天：${JSON.stringify(report.by_day)}</div>
      <div>按一级分类：${JSON.stringify(report.by_category1)}</div>
      <div>按二级分类：${JSON.stringify(report.by_category2)}</div>
    `;
  }
  if (chartEl) {
    chartEl.textContent = JSON.stringify(chart, null, 2);
  }
}

async function loadCats() {
  try {
    cat1 = await window.ledgerApi.listCat1();
    cat2 = await window.ledgerApi.listCat2();
    renderCats();
  } catch (e) {
    const err = $('cat-error');
    if (err) err.textContent = e.message;
  }
}

async function loadTags() {
  try {
    tags = await window.ledgerApi.listTags();
    renderTags();
  } catch (e) {
    const err = $('tag-error');
    if (err) err.textContent = e.message;
  }
}

async function loadRecords(params = {}) {
  try {
    records = await window.ledgerApi.listRecords(params);
    renderRecords(records);
  } catch (e) {
    const err = $('record-error');
    if (err) err.textContent = e.message;
  }
}

async function loadReport(year, month) {
  try {
    const report = await window.ledgerApi.monthlyReport(year, month);
    const chart = await window.ledgerApi.monthlyChart(year, month);
    renderReport(report, chart);
  } catch (e) {
    const reportEl = $('report');
    if (reportEl) reportEl.textContent = e.message;
  }
}

// 表单：新增记录
document.getElementById('record-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const f = e.target;
  const tagsInput = f.tags.value
    .split(',')
    .map((t) => t.trim())
    .filter(Boolean);
  const payload = {
    amount: parseFloat(f.amount.value),
    currency: f.currency.value || 'CNY',
    category_level1_id: f.category1.value || null,
    category_level2_id: f.category2.value || null,
    tags: tagsInput,
    happened_at: f.happened_at.value ? new Date(f.happened_at.value).toISOString() : new Date().toISOString(),
    note: f.note.value || null,
    is_public: f.is_public.checked,
    in_bill: f.in_bill.checked,
  };
  if (Number.isNaN(payload.amount)) {
    const err = $('record-error');
    if (err) err.textContent = '金额格式不正确';
    return;
  }
  try {
    await window.ledgerApi.createRecord(payload);
    f.reset();
    await loadRecords();
  } catch (err) {
    const msg = $('record-error');
    if (msg) msg.textContent = err.message;
  }
});

// 表单：筛选
document.getElementById('filter-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const f = e.target;
  await loadRecords({
    start: f.start.value,
    end: f.end.value,
    category1: f.category1_filter.value,
    category2: f.category2_filter.value,
    tag: f.tag_filter.value,
    public_only: f.public_only.checked ? true : undefined,
  });
});

// 表单：一级分类
document.getElementById('cat1-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const f = e.target;
  try {
    await window.ledgerApi.createCat1({ name: f.name.value, icon: null });
    f.reset();
    await loadCats();
  } catch (err) {
    const el = $('cat-error');
    if (el) el.textContent = err.message;
  }
});

// 表单：二级分类
document.getElementById('cat2-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const f = e.target;
  if (!f.level1.value) {
    const el = $('cat-error');
    if (el) el.textContent = '请选择一级分类';
    return;
  }
  try {
    await window.ledgerApi.createCat2({ name: f.name.value, level1_id: Number(f.level1.value) });
    f.reset();
    await loadCats();
  } catch (err) {
    const el = $('cat-error');
    if (el) el.textContent = err.message;
  }
});

// 表单：标签
document.getElementById('tag-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const f = e.target;
  try {
    await window.ledgerApi.createTag({ name: f.name.value });
    f.reset();
    await loadTags();
  } catch (err) {
    const el = $('tag-error');
    if (el) el.textContent = err.message;
  }
});

// 表单：月报
document.getElementById('report-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const f = e.target;
  await loadReport(Number(f.year.value), Number(f.month.value));
});

// 初始化
(async () => {
  const now = new Date();
  const reportYear = document.querySelector('#report-form [name="year"]');
  const reportMonth = document.querySelector('#report-form [name="month"]');
  if (reportYear) reportYear.value = now.getFullYear();
  if (reportMonth) reportMonth.value = now.getMonth() + 1;
  const happened = document.querySelector('input[name="happened_at"]');
  if (happened) {
    happened.value = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
      .toISOString()
      .slice(0, 16);
  }

  await loadCats();
  await loadTags();
  await loadRecords();
  await loadReport(now.getFullYear(), now.getMonth() + 1);
})();

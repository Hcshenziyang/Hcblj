const { contextBridge } = require('electron');
const API_BASE = 'http://127.0.0.1:8000';

async function apiFetch(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  if (res.status === 204) return null;
  return res.json();
}

contextBridge.exposeInMainWorld('ledgerApi', {
  // records
  listRecords: (query = {}) => {
    const params = new URLSearchParams();
    Object.entries(query).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') params.append(k, v);
    });
    const qs = params.toString();
    return apiFetch(`/records${qs ? `?${qs}` : ''}`);
  },
  createRecord: (payload) =>
    apiFetch('/records/', { method: 'POST', body: JSON.stringify(payload) }),
  updateRecord: (id, payload) =>
    apiFetch(`/records/${id}`, { method: 'PUT', body: JSON.stringify(payload) }),
  deleteRecord: (id) => apiFetch(`/records/${id}`, { method: 'DELETE' }),
  monthlyReport: (year, month) =>
    apiFetch(`/records/monthly-report?year=${year}&month=${month}`),
  monthlyChart: (year, month) =>
    apiFetch(`/records/monthly-chart?year=${year}&month=${month}`),

  // categories
  listCat1: () => apiFetch('/categories/level1'),
  createCat1: (payload) =>
    apiFetch('/categories/level1', { method: 'POST', body: JSON.stringify(payload) }),
  listCat2: (level1_id) => {
    const qs = level1_id ? `?level1_id=${level1_id}` : '';
    return apiFetch(`/categories/level2${qs}`);
  },
  createCat2: (payload) =>
    apiFetch('/categories/level2', { method: 'POST', body: JSON.stringify(payload) }),

  // tags
  listTags: () => apiFetch('/tags'),
  createTag: (payload) =>
    apiFetch('/tags', { method: 'POST', body: JSON.stringify(payload) }),
});

const API = '';
let currentSOP = null;
let isExistingSOP = false;

const processInput = document.getElementById('process-input');
const generateBtn = document.getElementById('generate-btn');
const sopResult = document.getElementById('sop-result');
const editPanel = document.getElementById('edit-panel');
const loadingOverlay = document.getElementById('loading-overlay');

function showToast(msg) {
  const container = document.getElementById('toast-container');
  const t = document.createElement('div');
  t.className = 'toast'; t.innerText = msg;
  container.appendChild(t);
  setTimeout(() => t.remove(), 3000);
}

function renderSOP(sop) {
  currentSOP = sop;
  ['process_name', 'department', 'objective', 'scope', 'roles', 'prerequisites', 'steps', 'kpis', 'risk_factors', 'tools_required', 'review_frequency'].forEach(key => {
    const el = document.getElementById(key === 'process_name' ? 'res-process-name' : key === 'department' ? 'res-dept' : `res-${key.replace('_', '-')}`);
    if (el) el.textContent = sop[key] || '—';
  });
  sopResult.classList.add('active');
}

async function handleGenerate() {
  const name = processInput.value.trim();
  if (!name) return showToast('Enter process name');
  loadingOverlay.classList.add('active');
  sopResult.classList.remove('active');
  try {
    const res = await fetch(`${API}/generate`, {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({process_name: name})
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Error');
    isExistingSOP = (data.status === 'exact_match');
    showToast(isExistingSOP ? 'Loaded existing SOP' : 'Generated new SOP');
    renderSOP(data.sop);
  } catch (err) {
    showToast(err.message);
  } finally {
    loadingOverlay.classList.remove('active');
  }
}

async function handleSave() {
  if (!currentSOP) return;
  try {
    const res = await fetch(`${API}/sops${isExistingSOP ? '/' + encodeURIComponent(currentSOP.process_name) : ''}`, {
      method: isExistingSOP ? 'PUT' : 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(currentSOP)
    });
    if (!res.ok && res.status !== 409) throw new Error('Save failed');
    isExistingSOP = true;
    showToast('Saved to library!');
  } catch (e) { showToast(e.message); }
}

function handleEdit() {
  if (!currentSOP) return;
  ['process_name', 'department', 'objective', 'scope', 'roles', 'prerequisites', 'steps', 'kpis', 'risk_factors', 'tools_required', 'review_frequency'].forEach(key => {
    const el = document.getElementById(`edit-${key.replace('_', '-')}`);
    if (el) el.value = currentSOP[key] || '';
  });
  editPanel.classList.add('active');
}

async function handleSaveEdits() {
  const updated = {};
  ['process_name', 'department', 'objective', 'scope', 'roles', 'prerequisites', 'steps', 'kpis', 'risk_factors', 'tools_required', 'review_frequency'].forEach(key => {
    updated[key] = document.getElementById(`edit-${key.replace('_', '-')}`).value;
  });
  try {
    const res = await fetch(`${API}/sops${isExistingSOP ? '/' + encodeURIComponent(currentSOP.process_name) : ''}`, {
      method: isExistingSOP ? 'PUT' : 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(updated)
    });
    const saved = await res.json();
    currentSOP = saved; isExistingSOP = true;
    renderSOP(saved);
    editPanel.classList.remove('active');
    showToast('Changes saved!');
  } catch (e) { showToast('Update failed'); }
}

function handleDownload() {
  if (!currentSOP) return;
  const content = Object.entries(currentSOP).map(([k, v]) => `${k.toUpperCase()}\n${v}\n`).join('\n');
  const blob = new Blob([content], {type: 'text/plain'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `SOP_${currentSOP.process_name}.txt`;
  a.click();
}

generateBtn.addEventListener('click', handleGenerate);
document.getElementById('btn-edit').addEventListener('click', handleEdit);
document.getElementById('btn-save').addEventListener('click', handleSave);
document.getElementById('btn-download').addEventListener('click', handleDownload);
document.getElementById('btn-save-edits').addEventListener('click', handleSaveEdits);
document.getElementById('btn-cancel-edit').addEventListener('click', () => editPanel.classList.remove('active'));
document.getElementById('btn-view-library').addEventListener('click', () => window.location.href = '/library');

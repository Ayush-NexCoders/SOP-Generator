const API = '';
let allSOPs = [];

const sopGrid = document.getElementById('sop-grid');
const searchInput = document.getElementById('search-input');
const viewModal = document.getElementById('view-modal');
const modalBody = document.getElementById('modal-sop-body');

function showToast(msg) {
  const container = document.getElementById('toast-container');
  const t = document.createElement('div');
  t.className = 'toast'; t.innerText = msg;
  container.appendChild(t);
  setTimeout(() => t.remove(), 3000);
}

function renderGrid(sops) {
  sopGrid.innerHTML = sops.length ? '' : '<div style="color:white">No SOPs found.</div>';
  sops.forEach(sop => {
    const card = document.createElement('div');
    card.className = 'sop-lib-card';
    card.innerHTML = `
      <div class="lib-card-name">${sop.process_name}</div>
      <div style="color:var(--text-secondary); font-size:0.8rem; margin-top:5px;">${sop.department || 'General'}</div>
      <div class="lib-card-actions">
        <button class="btn btn-secondary btn-sm" onclick="handleView('${sop.process_name}')">View</button>
        <button class="btn btn-danger btn-sm" onclick="handleDelete('${sop.process_name}')">Delete</button>
      </div>`;
    sopGrid.appendChild(card);
  });
}

async function loadSOPs() {
  const res = await fetch(`${API}/sops`);
  const data = await res.json();
  allSOPs = data.sops || [];
  renderGrid(allSOPs);
}

searchInput.addEventListener('input', () => {
  const q = searchInput.value.toLowerCase();
  renderGrid(allSOPs.filter(s => (s.process_name||'').toLowerCase().includes(q)));
});

async function handleView(name) {
  const res = await fetch(`${API}/sops/${encodeURIComponent(name)}`);
  const sop = await res.json();
  modalBody.innerHTML = Object.entries(sop).map(([k,v]) => `<div style="margin-bottom:10px"><strong>${k.toUpperCase()}</strong><br/>${v}</div>`).join('');
  viewModal.classList.add('active');
}

async function handleDelete(name) {
  if (!confirm(`Delete ${name}?`)) return;
  await fetch(`${API}/sops/${encodeURIComponent(name)}`, {method: 'DELETE'});
  showToast('Deleted!');
  loadSOPs();
}

document.getElementById('close-modal').addEventListener('click', () => viewModal.classList.remove('active'));
document.getElementById('close-modal-footer').addEventListener('click', () => viewModal.classList.remove('active'));
document.getElementById('btn-generate-new').addEventListener('click', () => window.location.href = '/');

loadSOPs();

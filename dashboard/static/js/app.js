/**
 * Freelance Dev OS — Frontend App  (Alpine.js v3)
 *
 * Provides all interactive components: toasts, sidebar, charts,
 * WebSocket live updates, theme toggle, search / filter, and modals.
 */

'use strict';

/* ── Alpine Global Store ────────────────────────────────────────────────────── */
document.addEventListener('alpine:init', () => {

  // ── App-level store ──────────────────────────────────────────────────────
  Alpine.store('app', {
    theme:       localStorage.getItem('fdo-theme') || 'dark',
    sidebarOpen: window.innerWidth > 900,
    loading:     false,
    wsConnected: false,

    toggleTheme() {
      this.theme = this.theme === 'dark' ? 'light' : 'dark';
      localStorage.setItem('fdo-theme', this.theme);
      document.documentElement.setAttribute('data-theme', this.theme);
    },

    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen;
    },

    init() {
      document.documentElement.setAttribute('data-theme', this.theme);
      window.addEventListener('resize', () => {
        if (window.innerWidth > 900) this.sidebarOpen = true;
      });
    },
  });

  // ── Toast store ──────────────────────────────────────────────────────────
  Alpine.store('toast', {
    messages: [],
    _nextId: 1,

    show(msg, type = 'info', duration = 4000) {
      const id = this._nextId++;
      const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
      this.messages.push({ id, msg, type, icon: icons[type] || 'ℹ️' });
      if (duration > 0) setTimeout(() => this.remove(id), duration);
      return id;
    },

    remove(id) {
      this.messages = this.messages.filter(m => m.id !== id);
    },

    success(msg, d) { return this.show(msg, 'success', d); },
    error(msg, d)   { return this.show(msg, 'error', d); },
    warn(msg, d)    { return this.show(msg, 'warning', d); },
    info(msg, d)    { return this.show(msg, 'info', d); },
  });

}); // end alpine:init


/* ── Component Factories ────────────────────────────────────────────────────── */

/**
 * Login form component.
 */
function loginComponent() {
  return {
    username:      '',
    password:      '',
    showPassword:  false,
    loading:       false,
    error:         '',
    nextUrl:       new URLSearchParams(window.location.search).get('next') || '/',

    async submit() {
      if (!this.username || !this.password) {
        this.error = 'Please enter username and password.';
        return;
      }
      this.loading = true;
      this.error   = '';

      const form = new URLSearchParams();
      form.append('username', this.username);
      form.append('password', this.password);

      try {
        const resp = await fetch('/auth/login', {
          method:  'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body:    form.toString(),
        });

        if (resp.ok) {
          Alpine.store('toast').success('Welcome back!');
          window.location.href = this.nextUrl;
        } else {
          const data = await resp.json().catch(() => ({}));
          this.error = data.detail || 'Invalid credentials.';
        }
      } catch (e) {
        this.error = 'Network error — please try again.';
      } finally {
        this.loading = false;
      }
    },
  };
}


/**
 * Dashboard overview component with WebSocket live updates.
 */
function overviewComponent(initialData) {
  return {
    data:        initialData || {},
    wsConnected: false,
    lastUpdate:  null,
    _ws:         null,

    init() {
      Alpine.store('app').init();
      this.connectWs();
    },

    destroy() {
      if (this._ws) this._ws.close();
    },

    connectWs() {
      if (!window.WS_ENABLED) return;
      const proto = location.protocol === 'https:' ? 'wss' : 'ws';
      const ws    = new WebSocket(`${proto}://${location.host}/ws/live`);

      ws.onopen = () => {
        this.wsConnected = true;
        Alpine.store('app').wsConnected = true;
      };

      ws.onmessage = (ev) => {
        const msg = JSON.parse(ev.data);
        if (msg.type === 'snapshot' || msg.type === 'refresh') {
          this.data       = msg.data;
          this.lastUpdate = new Date().toLocaleTimeString();
        }
      };

      ws.onclose = () => {
        this.wsConnected = false;
        Alpine.store('app').wsConnected = false;
        // Reconnect after 10 s
        setTimeout(() => this.connectWs(), 10000);
      };

      ws.onerror = () => ws.close();

      // Heartbeat every 20 s
      const ping = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) ws.send('ping');
        else clearInterval(ping);
      }, 20000);

      this._ws = ws;
    },

    fmt(n, prefix = '') {
      if (n === undefined || n === null) return '—';
      if (n >= 1_000_000) return `${prefix}${(n / 1_000_000).toFixed(1)}M`;
      if (n >= 1_000)     return `${prefix}${(n / 1000).toFixed(1)}K`;
      return `${prefix}${Number(n).toFixed(2)}`;
    },

    fmtHours(n) {
      return n !== undefined ? `${Number(n).toFixed(1)}h` : '—';
    },
  };
}


/**
 * Generic list/search/filter component (projects, clients, etc.).
 */
function listComponent(initialItems, filterKey = 'status') {
  return {
    items:       initialItems || [],
    searchQuery: '',
    activeFilter:'',

    get filtered() {
      let result = this.items;
      if (this.activeFilter) {
        result = result.filter(item => item[filterKey] === this.activeFilter);
      }
      if (this.searchQuery.trim()) {
        const q = this.searchQuery.toLowerCase();
        result = result.filter(item =>
          JSON.stringify(item).toLowerCase().includes(q)
        );
      }
      return result;
    },

    setFilter(val) {
      this.activeFilter = this.activeFilter === val ? '' : val;
    },
  };
}


/**
 * Settings panel component with tab switching.
 */
function settingsComponent() {
  return {
    activeTab:  'general',
    theme:      localStorage.getItem('fdo-theme') || 'dark',
    saved:      false,

    setTab(tab) {
      this.activeTab = tab;
    },

    saveGeneral() {
      localStorage.setItem('fdo-theme', this.theme);
      document.documentElement.setAttribute('data-theme', this.theme);
      Alpine.store('app').theme = this.theme;
      Alpine.store('toast').success('Settings saved!');
      this.saved = true;
      setTimeout(() => { this.saved = false; }, 2500);
    },

    async changePassword(current, next, confirm) {
      if (next !== confirm) {
        Alpine.store('toast').error('Passwords do not match.');
        return false;
      }
      if (next.length < 8) {
        Alpine.store('toast').error('Password must be at least 8 characters.');
        return false;
      }
      // In a full implementation this would call /auth/change-password
      Alpine.store('toast').info('Password change requires server restart (see .env).');
      return true;
    },
  };
}


/* ── Chart Helpers ──────────────────────────────────────────────────────────── */

/**
 * Render a Chart.js line chart for revenue.
 *
 * @param {string}   canvasId    - canvas element id
 * @param {object}   monthlyData - { 'YYYY-MM': value, ... }
 */
function renderRevenueChart(canvasId, monthlyData) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || typeof Chart === 'undefined') return;

  const labels = Object.keys(monthlyData).map(k => {
    const [y, m] = k.split('-');
    return new Date(+y, +m - 1).toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
  });
  const values = Object.values(monthlyData);

  // Destroy existing instance to allow re-render
  if (canvas._chartInstance) canvas._chartInstance.destroy();

  canvas._chartInstance = new Chart(canvas, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label:           'Revenue',
        data:             values,
        fill:             true,
        tension:          0.4,
        borderColor:      '#7c3aed',
        backgroundColor:  'rgba(124,58,237,0.1)',
        pointBackgroundColor: '#7c3aed',
        pointRadius:      4,
        pointHoverRadius: 6,
        borderWidth:      2,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { intersect: false, mode: 'index' },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1c2333',
          borderColor:      'rgba(255,255,255,0.1)',
          borderWidth:      1,
          titleColor:       '#f0f6fc',
          bodyColor:        '#8b949e',
          callbacks: {
            label: ctx => ` $${ctx.parsed.y.toFixed(2)}`,
          },
        },
      },
      scales: {
        x: {
          grid:  { color: 'rgba(255,255,255,0.05)' },
          ticks: { color: '#8b949e', font: { size: 11 } },
        },
        y: {
          grid:  { color: 'rgba(255,255,255,0.05)' },
          ticks: {
            color: '#8b949e',
            font:  { size: 11 },
            callback: v => `$${v >= 1000 ? (v / 1000).toFixed(1) + 'k' : v}`,
          },
        },
      },
    },
  });
}


/**
 * Render a doughnut chart for hours by client.
 */
function renderHoursChart(canvasId, byClient) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || typeof Chart === 'undefined') return;

  const palette = ['#7c3aed','#2563eb','#06b6d4','#10b981','#f59e0b','#ef4444','#ec4899'];
  const labels  = Object.keys(byClient);
  const values  = labels.map(k => byClient[k].billable + (byClient[k].non_billable || 0));

  if (canvas._chartInstance) canvas._chartInstance.destroy();

  canvas._chartInstance = new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data:             values,
        backgroundColor:  palette.slice(0, labels.length),
        borderColor:      '#0d1117',
        borderWidth:      3,
        hoverOffset:      6,
      }],
    },
    options: {
      responsive:          true,
      maintainAspectRatio: false,
      cutout:              '65%',
      plugins: {
        legend: {
          position: 'right',
          labels:   { color: '#8b949e', boxWidth: 12, padding: 14, font: { size: 12 } },
        },
        tooltip: {
          backgroundColor: '#1c2333',
          titleColor:      '#f0f6fc',
          bodyColor:       '#8b949e',
          callbacks: {
            label: ctx => ` ${ctx.label}: ${ctx.parsed.toFixed(1)}h`,
          },
        },
      },
    },
  });
}


/**
 * Render a horizontal bar chart for pipeline value by stage.
 */
function renderPipelineChart(canvasId, stages) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || typeof Chart === 'undefined') return;

  const labels = Object.keys(stages);
  const values = labels.map(k => stages[k].reduce((s, i) => s + (i.value || 0), 0));

  if (canvas._chartInstance) canvas._chartInstance.destroy();

  canvas._chartInstance = new Chart(canvas, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label:           'Pipeline Value ($)',
        data:             values,
        backgroundColor: ['rgba(124,58,237,0.7)','rgba(37,99,235,0.7)','rgba(6,182,212,0.7)','rgba(16,185,129,0.7)'],
        borderRadius:    6,
        borderSkipped:   false,
      }],
    },
    options: {
      indexAxis:           'y',
      responsive:          true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1c2333',
          callbacks: {
            label: ctx => ` $${ctx.parsed.x.toFixed(2)}`,
          },
        },
      },
      scales: {
        x: {
          grid:  { color: 'rgba(255,255,255,0.05)' },
          ticks: { color: '#8b949e', callback: v => `$${v >= 1000 ? (v/1000).toFixed(0)+'k' : v}` },
        },
        y: {
          grid:  { display: false },
          ticks: { color: '#8b949e', font: { size: 12 }, textTransform: 'capitalize' },
        },
      },
    },
  });
}


/* ── Utility Functions ──────────────────────────────────────────────────────── */

/**
 * Animate a counter from 0 to target value over duration ms.
 */
function animateCounter(el, target, duration = 800, prefix = '', suffix = '') {
  if (!el) return;
  const start  = performance.now();
  const update = (now) => {
    const pct = Math.min((now - start) / duration, 1);
    const val = pct * target;
    el.textContent = prefix + (Number.isInteger(target) ? Math.round(val) : val.toFixed(2)) + suffix;
    if (pct < 1) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}


/**
 * Kick off counter animations for all elements with data-counter attribute.
 */
function initCounters() {
  document.querySelectorAll('[data-counter]').forEach(el => {
    const target = parseFloat(el.dataset.counter);
    const prefix = el.dataset.prefix || '';
    const suffix = el.dataset.suffix || '';
    if (!isNaN(target)) animateCounter(el, target, 900, prefix, suffix);
  });
}


/**
 * Lightweight debounce helper.
 */
function debounce(fn, delay = 300) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}


/* ── DOM Ready ──────────────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  // Apply saved theme immediately
  const saved = localStorage.getItem('fdo-theme');
  if (saved) document.documentElement.setAttribute('data-theme', saved);

  // Counter animations (for non-Alpine pages)
  initCounters();

  // Keyboard shortcut: Ctrl/Cmd+K → focus search
  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      document.querySelector('.search-box input')?.focus();
    }
    // Escape → close sidebar on mobile
    if (e.key === 'Escape' && window.innerWidth <= 900) {
      Alpine.store('app').sidebarOpen = false;
    }
  });
});


/* ── Export for templates ───────────────────────────────────────────────────── */
window.FDO = {
  loginComponent,
  overviewComponent,
  listComponent,
  settingsComponent,
  renderRevenueChart,
  renderHoursChart,
  renderPipelineChart,
  animateCounter,
  initCounters,
  debounce,
};

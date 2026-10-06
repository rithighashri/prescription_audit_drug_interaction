<template>
  <div class="app" v-if="!isLoginPage">
    <header class="header">
  <div class="top-bar" v-if="user">
    <span class="welcome-text">{{ user.full_name }} <span class="role-tag">({{ user.role }})</span></span>
    <button class="btn-logout-large" @click="handleLogout">Logout</button>
  </div>

  <h1>Prescription Audit Portal</h1>
  <p class="subtitle">Outpatient drug interaction & override tracking</p>
  <nav class="nav">
    <RouterLink to="/patients">Patients</RouterLink>
    <RouterLink to="/add-patient">Add Patient</RouterLink>
    <RouterLink to="/prescriptions">New Prescription</RouterLink>
    <RouterLink v-if="user?.role === 'admin'" to="/audit">Audit Dashboard</RouterLink>
  </nav>
</header>

    <RouterView />
  </div>
  <RouterView v-else />
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getUser, logout } from './auth.js'

const route = useRoute()
const router = useRouter()
const user = computed(() => getUser())
const isLoginPage = computed(() => route.path === '/login')

function handleLogout() {
  logout()
  router.push('/login')
}
</script>

<style>
/* ===== Design tokens ===== */
* { box-sizing: border-box; }

:root {
  --bg-primary: #0d0e13;
  --bg-card: #1a1b23;
  --bg-input: #12131a;
  --border: #2a2c38;
  --text-primary: #f4f4f6;
  --text-secondary: #9499ad;
  --accent-blue: #6ea8fe;
  --accent-purple: #a78bfa;
  --accent-gradient: linear-gradient(135deg, #6ea8fe 0%, #a78bfa 55%, #e879f9 100%);
  --success: #4ade80;
  --warning: #fbbf24;
  --danger: #f87171;
  --radius-lg: 16px;
  --radius-md: 10px;
  --shadow-soft: 0 8px 30px rgba(0, 0, 0, 0.35);
  --shadow-glow: 0 0 0 1px rgba(110, 168, 254, 0.1), 0 8px 24px rgba(110, 168, 254, 0.08);
}

body {
  background: radial-gradient(ellipse at top, #16171f 0%, #0a0b0f 60%);
  min-height: 100vh;
}

.app {
  max-width: 980px;
  margin: 0 auto;
  padding: 2rem 1.5rem 4rem;
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  color: var(--text-primary);
}

/* ===== Top bar ===== */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 980px;
  margin: 0 auto 1.8rem;
  padding: 1rem 1.5rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-soft);
}
.welcome-text {
  font-size: 1.3rem;
  color: #ffffff;
  font-weight: 800;
  letter-spacing: 0.2px;
}
.role-tag {
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 0.95rem;
  margin-left: 0.4rem;
  text-transform: capitalize;
}
.btn-logout-large {
  background: linear-gradient(135deg, #b8590a, #d97706);
  color: white;
  border: none;
  padding: 0.75rem 1.7rem;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
  box-shadow: 0 4px 14px rgba(184, 89, 10, 0.3);
}
.btn-logout-large:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(184, 89, 10, 0.45); }

/* ===== Header ===== */
.header { text-align: center; margin-bottom: 2.8rem; }
.header h1 {
  font-size: 2.8rem;
  margin-bottom: 0.4rem;
  font-weight: 800;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}
.subtitle { color: var(--text-secondary); font-size: 1.05rem; }

/* ===== Nav ===== */
.nav {
  display: flex;
  justify-content: center;
  gap: 0.6rem;
  margin-top: 1.8rem;
  flex-wrap: wrap;
}
.nav a {
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 600;
  padding: 0.65rem 1.3rem;
  border-radius: 999px;
  transition: all 0.15s;
  border: 1px solid transparent;
}
.nav a:hover { color: var(--text-primary); background: rgba(255,255,255,0.04); }
.nav a.router-link-active {
  color: white;
  background: var(--accent-gradient);
  box-shadow: 0 4px 16px rgba(110, 168, 254, 0.35);
}

/* ===== Cards ===== */
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 2rem;
  margin-bottom: 1.8rem;
  box-shadow: var(--shadow-soft);
  transition: box-shadow 0.2s;
}
.card:hover { box-shadow: var(--shadow-soft), var(--shadow-glow); }
.card h2 {
  margin-top: 0;
  margin-bottom: 1.4rem;
  font-size: 1.35rem;
  color: #fafafa;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.card h2::before {
  content: '';
  width: 4px;
  height: 20px;
  background: var(--accent-gradient);
  border-radius: 4px;
  display: inline-block;
}

/* ===== Tables ===== */
.data-table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td { padding: 0.85rem 1.1rem; text-align: left; border-bottom: 1px solid var(--border); font-size: 0.95rem; }
.data-table th { color: var(--text-secondary); font-weight: 700; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.5px; }
.data-table tbody tr { transition: background 0.12s; }
.data-table tbody tr:hover { background: rgba(255,255,255,0.025); }

/* ===== Forms ===== */
.form-row { margin-bottom: 1.5rem; }
.form-row label { display: block; margin-bottom: 0.55rem; font-weight: 600; color: #d1d5db; font-size: 0.95rem; }
.hint { font-weight: 400; color: #6b7280; font-size: 0.85rem; }
.form-row input[type="text"], .form-row input[type="number"], .patient-select {
  width: 100%; padding: 0.8rem 1rem; border-radius: var(--radius-md);
  border: 1px solid var(--border); background: var(--bg-input); color: var(--text-primary);
  font-size: 1rem; transition: border-color 0.15s, box-shadow 0.15s;
}
.form-row input:focus, .patient-select:focus {
  outline: none; border-color: var(--accent-blue);
  box-shadow: 0 0 0 3px rgba(110, 168, 254, 0.15);
}
.patient-info { margin-top: 0.6rem; font-size: 0.9rem; color: var(--text-secondary); }
.patient-info strong { color: var(--warning); }

/* ===== Drug picker ===== */
.drug-search-input {
  width: 100%; padding: 0.8rem 1rem; border-radius: var(--radius-md) var(--radius-md) 0 0;
  border: 1px solid var(--border); border-bottom: none; background: var(--bg-input);
  color: var(--text-primary); font-size: 1rem;
}
.drug-checklist {
  max-height: 260px; overflow-y: auto; border: 1px solid var(--border);
  border-radius: 0 0 var(--radius-md) var(--radius-md); background: var(--bg-input); padding: 0.5rem;
}
.drug-checkbox-row { display: flex; align-items: center; gap: 0.6rem; padding: 0.55rem 0.5rem; border-radius: 6px; cursor: pointer; transition: background 0.12s; }
.drug-checkbox-row:hover { background: rgba(110,168,254,0.08); }
.no-results { color: #6b7280; padding: 0.5rem; }
.selected-tags { margin-top: 0.8rem; display: flex; flex-wrap: wrap; gap: 0.5rem; }
.tag {
  background: rgba(110,168,254,0.12); color: var(--accent-blue);
  padding: 0.35rem 0.85rem; border-radius: 999px; font-size: 0.85rem; font-weight: 600;
  border: 1px solid rgba(110,168,254,0.25);
}

/* ===== Buttons ===== */
.btn-primary {
  background: var(--accent-gradient); color: white; border: none;
  padding: 0.85rem 1.8rem; border-radius: var(--radius-md); font-size: 1rem; font-weight: 700;
  cursor: pointer; transition: transform 0.15s, box-shadow 0.15s;
  box-shadow: 0 4px 18px rgba(110, 168, 254, 0.3);
}
.btn-primary:hover { transform: translateY(-1px); box-shadow: 0 6px 24px rgba(110, 168, 254, 0.45); }
.btn-warning {
  background: linear-gradient(135deg, #d97706, #ea580c); color: white; border: none;
  padding: 0.75rem 1.5rem; border-radius: var(--radius-md); font-weight: 700; cursor: pointer;
  transition: transform 0.15s;
}
.btn-warning:hover { transform: translateY(-1px); }

/* ===== Warning box ===== */
.warning-box {
  margin-top: 1.6rem; padding: 1.5rem 1.7rem; background: rgba(251, 191, 36, 0.06);
  border: 1px solid rgba(251, 191, 36, 0.35); border-radius: var(--radius-md);
}
.warning-box h3 { margin-top: 0; color: var(--warning); font-size: 1.1rem; }
.warning-box ul { padding-left: 1.2rem; }
.warning-box li { margin-bottom: 0.9rem; }
.note { color: #d4b06a; font-size: 0.9rem; }

.severity { margin-left: 0.6rem; padding: 0.2rem 0.7rem; border-radius: 999px; font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.3px; }
.severity.major { background: rgba(248, 113, 113, 0.15); color: var(--danger); }
.severity.moderate { background: rgba(251, 191, 36, 0.15); color: var(--warning); }
.severity.minor { background: rgba(74, 222, 128, 0.15); color: var(--success); }

.override-row { margin-top: 1.2rem; padding-top: 1.2rem; border-top: 1px solid rgba(251,191,36,0.2); }
.override-row label { display: block; margin-bottom: 0.55rem; font-weight: 600; }
.override-row input {
  width: 100%; padding: 0.7rem 0.9rem; border-radius: var(--radius-md);
  border: 1px solid rgba(251,191,36,0.3); background: var(--bg-input); color: white; margin-bottom: 0.9rem;
}

.success-msg { margin-top: 1.3rem; color: var(--success); font-weight: 700; display: flex; align-items: center; gap: 0.4rem; }
.risk-badge { margin: 0.6rem 0 1.1rem; font-size: 0.95rem; color: #d4b8ff; }
.risk-badge strong { color: var(--warning); }

/* ===== Stats ===== */
.stats-row { display: flex; gap: 1.1rem; margin-bottom: 2rem; }
.stat-box {
  flex: 1; background: var(--bg-input); border: 1px solid var(--border);
  border-radius: var(--radius-md); padding: 1.4rem; text-align: center;
  transition: transform 0.15s;
}
.stat-box:hover { transform: translateY(-2px); }
.stat-number { font-size: 2.2rem; font-weight: 800; background: var(--accent-gradient); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
.stat-label { color: var(--text-secondary); font-size: 0.8rem; margin-top: 0.4rem; text-transform: uppercase; letter-spacing: 0.5px; }

.override-row-highlight { background: rgba(251, 191, 36, 0.05) !important; }
.action-badge, .override-badge { padding: 0.25rem 0.7rem; border-radius: 999px; font-size: 0.75rem; font-weight: 800; }
.action-badge.override { background: rgba(251,191,36,0.15); color: var(--warning); }
.action-badge.create { background: rgba(74,222,128,0.15); color: var(--success); }
.override-badge.high { background: rgba(248,113,113,0.15); color: var(--danger); }
.override-badge.normal { background: rgba(74,222,128,0.15); color: var(--success); }
</style>
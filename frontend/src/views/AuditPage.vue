<template>
  <div>
    <section class="card">
      <h2>Audit Dashboard</h2>
      <div class="stats-row">
        <div class="stat-box">
          <div class="stat-number">{{ stats.total_actions }}</div>
          <div class="stat-label">Total Actions</div>
        </div>
        <div class="stat-box">
          <div class="stat-number">{{ stats.total_overrides }}</div>
          <div class="stat-label">Overrides</div>
        </div>
        <div class="stat-box">
          <div class="stat-number">{{ stats.override_rate_percent }}%</div>
          <div class="stat-label">Override Rate</div>
        </div>
      </div>
    </section>

    <section class="card">
      <h2>Override Rate by Doctor</h2>
      <table class="data-table">
        <thead>
          <tr><th>Doctor</th><th>Total Prescriptions</th><th>Overrides</th><th>Override Rate</th></tr>
        </thead>
        <tbody>
          <tr v-for="doc in doctorSummary" :key="doc.doctor_name">
            <td>{{ doc.doctor_name }}</td>
            <td>{{ doc.total_prescriptions }}</td>
            <td>{{ doc.overrides }}</td>
            <td>
              <span :class="['override-badge', doc.override_rate_percent > 50 ? 'high' : 'normal']">
                {{ doc.override_rate_percent }}%
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <section class="card">
      <h2>All Prescriptions</h2>
      <table class="data-table">
        <thead>
          <tr><th>ID</th><th>Patient ID</th><th>Doctor</th><th>Drugs</th><th>Created</th><th>Overridden?</th><th>Reason</th></tr>
        </thead>
        <tbody>
          <tr v-for="rx in allPrescriptions" :key="rx.id" :class="{ 'override-row-highlight': rx.was_overridden }">
            <td>{{ rx.id }}</td>
            <td>{{ rx.patient_id }}</td>
            <td>{{ rx.doctor_name }}</td>
            <td>{{ rx.drugs.join(', ') }}</td>
            <td>{{ rx.created_at }}</td>
            <td>
              <span :class="['action-badge', rx.was_overridden ? 'override' : 'create']">
                {{ rx.was_overridden ? 'Overridden' : 'Clean' }}
              </span>
            </td>
            <td>{{ rx.override_reason || '—' }}</td>
          </tr>
        </tbody>
      </table>
    </section>

    <section class="card">
      <h2>Full Audit Log</h2>
      <table class="data-table">
        <thead>
          <tr><th>ID</th><th>Prescription</th><th>Action</th><th>Doctor</th><th>Details</th><th>Override Reason</th><th>Timestamp</th></tr>
        </thead>
        <tbody>
          <tr v-for="log in auditLogs" :key="log.id" :class="{ 'override-row-highlight': log.action === 'override' }">
            <td>{{ log.id }}</td>
            <td>#{{ log.prescription_id }}</td>
            <td><span :class="['action-badge', log.action]">{{ log.action }}</span></td>
            <td>{{ log.doctor_name }}</td>
            <td>{{ log.details }}</td>
            <td>{{ log.override_reason || '—' }}</td>
            <td>{{ log.timestamp }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const auditLogs = ref([])
const stats = ref({ total_actions: 0, total_overrides: 0, override_rate_percent: 0 })
const doctorSummary = ref([])
const allPrescriptions = ref([])

onMounted(async () => {
  const logsRes = await axios.get('http://127.0.0.1:5000/audit-log')
  auditLogs.value = logsRes.data

  const statsRes = await axios.get('http://127.0.0.1:5000/audit-log/stats')
  stats.value = statsRes.data

  const doctorsRes = await axios.get('http://127.0.0.1:5000/doctors/override-summary')
  doctorSummary.value = doctorsRes.data

  const prescriptionsRes = await axios.get('http://127.0.0.1:5000/prescriptions/detailed')
  allPrescriptions.value = prescriptionsRes.data
})
</script>
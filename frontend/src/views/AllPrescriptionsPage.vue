<template>
  <section class="card">
    <h2>All Prescriptions (All Doctors)</h2>

    <div class="form-row">
      <label>Filter by Doctor</label>
      <select v-model="selectedDoctor" class="patient-select" @change="loadPrescriptions">
        <option value="">All Doctors</option>
        <option v-for="doc in doctorNames" :key="doc" :value="doc">{{ doc }}</option>
      </select>
    </div>

    <table class="data-table">
      <thead>
        <tr>
          <th>ID</th><th>Patient ID</th><th>Doctor</th><th>Drugs</th>
          <th>Created</th><th>Status</th><th>Override Reason</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="rx in prescriptions" :key="rx.id" :class="{ 'override-row-highlight': rx.was_overridden }">
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
    <p v-if="prescriptions.length === 0" class="no-results">No prescriptions found.</p>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const allPrescriptions = ref([])
const prescriptions = ref([])
const selectedDoctor = ref('')

const doctorNames = computed(() =>
  [...new Set(allPrescriptions.value.map(p => p.doctor_name))].sort()
)

async function loadPrescriptions() {
  const params = selectedDoctor.value ? { doctor_name: selectedDoctor.value } : {}
  const res = await axios.get('http://127.0.0.1:5000/prescriptions/detailed', { params })
  prescriptions.value = res.data
}

onMounted(async () => {
  const allRes = await axios.get('http://127.0.0.1:5000/prescriptions/detailed')
  allPrescriptions.value = allRes.data
  prescriptions.value = allRes.data
})
</script>
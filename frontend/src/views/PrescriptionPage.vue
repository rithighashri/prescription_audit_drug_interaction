<template>
  <section class="card">
    <h2>New Prescription</h2>

    <div class="form-row">
      <label>Patient</label>
      <select v-model.number="form.patient_id" class="patient-select">
        <option :value="null" disabled>Select a patient</option>
        <option v-for="patient in patients" :key="patient.id" :value="patient.id">
          {{ patient.name }} (Age {{ patient.age }}, {{ patient.gender }})
        </option>
      </select>
      <p v-if="selectedPatient" class="patient-info">
        Known allergies: <strong>{{ selectedPatient.allergies || 'None recorded' }}</strong>
      </p>
    </div>

    <div class="form-row">
      <label>Doctor Name</label>
      <input v-model="form.doctor_name" type="text" placeholder="e.g. Dr. Smith" />
    </div>

    <div class="form-row">
      <label>Select Drugs</label>
      <input
        v-model="drugSearch"
        type="text"
        placeholder="Type to search drugs..."
        class="drug-search-input"
      />
      <div class="drug-checklist">
        <label v-for="drug in filteredDrugs" :key="drug.id" class="drug-checkbox-row">
          <input type="checkbox" :value="drug.id" v-model="form.drug_ids" />
          {{ drug.name }}
        </label>
        <p v-if="filteredDrugs.length === 0" class="no-results">No drugs match "{{ drugSearch }}"</p>
      </div>
      <div class="selected-tags" v-if="form.drug_ids.length">
        <span class="tag" v-for="id in form.drug_ids" :key="id">
          {{ drugs.find(d => d.id === id)?.name }}
        </span>
      </div>
    </div>

    <button class="btn-primary" @click="submitPrescription">Create Prescription</button>

    <div v-if="warnings.length" class="warning-box">
      <h3>⚠ Interaction Warnings</h3>

      <p v-if="overrideRisk !== null" class="risk-badge">
        🤖 AI-predicted override likelihood: <strong>{{ (overrideRisk * 100).toFixed(0) }}%</strong>
      </p>

      <ul>
        <li v-for="(w, i) in warnings" :key="i">
          <strong>{{ w.drug_a }} + {{ w.drug_b }}</strong>
          <span :class="['severity', w.severity]">{{ w.severity }}</span>
          <br /><span class="note">{{ w.note }}</span>
        </li>
      </ul>

      <div v-if="needsOverride" class="override-row">
        <label>Override reason</label>
        <input v-model="form.override_reason" type="text" placeholder="Why proceed despite the warning?" />
        <button class="btn-warning" @click="submitPrescription">Confirm Override & Save</button>
      </div>
    </div>

    <p v-if="successMessage" class="success-msg">✓ {{ successMessage }}</p>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const patients = ref([])
const drugs = ref([])
const warnings = ref([])
const needsOverride = ref(false)
const successMessage = ref('')
const overrideRisk = ref(null)
const drugSearch = ref('')

const form = ref({
  patient_id: null,
  doctor_name: '',
  drug_ids: [],
  override_reason: ''
})

const selectedPatient = computed(() =>
  patients.value.find(p => p.id === form.value.patient_id)
)

const sortedDrugs = computed(() =>
  [...drugs.value].sort((a, b) => a.name.localeCompare(b.name))
)

const filteredDrugs = computed(() =>
  sortedDrugs.value.filter(d =>
    d.name.toLowerCase().includes(drugSearch.value.toLowerCase())
  )
)

onMounted(async () => {
  const patientsRes = await axios.get('http://127.0.0.1:5000/patients')
  patients.value = patientsRes.data
  const drugsRes = await axios.get('http://127.0.0.1:5000/drugs')
  drugs.value = drugsRes.data
})

async function submitPrescription() {
  try {
    const res = await axios.post('http://127.0.0.1:5000/prescriptions', form.value)

    if (res.data.requires_override) {
      warnings.value = res.data.interaction_warnings
      needsOverride.value = true
      successMessage.value = ''

      const topSeverity = warnings.value[0].severity === 'major' ? 3
                          : warnings.value[0].severity === 'moderate' ? 2 : 1
      const currentHour = new Date().getHours()

      const predictRes = await axios.post('http://127.0.0.1:5000/predict-override-risk', {
        severity: topSeverity,
        patient_age: selectedPatient.value?.age || 50,
        allergy_count: selectedPatient.value?.allergies ? 1 : 0,
        active_med_count: form.value.drug_ids.length,
        doctor_override_rate: 0.3,
        time_of_day_busy: (currentHour >= 9 && currentHour <= 17) ? 1 : 0
      })
      overrideRisk.value = predictRes.data.override_likelihood

    } else {
      warnings.value = res.data.interaction_warnings || []
      needsOverride.value = false
      successMessage.value = `Prescription created (ID: ${res.data.id})`
      overrideRisk.value = null
    }
  } catch (err) {
    console.error(err)
  }
}
</script>
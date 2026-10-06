<template>
  <section class="card">
    <h2>Patients</h2>
    <table class="data-table">
      <thead>
        <tr><th>ID</th><th>Name</th><th>Age</th><th>Gender</th><th>Allergies</th></tr>
      </thead>
      <tbody>
        <tr v-for="patient in patients" :key="patient.id">
          <td>{{ patient.id }}</td>
          <td>{{ patient.name }}</td>
          <td>{{ patient.age }}</td>
          <td>{{ patient.gender }}</td>
          <td>{{ patient.allergies || '—' }}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const patients = ref([])

onMounted(async () => {
  const res = await axios.get('http://127.0.0.1:5000/patients')
  patients.value = res.data
})
</script>
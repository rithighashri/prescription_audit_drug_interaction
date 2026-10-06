<template>
  <section class="card">
    <h2>Add Patient</h2>
    <div class="form-row">
      <label>Name</label>
      <input v-model="newPatient.name" type="text" placeholder="Full name" />
    </div>
    <div class="form-row">
      <label>Age</label>
      <input v-model.number="newPatient.age" type="number" placeholder="Age" />
    </div>
    <div class="form-row">
      <label>Gender</label>
      <select v-model="newPatient.gender" class="patient-select">
        <option disabled value="">Select gender</option>
        <option>Male</option>
        <option>Female</option>
        <option>Other</option>
      </select>
    </div>
    <div class="form-row">
      <label>Allergies</label>
      <input v-model="newPatient.allergies" type="text" placeholder="e.g. Penicillin, or leave blank" />
    </div>
    <button class="btn-primary" @click="addPatient">Add Patient</button>
    <p v-if="message" class="success-msg">✓ {{ message }}</p>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const newPatient = ref({ name: '', age: null, gender: '', allergies: '' })
const message = ref('')

async function addPatient() {
  try {
    const res = await axios.post('http://127.0.0.1:5000/patients', newPatient.value)
    message.value = `${newPatient.value.name} added (ID: ${res.data.id})`
    newPatient.value = { name: '', age: null, gender: '', allergies: '' }
  } catch (err) {
    console.error(err)
  }
}
</script>
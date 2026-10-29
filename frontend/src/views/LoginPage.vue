<template>
  <div class="login-wrapper">
    <div class="login-card">
      <div class="login-icon">🩺</div>
      <h1>Prescription Audit Portal</h1>
      <p class="subtitle">Sign in to continue</p>

      <div class="form-row">
        <label>Username</label>
        <input
          v-model="username"
          type="text"
          placeholder="e.g. dr.smith"
          @keyup.enter="login"
          autofocus
        />
      </div>

      <div class="form-row">
        <label>Password</label>
        <input
          v-model="password"
          type="password"
          placeholder="Enter your password"
          @keyup.enter="login"
        />
      </div>

      <button class="btn-primary btn-full" @click="login">Sign In</button>

      <p v-if="error" class="error-msg">{{ error }}</p>

      <div class="login-hint">
        <p>Demo accounts:</p>
        <p><strong>Doctor:</strong> dr.smith0 / doctor123</p>
        <p><strong>Admin:</strong> admin / admin123</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api.js'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

async function login() {
  try {
    const res = await api.post('/login', {
      username: username.value,
      password: password.value
    })
    localStorage.setItem('user', JSON.stringify(res.data))
    router.push('/patients')
  } catch (err) {
    error.value = 'Invalid username or password'
  }
}
</script>

<style scoped>
.login-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: radial-gradient(circle at top, #cae9ff, #f7fbff 62%, #e8f3ff);
  padding: 2rem;
}

.login-card {
  background: #ffffff;
  border: 1px solid #cbd9ea;
  border-radius: 20px;
  padding: 3.5rem 3rem;
  width: 100%;
  max-width: 480px;
  text-align: center;
  box-shadow: 0 20px 60px rgba(35, 97, 158, 0.18);
}

.login-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.login-card h1 {
  font-size: 2rem;
  margin-bottom: 0.4rem;
  background: linear-gradient(90deg, #0878e8, #7c3aed);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
}

.subtitle {
  color: #486581;
  margin-bottom: 2.5rem;
  font-size: 1.05rem;
}

.form-row {
  margin-bottom: 1.6rem;
  text-align: left;
}

.form-row label {
  display: block;
  margin-bottom: 0.6rem;
  font-weight: 600;
  color: #102a43;
  font-size: 0.95rem;
}

.form-row input {
  width: 100%;
  padding: 1rem 1.2rem;
  border-radius: 10px;
  border: 1px solid #b9cce0;
  background: #f8fbff;
  color: #102a43;
  font-size: 1.05rem;
  transition: border-color 0.15s;
}

.form-row input:focus {
  outline: none;
  border-color: #0866d8;
  box-shadow: 0 0 0 3px rgba(8, 102, 216, 0.15);
}

.btn-full {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
  margin-top: 0.5rem;
}

.error-msg {
  color: #c62828;
  margin-top: 1.2rem;
  font-size: 0.95rem;
}

.login-hint {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #d7e3f0;
  color: #486581;
  font-size: 0.85rem;
  line-height: 1.6;
}

.login-hint strong {
  color: #1f4f82;
}
</style>

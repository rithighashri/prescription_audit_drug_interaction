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
        <p><strong>Doctor:</strong> dr.smith / doctor123</p>
        <p><strong>Admin:</strong> admin / admin123</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

async function login() {
  try {
    const res = await axios.post('http://127.0.0.1:5000/login', {
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
  background: radial-gradient(circle at top, #1a1b22, #0d0e12);
  padding: 2rem;
}

.login-card {
  background: #1e1f26;
  border: 1px solid #2f3038;
  border-radius: 20px;
  padding: 3.5rem 3rem;
  width: 100%;
  max-width: 480px;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.login-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.login-card h1 {
  font-size: 2rem;
  margin-bottom: 0.4rem;
  background: linear-gradient(90deg, #6ea8fe, #a78bfa);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
}

.subtitle {
  color: #9ca3af;
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
  color: #d1d5db;
  font-size: 0.95rem;
}

.form-row input {
  width: 100%;
  padding: 1rem 1.2rem;
  border-radius: 10px;
  border: 1px solid #3a3b45;
  background: #14151a;
  color: #f5f5f5;
  font-size: 1.05rem;
  transition: border-color 0.15s;
}

.form-row input:focus {
  outline: none;
  border-color: #6ea8fe;
  box-shadow: 0 0 0 3px rgba(110, 168, 254, 0.15);
}

.btn-full {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
  margin-top: 0.5rem;
}

.error-msg {
  color: #ff6b6b;
  margin-top: 1.2rem;
  font-size: 0.95rem;
}

.login-hint {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #2f3038;
  color: #6b7280;
  font-size: 0.85rem;
  line-height: 1.6;
}

.login-hint strong {
  color: #9ca3af;
}
</style>
import { ref } from 'vue'

function readStoredUser() {
  try {
    const raw = localStorage.getItem('user')
    return raw ? JSON.parse(raw) : null
  } catch {
    localStorage.removeItem('user')
    return null
  }
}

export const currentUser = ref(readStoredUser())

export function getUser() {
  return currentUser.value
}

export function setUser(user) {
  localStorage.setItem('user', JSON.stringify(user))
  currentUser.value = user
}

export function logout() {
  localStorage.removeItem('user')
  currentUser.value = null
}

export function isAdmin() {
  const user = getUser()
  return user?.role === 'admin'
}

export function getUser() {
  const raw = localStorage.getItem('user')
  return raw ? JSON.parse(raw) : null
}

export function logout() {
  localStorage.removeItem('user')
}

export function isAdmin() {
  const user = getUser()
  return user?.role === 'admin'
}
import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from './views/LoginPage.vue'
import PatientsPage from './views/PatientsPage.vue'
import AddPatientPage from './views/AddPatientPage.vue'
import PrescriptionPage from './views/PrescriptionPage.vue'
import AuditPage from './views/AuditPage.vue'
import { getUser } from './auth.js'
import AllPrescriptionsPage from './views/AllPrescriptionsPage.vue'

const routes = [
  { path: '/', redirect: '/patients' },
  { path: '/login', component: LoginPage },
  { path: '/patients', component: PatientsPage, meta: { requiresAuth: true } },
  { path: '/add-patient', component: AddPatientPage, meta: { requiresAuth: true } },
  { path: '/prescriptions', component: PrescriptionPage, meta: { requiresAuth: true } },
  { path: '/audit', component: AuditPage, meta: { requiresAuth: true, adminOnly: true } },
  { path: '/all-prescriptions', component: AllPrescriptionsPage, meta: { requiresAuth: true, adminOnly: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const user = getUser()
  if (to.meta.requiresAuth && !user) {
    next('/login')
  } else if (to.meta.adminOnly && user?.role !== 'admin') {
    next('/patients')
  } else {
    next()
  }
})

export default router
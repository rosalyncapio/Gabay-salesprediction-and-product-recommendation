import { createRouter, createWebHistory } from 'vue-router'

// Import components
import PurchaseHistory from '../views/products/PurchaseHistory.vue'
import PurchaseForm from '../views/products/PurchaseForm.vue'
import AutomaticRecommendations from '../views/products/AutomaticRecommendations.vue'
import SalesForm from '../views/sales/SalesForm.vue'
import SalesHistory from '../views/sales/SalesHistory.vue'
import SalesPrediction from '../views/sales/SalesPrediction.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { title: 'Dashboard' }
  },
  {
    path: '/products',
    name: 'Products',
    component: () => import('../views/ProductsPage.vue'),
    meta: { title: 'Product Management' }
  },
  {
    path: '/sales',
    name: 'Sales',
    component: () => import('../views/Sales.vue'),
    meta: { title: 'Sales Management' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: { title: 'Page Not Found' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard to update document title
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title} | CAPIO` || 'CAPIO'
  next()
})

export default router


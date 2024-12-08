<template>
  <div class="management-page products-management">
    <div class="container">
      <h1 class="page-title">Products Management</h1>
      <div class="management-card">
        <nav class="management-nav">
          <router-link
            v-for="link in links"
            :key="link.to"
            :to="link.to"
            class="nav-link"
            :class="{ 'active': isActive(link.to) }"
          >
            {{ link.text }}
          </router-link>
        </nav>
        <div class="management-content">
          <router-view></router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const links = [
  { to: '/products/history', text: 'Purchase History' },
  { to: '/products/purchase', text: 'New Purchase' },
  { to: '/products/recommendations', text: 'Recommendations' }
]

const isActive = (path) => computed(() => route.path === path).value
</script>

<style scoped>
.products-management {
  --primary-color: #3b82f6;
  --primary-dark: #2563eb;
}
</style>
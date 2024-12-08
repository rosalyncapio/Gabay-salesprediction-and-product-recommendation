<template>
  <div id="app" class="d-flex">
    <Sidebar />
    <main class="main-content flex-grow-1 p-4">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup>
import Sidebar from '@/components/Sidebar.vue';
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
}

.main-content {
  margin-left: 250px;
}
</style>


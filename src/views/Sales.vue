<template>
  <div class="sales-page">
    <h1 class="h2 mb-4">Sales Management</h1>
    <div class="card">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="h4 mb-0">Sales History</h2>
          <button @click="showSalesForm = true" class="btn btn-primary">Add New Sales Data</button>
        </div>
        <SalesHistory />
      </div>
    </div>

    <!-- Sales Form Modal -->
    <div v-if="showSalesForm" class="modal" tabindex="-1" style="display: block;">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <!-- <h5 class="modal-title">Add New Sales Data</h5> -->
            <button type="button" class="btn-close" @click="showSalesForm = false"></button>
          </div>
          <div class="modal-body">
            <SalesForm @sales-added="onSalesAdded" />
          </div>
        </div>
      </div>
    </div>
    <div v-if="showSalesForm" class="modal-backdrop fade show"></div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import SalesHistory from './sales/SalesHistory.vue';
import SalesForm from './sales/SalesForm.vue';

const showSalesForm = ref(false);

const onSalesAdded = () => {
  showSalesForm.value = false;
  // You might want to refresh the SalesHistory component here
};
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.5);
}
</style>


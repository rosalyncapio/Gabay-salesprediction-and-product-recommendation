<template>
    <div class="products-page">
      <h1 class="h2 mb-4">Product Management</h1>
      <div class="card">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="h4 mb-0">Purchase History</h2>
            <button @click="showPurchaseForm = true" class="btn btn-primary">Add New Purchase</button>
          </div>
          <PurchaseHistory />
        </div>
      </div>
  
      <div v-if="showPurchaseForm" class="modal" tabindex="-1" style="display: block;">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Add New Purchase</h5>
              <button type="button" class="btn-close" @click="showPurchaseForm = false"></button>
            </div>
            <div class="modal-body">
              <PurchaseForm @purchase-added="onPurchaseAdded" />
            </div>
          </div>
        </div>
      </div>
      <div v-if="showPurchaseForm" class="modal-backdrop fade show"></div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import PurchaseHistory from './products/PurchaseHistory.vue';
  import PurchaseForm from './products/PurchaseForm.vue';
  
  const showPurchaseForm = ref(false);
  
  const onPurchaseAdded = () => {
    showPurchaseForm.value = false;
    // You might want to refresh the PurchaseHistory component h  ere
  };
  </script>
  
  <style scoped>
  .modal {
    background-color: rgba(0, 0, 0, 0.5);
  }
  </style>
  
  
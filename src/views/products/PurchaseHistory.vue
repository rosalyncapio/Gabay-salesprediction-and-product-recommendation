<template>
  <div class="history-container">
    <div v-if="loading" class="loading-state">
      <div class="animate-spin"></div>
      <p class="loading-text">Loading purchase history...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>Item</th>
            <th>Category</th>
            <th>Quantity</th>
            <th>Price</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="purchase in history" :key="purchase.id">
            <td>{{ purchase.item_name }}</td>
            <td>{{ purchase.category }}</td>
            <td>{{ purchase.quantity }}</td>
            <td>{{ formatCurrency(purchase.unit_price) }}</td>
            <td>{{ formatCurrency(purchase.quantity * purchase.unit_price) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { getPurchaseHistory } from '@/services/api'

const history = ref([])
const loading = ref(true)
const error = ref(null)

const fetchHistory = async () => {
  try {
    const response = await getPurchaseHistory()
    history.value = response.data
  } catch (err) {
    console.error('Error fetching purchase history:', err)
    error.value = 'Failed to load purchase history. Please try again later.'
  } finally {
    loading.value = false
  }
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-PH', {
    style: 'currency',
    currency: 'PHP'
  }).format(value)
}

onMounted(fetchHistory)
</script>
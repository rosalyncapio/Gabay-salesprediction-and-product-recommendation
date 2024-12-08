<template>
  <div class="history-container">
    <div v-if="loading" class="loading-state">
      <div class="animate-spin"></div>
      <p class="loading-text">Loading sales history...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Total Sales</th>
            <th>Insecticides Sales</th>
            <th>Fertilizers Sales</th>
            <th>Herbicides Sales</th>
            <th>Promo Active</th>
            <th>Holiday Season</th>
            <th>Economic Indicator</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sale in salesHistory" :key="sale.id">
            <td>{{ formatDate(sale.month, sale.year) }}</td>
            <td>{{ formatCurrency(sale.total_sales) }}</td>
            <td>{{ formatCurrency(sale.insecticides_sales) }}</td>
            <td>{{ formatCurrency(sale.fertilizers_sales) }}</td>
            <td>{{ formatCurrency(sale.herbicides_sales) }}</td>
            <td>
              <span :class="sale.promo_active ? 'badge-success' : 'badge-danger'">
                {{ sale.promo_active ? 'Yes' : 'No' }}
              </span>
            </td>
            <td>
              <span :class="sale.holiday_season ? 'badge-success' : 'badge-danger'">
                {{ sale.holiday_season ? 'Yes' : 'No' }}
              </span>
            </td>
            <td>{{ formatNumber(sale.economic_indicator) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import { XCircleIcon } from 'lucide-vue-next';
import { getSalesHistory } from '@/services/api';

const salesHistory = ref([]);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const response = await getSalesHistory();
    salesHistory.value = response.data;
  } catch (err) {
    error.value = 'Failed to load sales history. Please try again later.';
    console.error('Error fetching sales history:', err);
  } finally {
    loading.value = false;
  }
});

const formatDate = (month, year) => {
  const date = new Date(year, month - 1);
  return date.toLocaleString('en-US', { month: 'long', year: 'numeric' });
};

const formatCurrency = (value) => {
  if (value === null || value === undefined) return 'N/A';
  return new Intl.NumberFormat('en-PH', {
    style: 'currency',
    currency: 'PHP'
  }).format(value);
};

const formatNumber = (value) => {
  if (value === null || value === undefined) return 'N/A';
  return new Intl.NumberFormat('en-PH', {
    maximumFractionDigits: 2
  }).format(value);
};
</script>


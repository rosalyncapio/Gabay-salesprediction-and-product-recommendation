<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h2 class="text-3xl font-bold text-gray-900 mb-8">Sales Prediction</h2>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
        <p class="mt-4 text-gray-500">Loading predictions...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="rounded-md bg-red-50 p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <XCircleIcon class="h-5 w-5 text-red-400" />
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">Error loading predictions</h3>
            <div class="mt-2 text-sm text-red-700">{{ error }}</div>
          </div>
        </div>
      </div>

      <!-- Prediction Content -->
      <div v-else class="space-y-8">
        <!-- Monthly Prediction Card -->
        <div class="bg-white overflow-hidden shadow-lg rounded-lg">
          <div class="px-6 py-8">
            <div class="text-sm font-medium text-gray-500 uppercase tracking-wide">Next Month's Predicted Sales</div>
            <div class="mt-2 text-4xl font-extrabold text-gray-900">
              {{ formatCurrency(predictions.monthly) }}
            </div>
          </div>
        </div>

        <!-- Sales Prediction Chart -->
        <div class="bg-white overflow-hidden shadow-lg rounded-lg">
          <div class="px-6 py-8">
            <h3 class="text-xl font-semibold text-gray-900 mb-6">12-Month Sales Forecast</h3>
            <SalesPredictionChart :chartData="chartData" />
          </div>
        </div>

        <!-- Yearly Predictions Table -->
        <div class="bg-white overflow-hidden shadow-lg rounded-lg">
          <div class="px-6 py-8">
            <h3 class="text-xl font-semibold text-gray-900 mb-6">12-Month Forecast Details</h3>
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Year
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Month
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Predicted Sales
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="prediction in predictions.yearly" :key="`${prediction.year}-${prediction.month}`" class="hover:bg-gray-50 transition-colors duration-200">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {{ prediction.year }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ getMonthName(prediction.month) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {{ formatCurrency(prediction.predicted_sales) }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { XCircleIcon } from 'lucide-vue-next';
import { getSalesPrediction } from '../../services/api';
import SalesPredictionChart from './SalesPredictionChart.vue';

const predictions = ref({
  monthly: 0,
  yearly: []
});
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const response = await getSalesPrediction();
    predictions.value = response.data;
  } catch (err) {
    error.value = 'Failed to load predictions. Please try again later.';
    console.error('Error fetching predictions:', err);
  } finally {
    loading.value = false;
  }
});

const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-PH', {
    style: 'currency',
    currency: 'PHP'
  }).format(value);
};

const getMonthName = (monthNumber) => {
  const date = new Date();
  date.setMonth(monthNumber - 1);
  return date.toLocaleString('en-US', { month: 'long' });
};

const chartData = computed(() => {
  return {
    labels: predictions.value.yearly.map(p => `${getMonthName(p.month)} ${p.year}`),
    datasets: [{
      label: 'Predicted Sales',
      data: predictions.value.yearly.map(p => p.predicted_sales),
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      fill: true,
    }]
  };
});
</script>
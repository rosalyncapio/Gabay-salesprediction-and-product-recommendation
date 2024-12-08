<template>
  <div class="dashboard">
    <h1 class="h2 mb-4">Dashboard</h1>
    <div class="row">
      <!-- Sales Prediction -->
      <div class="col-md-6 mb-4">
        <div class="card h-100">
          <div class="card-body">
            <h2 class="card-title h4 mb-4">Sales Prediction</h2>
            <div v-if="loadingSales" class="text-center py-5">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            <div v-else-if="salesError" class="alert alert-danger" role="alert">
              {{ salesError }}
            </div>
            <div v-else>
              <SalesPredictionChart :chartData="salesChartData" />
            </div>
          </div>
        </div>
      </div>

      <!-- Product Recommendations -->
      <div class="col-md-6 mb-4">
        <div class="card h-100">
          <div class="card-body">
            <h2 class="card-title h4 mb-4">Product Recommendations</h2>
            <div v-if="loadingRecommendations" class="text-center py-5">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            <div v-else-if="recommendationsError" class="alert alert-danger" role="alert">
              {{ recommendationsError }}
            </div>
            <div v-else>
              <ProductRecommendationChart :recommendations="recommendations" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Sales Per Category -->
    <div class="row mt-4">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title h4 mb-4">Sales per Category</h2>
            <div v-if="loading" class="text-center py-5">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            <div v-else-if="error" class="alert alert-danger" role="alert">
              {{ error }}
            </div>
            <div v-else>
              <SalesPerCategoryChart :salesData="salesPerCategory" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


  
  <script setup>
  import { ref, onMounted, computed } from 'vue';
  import SalesPredictionChart from '@/views/sales/SalesPredictionChart.vue';
  import ProductRecommendationChart from '@/components/ProductRecommendationChart.vue';
  import SalesPerCategoryChart from '@/components/SalesPerCategoryChart.vue';
  import { getSalesPrediction, getRecommendations, getPurchaseHistory } from '@/services/api';
  
  // State variables
  const loadingSales = ref(true);
  const loadingRecommendations = ref(true);
  const loading = ref(true); // Generic loading for sales per category
  const salesError = ref(null);
  const recommendationsError = ref(null);
  const error = ref(null); // Error for sales per category
  const salesPredictions = ref({ yearly: [] });
  const recommendations = ref({});
  const salesPerCategory = ref({});
  
  // Computed sales chart data
  const salesChartData = computed(() => ({
    labels: salesPredictions.value.yearly.map(p => `${getMonthName(p.month)} ${p.year}`),
    datasets: [
      {
        label: 'Predicted Sales',
        data: salesPredictions.value.yearly.map(p => p.predicted_sales),
        borderColor: '#4e73df',
        backgroundColor: 'rgba(78, 115, 223, 0.1)',
        fill: true,
      }
    ],
  }));
  
  // Utility function to get month names
  const getMonthName = (monthNumber) => {
    const date = new Date();
    date.setMonth(monthNumber - 1);
    return date.toLocaleString('en-US', { month: 'short' });
  };
  
  // Fetch sales predictions
  const fetchSalesPredictions = async () => {
    try {
      loadingSales.value = true;
      salesError.value = null;
      const response = await getSalesPrediction();
      salesPredictions.value = response.data;
    } catch (err) {
      console.error('Error fetching sales predictions:', err);
      salesError.value = 'Failed to load sales predictions. Please try again later.';
    } finally {
      loadingSales.value = false;
    }
  };
  
  // Fetch product recommendations
  const fetchRecommendations = async () => {
    try {
      loadingRecommendations.value = true;
      recommendationsError.value = null;
      const response = await getRecommendations();
      if (response.data && response.data.category_recommendations) {
        recommendations.value = response.data.category_recommendations;
      } else {
        throw new Error('No recommendation data received from API');
      }
    } catch (err) {
      console.error('Error fetching recommendations:', err);
      recommendationsError.value = 'Failed to load recommendations. Please try again later.';
    } finally {
      loadingRecommendations.value = false;
    }
  };
  
  // Fetch purchase history and aggregate sales per category
  const fetchHistory = async () => {
    try {
      const response = await getPurchaseHistory();
      const history = response.data;
  
      // Aggregate sales per category
      salesPerCategory.value = history.reduce((acc, purchase) => {
        const category = purchase.category;
        const total = purchase.quantity * purchase.unit_price;
        acc[category] = (acc[category] || 0) + total;
        return acc;
      }, {});
    } catch (err) {
      console.error('Error fetching purchase history:', err);
      error.value = 'Failed to load sales per category. Please try again later.';
    } finally {
      loading.value = false;
    }
  };
  
  // Fetch data on mount
  onMounted(() => {
    fetchSalesPredictions();
    fetchRecommendations();
    fetchHistory(); // Handles sales per category
  });
  </script>
  
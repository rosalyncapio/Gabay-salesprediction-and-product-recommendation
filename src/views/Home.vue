<template>
  <div class="home">
    <section class="hero bg-light py-5">
      <div class="container">
        <h1 class="display-4">Welcome to <span class="text-primary">CAPIO</span></h1>
        <p class="lead">Your comprehensive sales prediction and product recommendation system</p>
      </div>
    </section>

    <div class="container mt-5">
      <div class="row">
        <div class="col-md-6 mb-4">
          <div class="card h-100">
            <div class="card-body">
              <h2 class="card-title">
                <ShoppingBagIcon class="icon text-primary" />
                Products
              </h2>
              <p class="card-text">Manage your product inventory, view purchase history, and get product recommendations.</p>
              <router-link to="/products" class="btn btn-primary">Go to Products</router-link>
            </div>
          </div>
        </div>
        <div class="col-md-6 mb-4">
          <div class="card h-100">
            <div class="card-body">
              <h2 class="card-title">
                <TrendingUpIcon class="icon text-success" />
                Sales
              </h2>
              <p class="card-text">Record sales data, view sales history, and get sales predictions.</p>
              <router-link to="/sales" class="btn btn-success">Go to Sales</router-link>
            </div>
          </div>
        </div>
      </div>

      <div class="row mt-5">
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

      <section class="mt-5">
        <h3 class="text-center mb-4">Why Choose CAPIO?</h3>
        <div class="row">
          <div class="col-md-4 mb-4">
            <div class="card text-center h-100">
              <div class="card-body">
                <ChartBarIcon class="icon text-primary mb-3" />
                <h4 class="card-title">Data-Driven Insights</h4>
                <p class="card-text">Make informed decisions with our advanced analytics</p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-4">
            <div class="card text-center h-100">
              <div class="card-body">
                <LightbulbIcon class="icon text-warning mb-3" />
                <h4 class="card-title">Smart Recommendations</h4>
                <p class="card-text">Get personalized product suggestions to boost sales</p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-4">
            <div class="card text-center h-100">
              <div class="card-body">
                <TrendingUpIcon class="icon text-success mb-3" />
                <h4 class="card-title">Sales Forecasting</h4>
                <p class="card-text">Predict future sales trends with machine learning</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { ShoppingBagIcon, TrendingUpIcon, ChartBarIcon, LightbulbIcon } from 'lucide-vue-next';
import SalesPredictionChart from '@/views/sales/SalesPredictionChart.vue';
import ProductRecommendationChart from '@/components/ProductRecommendationChart.vue';
import { getSalesPrediction, getRecommendations } from '@/services/api';

const loadingSales = ref(true);
const loadingRecommendations = ref(true);
const salesError = ref(null);
const recommendationsError = ref(null);
const salesPredictions = ref({ yearly: [] });
const recommendations = ref({});

const salesChartData = computed(() => ({
  labels: salesPredictions.value.yearly.map(p => `${getMonthName(p.month)} ${p.year}`),
  datasets: [{
    label: 'Predicted Sales',
    data: salesPredictions.value.yearly.map(p => p.predicted_sales),
    borderColor: '#4e73df',
    backgroundColor: 'rgba(78, 115, 223, 0.1)',
    fill: true,
  }]
}));

const getMonthName = (monthNumber) => {
  const date = new Date();
  date.setMonth(monthNumber - 1);
  return date.toLocaleString('en-US', { month: 'short' });
};

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

onMounted(() => {
  fetchSalesPredictions();
  fetchRecommendations();
});
</script>

<style scoped>
.icon {
  width: 2rem;
  height: 2rem;
}

.card {
  transition: all 0.3s ease-in-out;
  border: none;
  border-radius: 0.5rem;
}

.card:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.hero {
  background-color: #f8f9fa;
}

.display-4 {
  font-size: 2.5rem;
  font-weight: 300;
  line-height: 1.2;
}

.lead {
  font-size: 1.25rem;
  font-weight: 300;
}

@media (min-width: 768px) {
  .display-4 {
    font-size: 3.5rem;
  }
}
</style>


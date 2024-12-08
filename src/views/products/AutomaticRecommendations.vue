<template>
  <div class="automatic-recommendations">
    <div class="card shadow-sm">
      <div class="card-body">
        <h2 class="card-title text-2xl font-bold text-primary mb-4">Product Recommendations</h2>
        
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="mt-4 text-gray-500">Loading recommendations...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="alert alert-danger" role="alert">
          {{ error }}
        </div>

        <!-- Empty State -->
        <div v-else-if="isEmpty" class="alert alert-info" role="alert">
          No recommendations available at this time.
        </div>

        <!-- Content -->
        <div v-else>
          <div class="row mb-4">
            <div class="col-md-6">
              <div class="chart-container" style="position: relative; height:40vh; width:100%">
                <Bar :data="chartData" :options="chartOptions" />
              </div>
            </div>
            <div class="col-md-6">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Category</th>
                      <th>Product</th>
                      <th>Quantity Sold</th>
                      <th>Price</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(product, category) in categoryRecommendations" :key="category">
                      <td>{{ category }}</td>
                      <td>{{ product.name }}</td>
                      <td>{{ product.quantity_sold }}</td>
                      <td>{{ formatCurrency(product.price) }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getRecommendations } from '@/services/api'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const loading = ref(true)
const error = ref(null)
const categoryRecommendations = ref({})

const isEmpty = computed(() => Object.keys(categoryRecommendations.value).length === 0)

const chartData = computed(() => ({
  labels: Object.keys(categoryRecommendations.value),
  datasets: [
    {
      label: 'Quantity Sold',
      backgroundColor: '#4e73df',
      data: Object.values(categoryRecommendations.value).map(product => product.quantity_sold)
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Quantity Sold'
      }
    },
    x: {
      title: {
        display: true,
        text: 'Category'
      }
    }
  },
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          let label = context.dataset.label || '';
          if (label) {
            label += ': ';
          }
          if (context.parsed.y !== null) {
            label += context.parsed.y;
          }
          return label;
        }
      }
    }
  }
}

const fetchRecommendations = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await getRecommendations()
    if (response.data && response.data.category_recommendations) {
      categoryRecommendations.value = response.data.category_recommendations
    } else {
      throw new Error('No recommendation data received from API')
    }
  } catch (err) {
    console.error('Error fetching recommendations:', err)
    error.value = 'Failed to load recommendations. Please try again later.'
  } finally {
    loading.value = false
  }
}

const formatCurrency = (value) => {
  if (value == null) return 'N/A'
  return new Intl.NumberFormat('en-PH', {
    style: 'currency',
    currency: 'PHP'
  }).format(value)
}

onMounted(() => {
  fetchRecommendations()
})
</script>

<style scoped>
.card {
  border-radius: 0.5rem;
  transition: all 0.3s ease-in-out;
}

.card:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.table {
  font-size: 0.9rem;
}

.table th {
  font-weight: 600;
  text-transform: uppercase;
}

.chart-container {
  margin-bottom: 1rem;
}

@media (min-width: 768px) {
  .chart-container {
    margin-bottom: 0;
  }
}
</style>


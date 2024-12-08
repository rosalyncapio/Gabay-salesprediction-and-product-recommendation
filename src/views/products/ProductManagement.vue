<template>
    <div class="product-management">
      <h1 class="page-title">Product Management</h1>
  
      <!-- Product Recommendations -->
      <section class="recommendations mb-8">
        <h2 class="section-title">Product Recommendations</h2>
        <div v-if="loadingRecommendations" class="text-center py-5">
          <div class="spinner"></div>
          <p class="mt-3">Loading recommendations...</p>
        </div>
        <div v-else-if="recommendationsError" class="alert alert-danger" role="alert">
          {{ recommendationsError }}
        </div>
        <div v-else-if="isEmpty" class="text-center py-5">
          <p>No recommendations available at this time.</p>
        </div>
        <div v-else class="card-grid">
          <div v-for="product in topRecommendations" :key="product.name" class="card">
            <div class="card-body">
              <h3 class="card-title">{{ product.name }}</h3>
              <p class="card-text">Quantity Sold: {{ product.quantity_sold || product.total_sold }}</p>
              <p class="card-text">Price: {{ formatCurrency(product.price) }}</p>
            </div>
          </div>
        </div>
      </section>
  
      <!-- New Purchase Button and Form -->
      <section class="new-purchase mb-8">
        <button @click="togglePurchaseForm" class="btn btn-primary mb-4">
          {{ showPurchaseForm ? 'Hide Purchase Form' : 'Add New Purchase' }}
        </button>
        <div v-if="showPurchaseForm" class="purchase-form card">
          <div class="card-body">
            <h2 class="card-title">New Purchase</h2>
            <form @submit.prevent="submitPurchase">
              <div class="form-group">
                <label for="item_name">Item Name</label>
                <input v-model="purchaseForm.item_name" type="text" id="item_name" class="form-control" required>
              </div>
              <div class="form-group">
                <label for="category">Category</label>
                <input v-model="purchaseForm.category" type="text" id="category" class="form-control" required>
              </div>
              <div class="form-group">
                <label for="quantity">Quantity</label>
                <input v-model.number="purchaseForm.quantity" type="number" id="quantity" class="form-control" min="1" required>
              </div>
              <div class="form-group">
                <label for="unit_price">Unit Price (₱)</label>
                <input v-model.number="purchaseForm.unit_price" type="number" id="unit_price" class="form-control" step="0.01" min="0" required>
              </div>
              <button type="submit" class="btn btn-success" :disabled="submittingPurchase">
                {{ submittingPurchase ? 'Submitting...' : 'Submit Purchase' }}
              </button>
            </form>
          </div>
        </div>
      </section>
  
      <!-- Purchase History -->
      <section class="purchase-history">
        <h2 class="section-title">Purchase History</h2>
        <div v-if="loadingHistory" class="text-center py-5">
          <div class="spinner"></div>
          <p class="mt-3">Loading purchase history...</p>
        </div>
        <div v-else-if="historyError" class="alert alert-danger" role="alert">
          {{ historyError }}
        </div>
        <div v-else class="table-responsive">
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>Date</th>
                <th>Item</th>
                <th>Category</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="purchase in purchaseHistory" :key="purchase.id">
                <td>{{ formatDate(purchase.date) }}</td>
                <td>{{ purchase.item_name }}</td>
                <td>{{ purchase.category }}</td>
                <td>{{ purchase.quantity }}</td>
                <td>{{ formatCurrency(purchase.unit_price) }}</td>
                <td>{{ formatCurrency(purchase.quantity * purchase.unit_price) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import { getRecommendations, submitPurchase, getPurchaseHistory } from '@/services/api'
  
  // Recommendations
  const recommendations = ref({
    category_recommendations: {},
    most_popular_products: [],
    price_ranges: {}
  })
  const loadingRecommendations = ref(true)
  const recommendationsError = ref(null)
  
  const topRecommendations = computed(() => {
    const allProducts = [
      ...Object.values(recommendations.value.category_recommendations).flat(),
      ...recommendations.value.most_popular_products,
      ...Object.values(recommendations.value.price_ranges).flat()
    ]
    return [...new Set(allProducts)].slice(0, 6) // Get unique products, limit to 6
  })
  
  const isEmpty = computed(() => topRecommendations.value.length === 0)
  
  // Purchase Form
  const showPurchaseForm = ref(false)
  const purchaseForm = ref({
    item_name: '',
    category: '',
    quantity: 1,
    unit_price: 0
  })
  const submittingPurchase = ref(false)
  
  // Purchase History
  const purchaseHistory = ref([])
  const loadingHistory = ref(true)
  const historyError = ref(null)
  
  // Fetch data
  const fetchRecommendations = async () => {
    try {
      loadingRecommendations.value = true
      const response = await getRecommendations()
      recommendations.value = response.data
    } catch (err) {
      console.error('Error fetching recommendations:', err)
      recommendationsError.value = 'Failed to load recommendations. Please try again later.'
    } finally {
      loadingRecommendations.value = false
    }
  }
  
  const fetchPurchaseHistory = async () => {
    try {
      loadingHistory.value = true
      const response = await getPurchaseHistory()
      purchaseHistory.value = response.data
    } catch (err) {
      console.error('Error fetching purchase history:', err)
      historyError.value = 'Failed to load purchase history. Please try again later.'
    } finally {
      loadingHistory.value = false
    }
  }
  
  // Form actions
  const togglePurchaseForm = () => {
    showPurchaseForm.value = !showPurchaseForm.value
  }
  
  const submitPurchase = async () => {
    submittingPurchase.value = true
    try {
      await submitPurchase(purchaseForm.value)
      purchaseForm.value = { item_name: '', category: '', quantity: 1, unit_price: 0 }
      showPurchaseForm.value = false
      await fetchPurchaseHistory() // Refresh the purchase history
    } catch (error) {
      console.error('Error submitting purchase:', error)
      alert('Failed to submit purchase. Please try again.')
    } finally {
      submittingPurchase.value = false
    }
  }
  
  // Utility functions
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-PH', {
      style: 'currency',
      currency: 'PHP'
    }).format(value)
  }
  
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }
  
  // Lifecycle hooks
  onMounted(() => {
    fetchRecommendations()
    fetchPurchaseHistory()
  })
  </script>
  
  <style scoped>
  .product-management {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }
  
  .page-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--primary-color);
    text-align: center;
    margin-bottom: 2rem;
  }
  
  .section-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1rem;
  }
  
  .card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
  }
  
  .card {
    background-color: #ffffff;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
  }
  
  .card:hover {
    transform: translateY(-5px);
  }
  
  .card-body {
    padding: 1rem;
  }
  
  .card-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
  }
  
  .card-text {
    font-size: 0.875rem;
    color: #666;
  }
  
  .btn {
    display: inline-block;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    font-weight: 500;
    text-align: center;
    text-decoration: none;
    border-radius: 0.25rem;
    transition: background-color 0.3s ease;
    cursor: pointer;
  }
  
  .btn-primary {
    background-color: var(--primary-color);
    color: #ffffff;
  }
  
  .btn-success {
    background-color: var(--primary-green);
    color: #ffffff;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  .form-control {
    display: block;
    width: 100%;
    padding: 0.5rem;
    font-size: 1rem;
    line-height: 1.5;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
  }
  
  .table {
    width: 100%;
    margin-bottom: 1rem;
    background-color: transparent;
    border-collapse: collapse;
  }
  
  .table th,
  .table td {
    padding: 0.75rem;
    vertical-align: top;
    border-top: 1px solid #dee2e6;
  }
  
  .table-striped tbody tr:nth-of-type(odd) {
    background-color: rgba(0, 0, 0, 0.05);
  }
  
  .table-hover tbody tr:hover {
    background-color: rgba(0, 0, 0, 0.075);
  }
  
  .spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid var(--primary-color);
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 0 auto;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  @media (max-width: 768px) {
    .card-grid {
      grid-template-columns: 1fr;
    }
  }
  </style>
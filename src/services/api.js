import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Products API endpoints
export const getProducts = () => api.get('/products/')
export const submitPurchase = (data) => api.post('/products/purchase/', data)
export const getPurchaseHistory = () => api.get('/products/history/')
export const getRecommendations = () => {
  console.log('Fetching recommendations...')
  return api.get('/products/recommendations/')
    .then(response => {
      console.log('Recommendations response:', response.data)
      return response
    })
    .catch(error => {
      console.error('Error fetching recommendations:', error.response || error)
      throw error
    })
}

// Sales API endpoints
export const submitSales = (data) => api.post('/sales/submit/', data)
export const getSalesHistory = () => api.get('/sales/history/')
export const getSalesPrediction = () => api.get('/sales/predict/')
export const getSalesPerCategory = () => api.get('/sales/per-category/')

// ML Prediction endpoints
export const getMachineLearningPrediction = () => api.get('/prediction/sales/')
export const getMachineLearningRecommendations = (userId) => 
  api.get('/prediction/products/', { params: { user_id: userId } })

// Error handling interceptor
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error)
    if (error.response) {
      console.error('Response data:', error.response.data)
      console.error('Response status:', error.response.status)
      console.error('Response headers:', error.response.headers)
    } else if (error.request) {
      console.error('No response received:', error.request)
    } else {
      console.error('Error setting up request:', error.message)
    }
    return Promise.reject(error)
  }
)

export default api


<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-md mx-auto bg-white shadow-lg rounded-lg overflow-hidden">
      <div class="px-6 py-8">
        <h2 class="text-3xl font-extrabold text-gray-900 text-center mb-6">Add New Sales Data</h2>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Insecticides Sales Input -->
          <div>
            <label for="insecticides_sales" class="block text-sm font-medium text-gray-700">
              Insecticides Sales
            </label>
            <div class="mt-1 relative rounded-md shadow-sm">
              <input id="insecticides_sales" v-model.number="formData.insecticides_sales" type="number" step="0.01"
                required class="input-base" />
            </div>
          </div>

          <!-- Fertilizers Sales Input -->
          <div>
            <label for="fertilizers_sales" class="block text-sm font-medium text-gray-700">
              Fertilizers Sales
            </label>
            <div class="mt-1 relative rounded-md shadow-sm">
              <input id="fertilizers_sales" v-model.number="formData.fertilizers_sales" type="number" step="0.01"
                required class="input-base" />
            </div>
          </div>

          <!-- Herbicides Sales Input -->
          <div>
            <label for="herbicides_sales" class="block text-sm font-medium text-gray-700">
              Herbicides Sales
            </label>
            <div class="mt-1 relative rounded-md shadow-sm">
              <input id="herbicides_sales" v-model.number="formData.herbicides_sales" type="number" step="0.01" required
                class="input-base" />
            </div>
          </div>

          <!-- Total Sales (Computed) -->
          <div>
            <label for="total_sales" class="block text-sm font-medium text-gray-700">
              Total Sales (PHP)
            </label>
            <div class="mt-1 relative rounded-md shadow-sm">
              <input id="total_sales" :value="totalSales" type="number" readonly
                class="input-base bg-gray-100 cursor-not-allowed" />
            </div>
          </div>

          <!-- Checkbox Group -->
        

            <div class="flex flex-col space-y-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Additional Options
              </label>
              <div class="flex items-center space-x-2">
                <input id="promo_active" v-model="formData.promo_active" type="checkbox" class="checkbox-base" />
                <label for="promo_active" class="text-sm font-medium text-gray-700">
                  Promo Active
                </label>
              </div>
              <div class="flex items-center space-x-2">
                <input id="holiday_season" v-model="formData.holiday_season" type="checkbox" class="checkbox-base" />
                <label for="holiday_season" class="text-sm font-medium text-gray-700">
                  Holiday Season
                </label>
              </div>
            </div>


            <!-- Economic Indicator Input -->
            <div>
              <label for="economic_indicator" class="block text-sm font-medium text-gray-700">
                Economic Indicator
              </label>
              <div class="mt-1 relative rounded-md shadow-sm">
                <input id="economic_indicator" v-model.number="formData.economic_indicator" type="number" step="0.01"
                  required class="input-base" />
              </div>
            </div>

            <!-- Year Input -->
            <div>
              <label for="year" class="block text-sm font-medium text-gray-700">
                Year
              </label>
              <div class="mt-1 relative rounded-md shadow-sm">
                <input id="year" v-model.number="formData.year" type="number" required min="2000" max="2100"
                  class="input-base" />
              </div>
            </div>

            <!-- Month Input -->
            <div>
              <label for="month" class="block text-sm font-medium text-gray-700">
                Month
              </label>
              <div class="mt-1 relative rounded-md shadow-sm">
                <select id="month" v-model="formData.month" required class="input-base">
                  <option v-for="i in 12" :key="i" :value="i">
                    {{ getMonthName(i) }}
                  </option>
                </select>
              </div>
            </div>

            <!-- Submit Button -->
            <div>
              <button type="submit" :disabled="loading" class="btn-primary">
                {{ loading ? 'Submitting...' : 'Submit Sales Data' }}
              </button>
            </div>
        </form>

        <!-- Alert Messages -->
        <div v-if="message" class="mt-4">
          <div :class="[success ? 'alert-success' : 'alert-error']">
            {{ message }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<script setup>
import { ref, reactive, computed } from 'vue';
import { submitSales } from '@/services/api';
import { defineEmits } from 'vue';

const emit = defineEmits(['sales-added']);

const formData = reactive({
  insecticides_sales: 0,
  fertilizers_sales: 0,
  herbicides_sales: 0,
  promo_active: false,
  holiday_season: false,
  economic_indicator: 0,
  year: new Date().getFullYear(),
  month: new Date().getMonth() + 1
});

const totalSales = computed(() => {
  return formData.insecticides_sales + formData.fertilizers_sales + formData.herbicides_sales;
});

const loading = ref(false);
const message = ref('');
const success = ref(false);

const getMonthName = (monthNumber) => {
  const date = new Date();
  date.setMonth(monthNumber - 1);
  return date.toLocaleString('en-US', { month: 'long' });
};

const handleSubmit = async () => {
  loading.value = true;
  message.value = '';

  try {
    const salesData = {
      ...formData,
      total_sales: totalSales.value,
      timestamp: new Date().toISOString()
    };
    await submitSales(salesData);
    success.value = true;
    message.value = 'Sales data submitted successfully!';
    emit('sales-added');

    // Reset form
    Object.assign(formData, {
      insecticides_sales: 0,
      fertilizers_sales: 0,
      herbicides_sales: 0,
      promo_active: false,
      holiday_season: false,
      economic_indicator: 0,
      year: new Date().getFullYear(),
      month: new Date().getMonth() + 1
    });
  } catch (error) {
    success.value = false;
    message.value = error.response?.data?.error || 'Failed to submit sales data. Please try again.';
  } finally {
    loading.value = false;
  }
};
</script>
<style scoped>
/* Common input styling */
.input-base {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background-color: #fff;
  transition: all 0.2s ease-in-out;
  font-size: 0.875rem;
  font-family: inherit;
}

.input-base:focus {
  border-color: #2563eb;
  outline: none;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.5);
}

/* Checkbox styling */
.checkbox-base {
  height: 1.25rem;
  width: 1.25rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  transition: all 0.2s ease-in-out;
  appearance: none;
}

.checkbox-base:checked {
  background-color: #2563eb;
  border-color: #2563eb;
}

/* Button styles */
.btn-primary {
  display: inline-block;
  width: 100%;
  padding: 0.75rem 1rem;
  text-align: center;
  background-color: #2563eb;
  color: #fff;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.btn-primary:hover {
  background-color: #1e40af;
}

.btn-primary:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}

/* Alert styles */
.alert-success {
  background-color: #d1fae5;
  color: #065f46;
  padding: 0.75rem;
  border-radius: 0.375rem;
}

.alert-error {
  background-color: #fee2e2;
  color: #b91c1c;
  padding: 0.75rem;
  border-radius: 0.375rem;
}
</style>

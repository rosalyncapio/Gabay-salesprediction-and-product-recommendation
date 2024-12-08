<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-md mx-auto bg-white shadow-md rounded-lg overflow-hidden">
      <div class="px-4 py-5 sm:p-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">New Purchase</h2>
        
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Item Name Input -->
          <div>
            <label for="item_name" class="block text-sm font-medium text-gray-700">
              Item Name
            </label>
            <div class="mt-1">
              <input
                id="item_name"
                v-model="formData.item_name"
                type="text"
                required
                class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
              />
            </div>
          </div>

          <!-- Category Input -->
          <div>
            <label for="category" class="block text-sm font-medium text-gray-700">
              Category
            </label>
            <div class="mt-1">
              <input
                id="category"
                v-model="formData.category"
                type="text"
                required
                class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
              />
            </div>
          </div>

          <!-- Quantity Input -->
          <div>
            <label for="quantity" class="block text-sm font-medium text-gray-700">
              Quantity
            </label>
            <div class="mt-1">
              <input
                id="quantity"
                v-model.number="formData.quantity"
                type="number"
                min="1"
                required
                class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
              />
            </div>
          </div>

          <!-- Unit Price Input -->
          <div>
            <label for="unit_price" class="block text-sm font-medium text-gray-700">
              Unit Price (₱)
            </label>
            <div class="mt-1">
              <input
                id="unit_price"
                v-model.number="formData.unit_price"
                type="number"
                step="0.01"
                min="0"
                required
                class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
              />
            </div>
          </div>

          <!-- Submit Button -->
          <div>
            <button
              type="submit"
              :disabled="loading"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {{ loading ? 'Submitting...' : 'Submit Purchase' }}
            </button>
          </div>
        </form>

        <!-- Alert Messages -->
        <div v-if="message" class="mt-4">
          <div
            :class="[
              'rounded-md p-4',
              success ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
            ]"
          >
            {{ message }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { submitPurchase } from '@/services/api';
import { defineEmits } from 'vue';


const emit = defineEmits(['purchase-added']);

const formData = reactive({
  item_name: '',
  category: '',
  quantity: 1,
  unit_price: 0
});

const loading = ref(false);
const message = ref('');
const success = ref(false);

const handleSubmit = async () => {
  loading.value = true;
  message.value = '';

  try {

    await submitPurchase(formData);
    success.value = true;
    message.value = 'Purchase submitted successfully!';
    emit('purchase-added');
    
    Object.assign(formData, {
      item_name: '',
      category: '',
      quantity: 1,
      unit_price: 0
    });


  } catch (error) {
    success.value = false;
    message.value = error.response?.data?.error || 'Failed to submit purchase. Please try again.';
  } finally {
    loading.value = false;
  }
};
</script>


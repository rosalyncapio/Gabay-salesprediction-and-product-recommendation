<template>
    <div class="chart-container">
      <Bar :data="chartData" :options="chartOptions" />
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue';
  import { Bar } from 'vue-chartjs';
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
  
  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);
  
  const props = defineProps({
    recommendations: {
      type: Object,
      required: true
    }
  });
  
  const chartData = computed(() => ({
    labels: Object.keys(props.recommendations),
    datasets: [
      {
        label: 'Quantity Sold',
        backgroundColor: '#4e73df',
        data: Object.values(props.recommendations).map(product => product.quantity_sold)
      }
    ]
  }));
  
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
  };
  </script>
  
  <style scoped>
  .chart-container {
    position: relative;
    height: 300px;
    width: 100%;
  }
  </style>
  
  
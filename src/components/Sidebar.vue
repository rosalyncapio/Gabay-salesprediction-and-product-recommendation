<template>
    <div class="sidebar bg-light border-right">
      <div class="sidebar-sticky">
        <ul class="nav flex-column">
          <li class="nav-item">
            <router-link to="/" class="nav-link" active-class="active">
              <HomeIcon class="feather mr-2" />
              Dashboard
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/products" class="nav-link" active-class="active">
              <ShoppingBagIcon class="feather mr-2" />
              Product Management
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/sales" class="nav-link" active-class="active">
              <TrendingUpIcon class="feather mr-2" />
              Sales Management
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script setup>
  import { HomeIcon, ShoppingBagIcon, TrendingUpIcon } from 'lucide-vue-next';
  </script>
  
  <style scoped>
  .sidebar {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    z-index: 100;
    padding: 48px 0 0;
    box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1);
    width: 250px;
  }
  
  .sidebar-sticky {
    position: relative;
    top: 0;
    height: calc(100vh - 48px);
    padding-top: .5rem;
    overflow-x: hidden;
    overflow-y: auto;
  }
  
  .nav-link {
    font-weight: 500;
    color: #333;
  }
  
  .nav-link.active {
    color: #007bff;
  }
  
  .feather {
    width: 16px;
    height: 16px;
    vertical-align: text-bottom;
  }
  </style>
  
  
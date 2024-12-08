from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_products, name='get_products'),
    path('purchase/', views.submit_purchase, name='submit_purchase'),
    path('history/', views.purchase_history, name='purchase_history'),
    path('recommendations/', views.product_recommendations, name='product_recommendations'),
]


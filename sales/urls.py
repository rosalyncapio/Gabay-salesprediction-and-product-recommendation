from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_sales, name='submit_sales'),
    path('history/', views.sales_history, name='sales_history'),
    path('predict/', views.sales_prediction, name='sales_prediction'),
]


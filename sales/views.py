from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Sale
from .serializers import SaleSerializer
from datetime import datetime, timedelta
import random

@api_view(['POST'])
def submit_sales(request):
    serializer = SaleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def sales_history(request):
    sales = Sale.objects.all().order_by('-date')
    serializer = SaleSerializer(sales, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def sales_prediction(request):
    # This is a placeholder. In a real-world scenario, you'd implement a prediction algorithm here.
    last_sale = Sale.objects.latest('date')
    
    # Generate dummy predictions
    monthly_prediction = last_sale.total_sales * random.uniform(0.9, 1.1)
    
    yearly_predictions = []
    for i in range(1, 13):
        prediction_date = last_sale.date + timedelta(days=30*i)
        prediction = {
            'year': prediction_date.year,
            'month': prediction_date.month,
            'predicted_sales': last_sale.total_sales * random.uniform(0.8, 1.2)
        }
        yearly_predictions.append(prediction)
    
    return Response({
        'monthly': monthly_prediction,
        'yearly': yearly_predictions
    })


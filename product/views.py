from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Purchase
from .serializers import ProductSerializer, PurchaseSerializer, PurchaseCreateSerializer
from datetime import datetime
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@api_view(['POST'])
def submit_purchase(request):
    serializer = PurchaseCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def purchase_history(request):
    purchases = Purchase.objects.all().order_by('-date')
    serializer = PurchaseSerializer(purchases, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_recommendations(request):
    logger.debug("product_recommendations view called")
    try:
        # Get all purchases
        purchases = Purchase.get_all()
        
        # Initialize category-based recommendations
        category_recommendations = defaultdict(list)
        product_stats = defaultdict(lambda: {'quantity': 0, 'revenue': 0})
        
        # Process purchase data
        for purchase in purchases:
            # Update product stats
            product_stats[purchase.item_name]['quantity'] += purchase.quantity
            product_stats[purchase.item_name]['revenue'] += (purchase.quantity * purchase.unit_price)
            
            # Add to category recommendations
            category_recommendations[purchase.category].append({
                'name': purchase.item_name,
                'quantity': purchase.quantity,
                'price': purchase.unit_price
            })

        # Prepare response data
        response_data = {
            # Category-based recommendations
            'category_recommendations': {},
            
            # Most popular products
            'most_popular_products': [],
            
            # Price range products
            'price_ranges': {
                'P0-500': [],
                'P501-1000': [],
                'P1000+': []
            }
        }

        # Process category recommendations
        for category, products in category_recommendations.items():
            # Group by product name and sum quantities
            product_summary = defaultdict(lambda: {'quantity': 0, 'price': 0})
            for product in products:
                product_summary[product['name']]['quantity'] += product['quantity']
                product_summary[product['name']]['price'] = product['price']
            
            # Convert to list and sort by quantity
            response_data['category_recommendations'][category] = [
                {
                    'name': name,
                    'quantity_sold': stats['quantity'],
                    'price': stats['price']
                }
                for name, stats in product_summary.items()
            ]

        # Process most popular products
        sorted_products = sorted(
            product_stats.items(),
            key=lambda x: x[1]['quantity'],
            reverse=True
        )
        response_data['most_popular_products'] = [
            {
                'name': product_name,
                'total_sold': stats['quantity']
            }
            for product_name, stats in sorted_products
        ]

        # Process price ranges
        for purchase in purchases:
            price = purchase.unit_price
            price_range = 'P0-500' if price <= 500 else 'P501-1000' if price <= 1000 else 'P1000+'
            if purchase.item_name not in [p['name'] for p in response_data['price_ranges'][price_range]]:
                response_data['price_ranges'][price_range].append({
                    'name': purchase.item_name,
                    'price': price
                })

        return Response(response_data)
        
    except Exception as e:
        logger.error(f"Error in product_recommendations: {str(e)}")
        return Response(
            {'error': 'Failed to generate product recommendations'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


from rest_framework import serializers
from .models import Sale

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id', 'date', 'total_sales', 'holiday_season', 'promo_active', 'economic_indicator']


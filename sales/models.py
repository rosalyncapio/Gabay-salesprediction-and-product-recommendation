from django.db import models

class Sale(models.Model):
    date = models.DateField()
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    holiday_season = models.BooleanField(default=False)
    promo_active = models.BooleanField(default=False)
    economic_indicator = models.FloatField()

    def __str__(self):
        return f"Sale on {self.date}: ${self.total_sales}"


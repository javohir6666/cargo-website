from django.db import models
    
class UzTracking(models.Model):
    customer = models.CharField(max_length=255)
    tracking_code = models.CharField(max_length=100)
    weight = models.FloatField()
    quantity = models.PositiveIntegerField()
    flight = models.PositiveIntegerField(null=True, blank=True)
    def __str__(self):  
        return f'{self.tracking_code} - {self.customer}'
    
    
class ShipmentTracking(models.Model):
    customer = models.CharField(max_length=255)
    tracking_code = models.CharField(max_length=255)
    shipping_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    weight = models.FloatField()
    package_number = models.CharField(max_length=255)
    flight = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.tracking_code} - {self.shipping_name}'
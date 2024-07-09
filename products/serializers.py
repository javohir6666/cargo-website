from rest_framework import serializers
from .models import UzTracking, ShipmentTracking
       
class UzTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UzTracking
        fields = '__all__'
        
        
class ShipmentTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentTracking
        fields = '__all__'
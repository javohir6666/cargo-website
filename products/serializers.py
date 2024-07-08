from rest_framework import serializers
from .models import Product, Order
from users.models import AbstractUser


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
        
class AbstractUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractUser
        fields = '__all__'
        
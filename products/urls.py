from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
from .views import import_orders, import_products

router = routers.DefaultRouter()

router.register(r'products', views.ProductList, 'products')
router.register(r'orders', views.OrderList, 'orders')


urlpatterns = [
    path('', include(router.urls)),
    path('import-products/', import_products, name='import-products'),
    path('import-orders/', import_orders, name='import-products'),
]
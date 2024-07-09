from django.urls import path, include
from rest_framework import routers
from . import views
from .views import import_shipments,import_uztracking

router = routers.DefaultRouter()
router.register(r'shipments', views.ShipmentTrackingList, 'shipments')
router.register(r'uztrackings', views.UzTrackingList, 'uztrackings')


urlpatterns = [
    path('', include(router.urls)),
    path('import-shipments/', import_shipments, name='import-shipments'),
    path('import-uztrackings/', import_uztracking, name='import-uztrackings'),
]
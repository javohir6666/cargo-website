from django.contrib import admin
from .models import ShipmentTracking,UzTracking

class ShipmentTrackingAdmin(admin.ModelAdmin):
    list_display = ["customer", "tracking_code", "quantity"]
    list_filter = ["customer"]
    search_fields = ["tracking_code", "customer__username"]

admin.site.register(ShipmentTracking, ShipmentTrackingAdmin)
    
    
class UzTrackingAdmin(admin.ModelAdmin):
    list_display = ["customer", "tracking_code", "quantity"]
    list_filter = ["customer"]
    search_fields = ["tracking_code", "customer__username"]
    
admin.site.register(UzTracking, UzTrackingAdmin)
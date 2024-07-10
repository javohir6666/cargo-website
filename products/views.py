from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from .models import ShipmentTracking, UzTracking
from .serializers import ShipmentTrackingSerializer, UzTrackingSerializer
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
import pandas as pd
   
class ShipmentTrackingFilter(django_filters.FilterSet):
    tracking_code = django_filters.CharFilter(field_name='tracking_code', lookup_expr='exact')

    class Meta:
        model = ShipmentTracking
        fields = ['tracking_code']

class ShipmentTrackingList(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ShipmentTrackingSerializer
    queryset = ShipmentTracking.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShipmentTrackingFilter
    
    
    
      
class UzTrackingList(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UzTrackingSerializer
    queryset = UzTracking.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['tracking_code']
    
    
    
#   IMPORT SHIPMENTS
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def import_shipments(request):
    file = request.FILES.get('file')
    if not file:
        return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not file.name.endswith('.xlsx'):
        return Response({"error": "Invalid file format. Please upload an Excel file."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        df = pd.read_excel(file)
        skipped_customers = []
        for _, row in df.iterrows():
            tracking_code = row['Shipment Tracking Code']
            shipping_name = row['Shipping Name']
            quantity = row['Quantity']
            weight = row['Weight/KG']
            customer_code = row['Customer code']
            package_number = row['Package Number']

            shipment_data = {
                'tracking_code': tracking_code,
                'shipping_name': shipping_name,
                'quantity': quantity,
                'weight': weight,
                'customer': customer_code,
                'package_number': package_number
            }

            serializer = ShipmentTrackingSerializer(data=shipment_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"success": "Shipments imported successfully."}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#   IMPORT UZTRACKING
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def import_uztracking(request):
    file = request.FILES.get('file')
    if not file:
        return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not file.name.endswith('.xlsx'):
        return Response({"error": "Invalid file format. Please upload an Excel file."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        df = pd.read_excel(file)
        for _, row in df.iterrows():
            tracking_code = row['Shipment Tracking Code']
            quantity = row['Quantity']
            weight = row['Weight/KG']
            customer_code = row['Customer code']

            uztracking_data = {
                'tracking_code': tracking_code,
                'quantity': quantity,
                'weight': weight,
                'customer': customer_code,
            }

            serializer = UzTrackingSerializer(data=uztracking_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"success": "Shipments imported successfully."}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        

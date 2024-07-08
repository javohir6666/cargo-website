from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd

from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

class ProductList(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class OrderList(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()



@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def import_products(request):
    file = request.FILES.get('file')
    if not file:
        return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not file.name.endswith('.xlsx'):
        return Response({"error": "Invalid file format. Please upload an Excel file."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        df = pd.read_excel(file)
        for _, row in df.iterrows():
            product_data = {
                'title': row['title'],
                'description': row['description'],
                'price': row['price'],
                'quantity': row['quantity']
            }
            serializer = ProductSerializer(data=product_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"success": "Products imported successfully."}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def import_orders(request):
    file = request.FILES.get('file')
    if not file:
        return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not file.name.endswith('.xlsx'):
        return Response({"error": "Invalid file format. Please upload an Excel file."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        df = pd.read_excel(file)
        for _, row in df.iterrows():
            order_data = {
                'user': row['user'],
                'product': row['product'],
                'delivery_to': row['delivery_to'],
                'status': row['status']
            }
            serializer = OrderSerializer(data=order_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"success": "Order's status imported successfully."}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

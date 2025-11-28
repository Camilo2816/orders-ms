from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from django.conf import settings
import requests
from .models import Order, OrderItem
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        items_data = data.get('items', [])
        
        if not items_data:
            return Response({"detail": "No items provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Create Order first (status PENDING by default)
                order = Order.objects.create(
                    customer_name=data.get('customer_name'),
                    customer_email=data.get('customer_email'),
                    status='PENDING'
                )

                total_amount = 0

                for item in items_data:
                    product_id = item.get('product_id')
                    quantity = item.get('quantity')

                    if not product_id or not quantity:
                        raise ValueError("Product ID and quantity are required for each item")

                    # Verify product and get price
                    product_url = f"{settings.PRODUCTS_MS_URL}/products/{product_id}"
                    try:
                        response = requests.get(product_url)
                        if response.status_code != 200:
                            raise ValueError(f"Product {product_id} not found or service unavailable")
                        
                        product_data = response.json()
                        unit_price = float(product_data.get('price', 0))
                        
                    except requests.RequestException:
                        raise ValueError(f"Failed to communicate with Products service for product {product_id}")

                    # Create OrderItem
                    # total_price is calculated in save() method of OrderItem but we need unit_price
                    order_item = OrderItem.objects.create(
                        order=order,
                        product_id=product_id,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=quantity * unit_price
                    )
                    
                    total_amount += float(order_item.total_price)

                # Update Order total amount
                order.total_amount = total_amount
                order.save()

                serializer = self.get_serializer(order)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

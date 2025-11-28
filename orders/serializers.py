from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'quantity', 'unit_price', 'total_price']
        read_only_fields = ['id', 'total_price', 'unit_price'] # unit_price is fetched from products-ms

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_email', 'status', 'total_amount', 'created_at', 'updated_at', 'items']
        read_only_fields = ['id', 'total_amount', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Logic is handled in the View to support atomic transaction and verification
        # This create method might not be used if we override create in ViewSet, 
        # but for standard DRF usage, we can leave it or override it.
        # We will handle creation in the ViewSet to keep verification logic separate or here.
        # Let's handle it in the ViewSet as requested to keep it clear.
        pass

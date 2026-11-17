from rest_framework import serializers
from .models import Product, Box, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class BoxSerializer(serializers.ModelSerializer):
    volume = serializers.ReadOnlyField()

    class Meta:
        model = Box
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product_sku = serializers.ReadOnlyField(source='product.sku')
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_sku', 'product_name', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    recommended_box_details = BoxSerializer(source='recommended_box', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'created_at',
            'is_packed',
            'recommended_box',
            'recommended_box_details',
            'items',
        ]
        read_only_fields = ['recommended_box', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        instance.order_number = validated_data.get('order_number', instance.order_number)
        instance.is_packed = validated_data.get('is_packed', instance.is_packed)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)

        return instance
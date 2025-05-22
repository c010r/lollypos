from rest_framework import serializers
from .models import MenuItem, Order, OrderItem

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'category']

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())

    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'items', 'status', 'timestamp']
        read_only_fields = ['status', 'timestamp'] # Status will be handled by the backend logic initially

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            menu_item_instance = item_data['menu_item']
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item_instance,
                quantity=item_data['quantity'],
                price_at_time_of_order=menu_item_instance.price # Set price at time of order
            )
        return order

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Category, Product, Ingredient, ProductIngredient,
    Role, Employee, Table, Customer, PaymentMethod,
    Discount, ModifierGroup, ProductModifier, ProductModifierRelation,
    Order, OrderItem, OrderItemModifier, OrderDiscount, Payment
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class ProductIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.ReadOnlyField(source='ingredient.name')
    
    class Meta:
        model = ProductIngredient
        fields = ['id', 'ingredient', 'ingredient_name', 'quantity']

class ModifierGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModifierGroup
        fields = '__all__'

class ProductModifierSerializer(serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(source='group.name', read_only=True)
    
    class Meta:
        model = ProductModifier
        fields = ['id', 'name', 'additional_price', 'group', 'group_name']

class ProductModifierRelationSerializer(serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(source='modifier_group.name')
    
    class Meta:
        model = ProductModifierRelation
        fields = ['id', 'modifier_group', 'group_name']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    ingredients = ProductIngredientSerializer(many=True, read_only=True)
    available_modifier_groups = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'cost', 'category', 'category_name', 
                 'image', 'is_available', 'sku_code', 'estimated_preparation_time', 
                 'ingredients', 'available_modifier_groups']
    
    def get_available_modifier_groups(self, obj):
        relations = ProductModifierRelation.objects.filter(product=obj)
        groups = [relation.modifier_group for relation in relations]
        return ModifierGroupSerializer(groups, many=True).data

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    role_name = serializers.ReadOnlyField(source='role.get_name_display')
    
    class Meta:
        model = Employee
        fields = ['id', 'user', 'first_name', 'last_name', 'role', 'role_name', 'is_active', 'pin_code']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee
    
    def update(self, instance, validated_data):
        if 'user' in validated_data:
            user_data = validated_data.pop('user')
            user = instance.user
            user.username = user_data.get('username', user.username)
            if 'password' in user_data:
                user.set_password(user_data['password'])
            user.email = user_data.get('email', user.email)
            user.save()
        
        return super().update(instance, validated_data)

class TableSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Table
        fields = ['id', 'number', 'capacity', 'status', 'status_display', 'location']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class DiscountSerializer(serializers.ModelSerializer):
    discount_type_display = serializers.CharField(source='get_discount_type_display', read_only=True)
    
    class Meta:
        model = Discount
        fields = '__all__'

class OrderItemModifierSerializer(serializers.ModelSerializer):
    modifier_name = serializers.ReadOnlyField(source='modifier.name')
    
    class Meta:
        model = OrderItemModifier
        fields = ['id', 'modifier', 'modifier_name', 'price_at_time']

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    modifiers = OrderItemModifierSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price', 
                 'subtotal', 'notes', 'status', 'status_display', 'modifiers']

class OrderDiscountSerializer(serializers.ModelSerializer):
    discount_name = serializers.ReadOnlyField(source='discount.name')
    
    class Meta:
        model = OrderDiscount
        fields = ['id', 'discount', 'discount_name', 'amount']

class PaymentSerializer(serializers.ModelSerializer):
    payment_method_name = serializers.ReadOnlyField(source='payment_method.name')
    
    class Meta:
        model = Payment
        fields = ['id', 'payment_method', 'payment_method_name', 'amount', 
                  'tip', 'datetime', 'reference']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    discounts = OrderDiscountSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    table_number = serializers.ReadOnlyField(source='table.number', default=None)
    customer_name = serializers.SerializerMethodField()
    employee_name = serializers.ReadOnlyField(source='employee.first_name')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    order_type_display = serializers.CharField(source='get_order_type_display', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'table', 'table_number', 'customer', 'customer_name',
                 'employee', 'employee_name', 'status', 'status_display', 
                 'order_type', 'order_type_display', 'datetime', 'subtotal', 
                 'tax', 'total', 'notes', 'delivery_address', 'items',
                 'discounts', 'payments']
    
    def get_customer_name(self, obj):
        if obj.customer:
            return f"{obj.customer.first_name} {obj.customer.last_name}"
        return None

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['table', 'customer', 'employee', 'status', 'order_type',
                 'notes', 'delivery_address']

class OrderItemCreateSerializer(serializers.ModelSerializer):
    modifiers = serializers.ListField(
        child=serializers.IntegerField(), 
        write_only=True,
        required=False
    )
    
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'notes', 'modifiers']
    
    def create(self, validated_data):
        modifiers_data = validated_data.pop('modifiers', [])
        order_item = OrderItem.objects.create(**validated_data)
        
        # Añadir modificadores si existen
        if modifiers_data:
            for modifier_id in modifiers_data:
                try:
                    modifier = ProductModifier.objects.get(id=modifier_id)
                    OrderItemModifier.objects.create(
                        order_item=order_item,
                        modifier=modifier,
                        price_at_time=modifier.additional_price
                    )
                except ProductModifier.DoesNotExist:
                    pass
        
        return order_item

class MenuCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products']

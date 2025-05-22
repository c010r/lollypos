from django.shortcuts import render
from django.db.models import Count, Sum, Q, F
from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import (
    Category, Product, Ingredient, ProductIngredient,
    Role, Employee, Table, Customer, PaymentMethod,
    Discount, ModifierGroup, ProductModifier, ProductModifierRelation,
    Order, OrderItem, OrderItemModifier, OrderDiscount, Payment
)
from .serializers import (
    CategorySerializer, ProductSerializer, IngredientSerializer,
    ProductIngredientSerializer, RoleSerializer, EmployeeSerializer,
    TableSerializer, CustomerSerializer, PaymentMethodSerializer,
    DiscountSerializer, ModifierGroupSerializer, ProductModifierSerializer,
    OrderSerializer, OrderItemSerializer, OrderItemModifierSerializer,
    OrderDiscountSerializer, PaymentSerializer, MenuCategorySerializer,
    OrderCreateSerializer, OrderItemCreateSerializer, ProductModifierRelationSerializer
)
from django.utils import timezone
from datetime import timedelta

# Create your views here.

@api_view(['GET'])
@permission_classes([])
def health_check(request):
    """Endpoint para verificar que la API está funcionando correctamente"""
    return Response(
        {"status": "success", "message": "API está funcionando correctamente"},
        status=status.HTTP_200_OK
    )

class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet para ver y editar categorías de productos"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    @action(detail=False, methods=['get'])
    def with_products(self, request):
        """Obtener categorías con sus productos"""
        categories = Category.objects.all()
        serializer = MenuCategorySerializer(categories, many=True)
        return Response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet para ver y editar productos"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['category', 'is_available']
    search_fields = ['name', 'description']
    
    @action(detail=True, methods=['get'])
    def ingredients(self, request, pk=None):
        """Ver los ingredientes de un producto específico"""
        product = self.get_object()
        ingredients = ProductIngredient.objects.filter(product=product)
        serializer = ProductIngredientSerializer(ingredients, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_ingredient(self, request, pk=None):
        """Añadir un ingrediente a un producto"""
        product = self.get_object()
        serializer = ProductIngredientSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def modifiers(self, request, pk=None):
        """Ver los grupos de modificadores disponibles para un producto"""
        product = self.get_object()
        relations = ProductModifierRelation.objects.filter(product=product)
        serializer = ProductModifierRelationSerializer(relations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_modifier_group(self, request, pk=None):
        """Añadir un grupo de modificadores a un producto"""
        product = self.get_object()
        serializer = ProductModifierRelationSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IngredientViewSet(viewsets.ModelViewSet):
    """ViewSet para ver y editar ingredientes"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Obtener ingredientes con stock bajo"""
        ingredients = Ingredient.objects.filter(current_stock__lte=F('minimum_stock'))
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

class RoleViewSet(viewsets.ModelViewSet):
    """ViewSet para roles de empleados"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet para empleados"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filterset_fields = ['is_active', 'role']
    search_fields = ['first_name', 'last_name']
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Obtiene información del empleado autenticado actualmente
        """
        if not request.user.is_authenticated:
            return Response({'error': 'No autenticado'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            employee = Employee.objects.get(user=request.user)
            serializer = self.get_serializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response(
                {'error': 'No existe un perfil de empleado para este usuario'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def login_with_pin(self, request):
        """Login con PIN para empleados"""
        pin = request.data.get('pin_code')
        if not pin:
            return Response({'error': 'Se requiere PIN'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            employee = Employee.objects.get(pin_code=pin, is_active=True)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response({'error': 'PIN inválido'}, status=status.HTTP_401_UNAUTHORIZED)

class TableViewSet(viewsets.ModelViewSet):
    """ViewSet para mesas"""
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    filterset_fields = ['status']
    
    @action(detail=True, methods=['get'])
    def active_orders(self, request, pk=None):
        """Obtener pedidos activos de una mesa"""
        table = self.get_object()
        orders = Order.objects.filter(
            table=table, 
            status__in=['PENDING', 'IN_PROGRESS', 'READY', 'SERVED']
        )
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Cambiar el estado de una mesa"""
        table = self.get_object()
        status = request.data.get('status')
        if status in dict(Table.TABLE_STATUS).keys():
            table.status = status
            table.save()
            serializer = TableSerializer(table)
            return Response(serializer.data)
        return Response({'error': 'Estado inválido'}, status=status.HTTP_400_BAD_REQUEST)

class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet para clientes"""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    search_fields = ['first_name', 'last_name', 'phone', 'email']

class PaymentMethodViewSet(viewsets.ModelViewSet):
    """ViewSet para métodos de pago"""
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer

class DiscountViewSet(viewsets.ModelViewSet):
    """ViewSet para descuentos"""
    queryset = Discount.objects.filter(is_active=True)
    serializer_class = DiscountSerializer
    
    @action(detail=False, methods=['post'])
    def validate_code(self, request):
        """Validar un código de descuento"""
        code = request.data.get('code')
        if not code:
            return Response({'error': 'Se requiere código'}, status=status.HTTP_400_BAD_REQUEST)
        
        now = timezone.now()
        try:
            discount = Discount.objects.get(
                code=code,
                is_active=True,
                start_date__lte=now,
                end_date__gte=now
            )
            serializer = DiscountSerializer(discount)
            return Response(serializer.data)
        except Discount.DoesNotExist:
            return Response({'error': 'Código inválido o vencido'}, status=status.HTTP_404_NOT_FOUND)

class ModifierGroupViewSet(viewsets.ModelViewSet):
    """ViewSet para grupos de modificadores"""
    queryset = ModifierGroup.objects.all()
    serializer_class = ModifierGroupSerializer
    
    @action(detail=True, methods=['get'])
    def modifiers(self, request, pk=None):
        """Obtener los modificadores de un grupo"""
        group = self.get_object()
        modifiers = ProductModifier.objects.filter(group=group)
        serializer = ProductModifierSerializer(modifiers, many=True)
        return Response(serializer.data)

class ProductModifierViewSet(viewsets.ModelViewSet):
    """ViewSet para modificadores de productos"""
    queryset = ProductModifier.objects.all()
    serializer_class = ProductModifierSerializer
    filterset_fields = ['group']

class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet para pedidos"""
    queryset = Order.objects.all()
    filterset_fields = ['status', 'order_type', 'table']
    search_fields = ['order_number']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtener pedidos activos"""
        orders = Order.objects.filter(
            status__in=['PENDING', 'IN_PROGRESS', 'READY', 'SERVED']
        ).order_by('datetime')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_date(self, request):
        """Obtener pedidos por rango de fechas"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        orders = Order.objects.all()
        if start_date:
            orders = orders.filter(datetime__gte=start_date)
        if end_date:
            orders = orders.filter(datetime__lte=end_date)
        
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """Añadir un ítem al pedido"""
        order = self.get_object()
        serializer = OrderItemCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.validated_data['order'] = order
            item = serializer.save()
            return Response(OrderItemSerializer(item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def add_discount(self, request, pk=None):
        """Aplicar un descuento al pedido"""
        order = self.get_object()
        discount_id = request.data.get('discount')
        
        try:
            discount = Discount.objects.get(id=discount_id, is_active=True)
            
            # Calcular el monto del descuento
            if discount.discount_type == 'PERCENTAGE':
                amount = order.subtotal * (discount.value / 100)
            else:
                amount = min(discount.value, order.subtotal)  # No descontar más que el subtotal
            
            # Aplicar el descuento
            discount_obj = OrderDiscount.objects.create(
                order=order,
                discount=discount,
                amount=amount
            )
            
            # Recalcular totales
            order.total = order.subtotal + order.tax - amount
            order.save()
            
            serializer = OrderDiscountSerializer(discount_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Discount.DoesNotExist:
            return Response({'error': 'Descuento no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Cambiar el estado del pedido"""
        order = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Order.ORDER_STATUS).keys():
            return Response({'error': 'Estado inválido'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Manejar cambios específicos de estado
        if new_status == 'PAID' and order.table:
            # Verificar si este es el último pedido activo en la mesa
            active_orders = Order.objects.filter(
                table=order.table, 
                status__in=['PENDING', 'IN_PROGRESS', 'READY', 'SERVED']
            ).exclude(id=order.id)
            
            if not active_orders.exists():
                order.table.status = 'AVAILABLE'
                order.table.save()
        
        order.status = new_status
        order.save()
        
        # También actualizar el estado de los items si es necesario
        if new_status in ['CANCELLED', 'PAID', 'SERVED', 'READY', 'IN_PROGRESS']:
            order.items.all().update(status=new_status)
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)

class OrderItemViewSet(viewsets.ModelViewSet):
    """ViewSet para items de pedido"""
    queryset = OrderItem.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderItemCreateSerializer
        return OrderItemSerializer
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Cambiar el estado de un ítem de pedido"""
        item = self.get_object()
        status = request.data.get('status')
        
        if status in dict(Order.ORDER_STATUS).keys():
            item.status = status
            item.save()
            serializer = OrderItemSerializer(item)
            return Response(serializer.data)
        return Response({'error': 'Estado inválido'}, status=status.HTTP_400_BAD_REQUEST)

class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet para pagos"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    def create(self, request, *args, **kwargs):
        """Procesar un nuevo pago"""
        serializer = PaymentSerializer(data=request.data)
        
        if serializer.is_valid():
            payment = serializer.save()
            
            # El método save de Payment ya actualiza el status del pedido
            # cuando se completa el pago
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReportViewSet(viewsets.ViewSet):
    """ViewSet para generar reportes básicos"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def sales_by_date(self, request):
        """Reporte de ventas por fecha"""
        days = int(request.query_params.get('days', 7))
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        orders = Order.objects.filter(
            status='PAID',
            datetime__gte=start_date,
            datetime__lte=end_date
        )
        
        # Agrupar por fecha
        sales_by_date = orders.values('datetime__date').annotate(
            total_sales=Sum('total'),
            orders_count=Count('id')
        ).order_by('datetime__date')
        
        return Response(sales_by_date)
    
    @action(detail=False, methods=['get'])
    def sales_by_product(self, request):
        """Reporte de ventas por producto"""
        days = int(request.query_params.get('days', 7))
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        # Obtener pedidos pagados en el rango de fechas
        paid_orders = Order.objects.filter(
            status='PAID',
            datetime__gte=start_date,
            datetime__lte=end_date
        )
        
        # Agrupar por producto
        items_sold = OrderItem.objects.filter(
            order__in=paid_orders
        ).values('product__name').annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum('subtotal')
        ).order_by('-total_revenue')
        
        return Response(items_sold)
    
    @action(detail=False, methods=['get'])
    def sales_by_category(self, request):
        """Reporte de ventas por categoría"""
        days = int(request.query_params.get('days', 7))
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        # Obtener pedidos pagados en el rango de fechas
        paid_orders = Order.objects.filter(
            status='PAID',
            datetime__gte=start_date,
            datetime__lte=end_date
        )
        
        # Agrupar por categoría
        items_by_category = OrderItem.objects.filter(
            order__in=paid_orders
        ).values('product__category__name').annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum('subtotal')
        ).order_by('-total_revenue')
        
        return Response(items_by_category)

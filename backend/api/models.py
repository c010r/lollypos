from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

# Create your models here.

class Category(models.Model):
    """Modelo para representar las categorías de productos en el menú"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Product(models.Model):
    """Modelo para representar los productos/platos disponibles en el menú"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    sku_code = models.CharField(max_length=50, blank=True, null=True, unique=True)
    estimated_preparation_time = models.PositiveIntegerField(default=15, help_text="Tiempo estimado de preparación en minutos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    """Modelo para representar los ingredientes del inventario"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50, help_text="Unidad de medida (kg, g, l, ml, etc)")
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=10)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Ingrediente"
        verbose_name_plural = "Ingredientes"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.unit})"
    
    @property
    def needs_restock(self):
        return self.current_stock <= self.minimum_stock

class ProductIngredient(models.Model):
    """Relación entre productos e ingredientes"""
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='products')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        verbose_name = "Ingrediente de Producto"
        verbose_name_plural = "Ingredientes de Productos"
        unique_together = ['product', 'ingredient']
    
    def __str__(self):
        return f"{self.product.name} - {self.ingredient.name}: {self.quantity} {self.ingredient.unit}"

class Role(models.Model):
    """Modelo para representar los roles de los empleados"""
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('MANAGER', 'Gerente'),
        ('WAITER', 'Mesero'),
        ('CASHIER', 'Cajero'),
        ('CHEF', 'Cocinero'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
    
    def __str__(self):
        return self.get_name_display()

class Employee(models.Model):
    """Modelo para representar a los empleados"""
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='employees')
    is_active = models.BooleanField(default=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True, help_text="PIN de 4-6 dígitos para acceso rápido")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"

class Table(models.Model):
    """Modelo para representar las mesas del establecimiento"""
    TABLE_STATUS = [
        ('AVAILABLE', 'Disponible'),
        ('OCCUPIED', 'Ocupada'),
        ('RESERVED', 'Reservada'),
        ('MAINTENANCE', 'Mantenimiento'),
    ]
    
    id = models.AutoField(primary_key=True)
    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField(default=4)
    status = models.CharField(max_length=20, choices=TABLE_STATUS, default='AVAILABLE')
    location = models.CharField(max_length=100, blank=True, null=True, help_text="Ubicación dentro del establecimiento")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        ordering = ['number']
    
    def __str__(self):
        return f"Mesa {self.number} ({self.get_status_display()}) - {self.capacity} personas"

class Customer(models.Model):
    """Modelo para representar a los clientes"""
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class PaymentMethod(models.Model):
    """Modelo para representar los métodos de pago"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Método de Pago"
        verbose_name_plural = "Métodos de Pago"
    
    def __str__(self):
        return self.name

class Discount(models.Model):
    """Modelo para representar los descuentos"""
    DISCOUNT_TYPE = [
        ('PERCENTAGE', 'Porcentaje'),
        ('FIXED', 'Monto Fijo'),
    ]
    
    APPLICABLE_TO = [
        ('ALL', 'Todo'),
        ('PRODUCT', 'Producto específico'),
        ('CATEGORY', 'Categoría'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE, default='PERCENTAGE')
    value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    code = models.CharField(max_length=50, blank=True, null=True, unique=True)
    applicable_to = models.CharField(max_length=20, choices=APPLICABLE_TO, default='ALL')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Descuento"
        verbose_name_plural = "Descuentos"
    
    def __str__(self):
        return f"{self.name} - {self.discount_type}: {self.value}"

class ModifierGroup(models.Model):
    """Grupo de modificadores para productos"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    is_required = models.BooleanField(default=False)
    multiple_selection = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Grupo de Modificadores"
        verbose_name_plural = "Grupos de Modificadores"
    
    def __str__(self):
        return self.name

class ProductModifier(models.Model):
    """Modelo para representar los modificadores de productos (extras, personalizaciones)"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    group = models.ForeignKey(ModifierGroup, on_delete=models.CASCADE, related_name='modifiers', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Modificador de Producto"
        verbose_name_plural = "Modificadores de Producto"
    
    def __str__(self):
        return f"{self.name} (+${self.additional_price})"

class ProductModifierRelation(models.Model):
    """Relación entre productos y sus modificadores disponibles"""
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='available_modifiers')
    modifier_group = models.ForeignKey(ModifierGroup, on_delete=models.CASCADE, related_name='applicable_products')
    
    class Meta:
        verbose_name = "Relación Producto-Modificador"
        verbose_name_plural = "Relaciones Producto-Modificador"
        unique_together = ['product', 'modifier_group']
    
    def __str__(self):
        return f"{self.product.name} - {self.modifier_group.name}"

class Order(models.Model):
    """Modelo para representar los pedidos"""
    ORDER_STATUS = [
        ('PENDING', 'Pendiente'),
        ('IN_PROGRESS', 'En Preparación'),
        ('READY', 'Listo'),
        ('SERVED', 'Servido'),
        ('PAID', 'Pagado'),
        ('CANCELLED', 'Cancelado'),
    ]
    
    ORDER_TYPE = [
        ('DINE_IN', 'En Salón'),
        ('TAKEAWAY', 'Para Llevar'),
        ('DELIVERY', 'A Domicilio'),
    ]
    
    id = models.AutoField(primary_key=True)
    order_number = models.CharField(max_length=50, unique=True, blank=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, related_name='orders', null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, related_name='orders', null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='orders')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PENDING')
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE, default='DINE_IN')
    datetime = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-datetime']
    
    def __str__(self):
        return f"Pedido #{self.order_number} - {self.get_status_display()}"
    
    def save(self, *args, **kwargs):
        # Generar número de orden único si es nuevo
        if not self.order_number:
            prefix = "ORD"
            date_str = self.datetime.strftime("%Y%m%d") if self.datetime else timezone.now().strftime("%Y%m%d")
            random_str = str(uuid.uuid4().hex)[:6]
            self.order_number = f"{prefix}-{date_str}-{random_str}"
        super().save(*args, **kwargs)
    
    def calculate_totals(self):
        """Calcular subtotal, impuestos y total del pedido"""
        items = self.items.all()
        self.subtotal = sum(item.subtotal for item in items)
        # Asumiendo un 16% de IVA, ajustar según requerimientos fiscales
        self.tax = self.subtotal * 0.16
        self.total = self.subtotal + self.tax
        self.save()

class OrderItem(models.Model):
    """Modelo para representar los ítems de un pedido"""
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Order.ORDER_STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Ítem de Pedido"
        verbose_name_plural = "Ítems de Pedido"
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} - ${self.subtotal}"
    
    def save(self, *args, **kwargs):
        # Actualizar precio unitario desde el producto si es nuevo
        if not self.id and not self.unit_price:
            self.unit_price = self.product.price
        
        # Calcular subtotal
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        
        # Actualizar totales del pedido
        self.order.calculate_totals()
        
        # Reducir inventario
        if not self.id:  # Solo si es nuevo item
            self.update_inventory()
    
    def update_inventory(self):
        """Actualizar el inventario basado en los ingredientes del producto"""
        ingredients = ProductIngredient.objects.filter(product=self.product)
        for item in ingredients:
            ingredient = item.ingredient
            quantity_needed = item.quantity * self.quantity
            if ingredient.current_stock >= quantity_needed:
                ingredient.current_stock -= quantity_needed
                ingredient.save()
            else:
                # Manejar falta de stock (podrías lanzar una excepción o manejarlo de otra forma)
                pass

class OrderItemModifier(models.Model):
    """Modelos para representar los modificadores aplicados a un ítem de pedido"""
    id = models.AutoField(primary_key=True)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='modifiers')
    modifier = models.ForeignKey(ProductModifier, on_delete=models.PROTECT)
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Modificador de Ítem"
        verbose_name_plural = "Modificadores de Ítem"
        unique_together = ['order_item', 'modifier']
    
    def __str__(self):
        return f"{self.order_item.product.name} - {self.modifier.name}"
    
    def save(self, *args, **kwargs):
        # Usar el precio actual del modificador si no se especificó
        if not self.price_at_time and not self.id:
            self.price_at_time = self.modifier.additional_price
        super().save(*args, **kwargs)
        
        # Actualizar subtotal del item de pedido y recalcular totales
        order_item = self.order_item
        modifiers_total = sum(mod.price_at_time for mod in order_item.modifiers.all())
        order_item.subtotal = (order_item.unit_price + modifiers_total) * order_item.quantity
        order_item.save()
        order_item.order.calculate_totals()

class OrderDiscount(models.Model):
    """Relación entre pedidos y descuentos aplicados"""
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='discounts')
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Descuento de Pedido"
        verbose_name_plural = "Descuentos de Pedido"
    
    def __str__(self):
        return f"{self.order} - {self.discount.name}: -${self.amount}"

class Payment(models.Model):
    """Modelo para representar los pagos"""
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tip = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    datetime = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=100, blank=True, null=True, help_text="Referencia externa del pago")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
    
    def __str__(self):
        return f"Pago de {self.order} por ${self.amount} ({self.payment_method.name})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Verificar si el pedido ha sido pagado completamente
        order = self.order
        total_paid = sum(payment.amount for payment in order.payments.all())
        if total_paid >= order.total:
            order.status = 'PAID'
            order.save()
            
            # Si el pedido estaba en una mesa, liberar la mesa
            if order.table and order.table.status == 'OCCUPIED':
                # Verificar si no hay otros pedidos activos en la mesa
                active_orders = Order.objects.filter(
                    table=order.table, 
                    status__in=['PENDING', 'IN_PROGRESS', 'READY', 'SERVED']
                ).exclude(id=order.id)
                
                if not active_orders.exists():
                    order.table.status = 'AVAILABLE'
                    order.table.save()

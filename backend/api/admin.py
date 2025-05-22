from django.contrib import admin
from .models import (
    Category, Product, Ingredient, ProductIngredient,
    Role, Employee, Table, Customer, PaymentMethod,
    Discount, ModifierGroup, ProductModifier, ProductModifierRelation,
    Order, OrderItem, OrderItemModifier, OrderDiscount, Payment
)

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class ProductIngredientInline(admin.TabularInline):
    model = ProductIngredient
    extra = 1

class ProductModifierRelationInline(admin.TabularInline):
    model = ProductModifierRelation
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    inlines = [ProductIngredientInline, ProductModifierRelationInline]

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'current_stock', 'minimum_stock', 'needs_restock')
    list_filter = ('unit',)
    search_fields = ('name',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('first_name', 'last_name')

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'status', 'location')
    list_filter = ('status',)
    search_fields = ('number', 'location')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email')
    search_fields = ('first_name', 'last_name', 'phone', 'email')

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_type', 'value', 'is_active', 'code')
    list_filter = ('discount_type', 'is_active')
    search_fields = ('name', 'code')

@admin.register(ModifierGroup)
class ModifierGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_required', 'multiple_selection')

class ProductModifierInline(admin.TabularInline):
    model = ProductModifier
    extra = 1

@admin.register(ProductModifier)
class ProductModifierAdmin(admin.ModelAdmin):
    list_display = ('name', 'additional_price', 'group')
    list_filter = ('group',)
    search_fields = ('name',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderDiscountInline(admin.TabularInline):
    model = OrderDiscount
    extra = 0

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'status', 'order_type', 'table', 'customer', 'employee', 'datetime', 'total')
    list_filter = ('status', 'order_type', 'datetime')
    search_fields = ('order_number',)
    inlines = [OrderItemInline, OrderDiscountInline, PaymentInline]

class OrderItemModifierInline(admin.TabularInline):
    model = OrderItemModifier
    extra = 0

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unit_price', 'subtotal', 'status')
    list_filter = ('status',)
    inlines = [OrderItemModifierInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'amount', 'tip', 'datetime')
    list_filter = ('payment_method', 'datetime')

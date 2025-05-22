import os
import django
import random
from decimal import Decimal

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lollypos_project.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import (
    Category, Product, Ingredient, ProductIngredient,
    Role, Employee, Table, Customer, PaymentMethod,
    Discount, ModifierGroup, ProductModifier, ProductModifierRelation
)

def create_initial_data():
    print("Creando datos iniciales para LollyPOS...")
    
    # Crear roles
    print("Creando roles...")
    roles = {
        "ADMIN": Role.objects.create(name="ADMIN", description="Administrador del sistema"),
        "MANAGER": Role.objects.create(name="MANAGER", description="Gerente del establecimiento"),
        "WAITER": Role.objects.create(name="WAITER", description="Mesero"),
        "CASHIER": Role.objects.create(name="CASHIER", description="Cajero"),
        "CHEF": Role.objects.create(name="CHEF", description="Cocinero")
    }
    
    # Crear un empleado administrador
    print("Creando empleado administrador...")
    admin_user = User.objects.get(username='admin')
    Employee.objects.create(
        user=admin_user,
        first_name="Admin",
        last_name="Sistema",
        role=roles["ADMIN"],
        pin_code="123456"
    )
    
    # Crear empleados adicionales
    print("Creando empleados adicionales...")
    employees_data = [
        {
            "username": "maria",
            "password": "maria123",
            "first_name": "María",
            "last_name": "López",
            "role": roles["MANAGER"],
            "pin_code": "789012"
        },
        {
            "username": "carlos",
            "password": "carlos123",
            "first_name": "Carlos",
            "last_name": "Rodríguez",
            "role": roles["WAITER"],
            "pin_code": "345678"
        },
        {
            "username": "ana",
            "password": "ana123",
            "first_name": "Ana",
            "last_name": "Gómez",
            "role": roles["CASHIER"],
            "pin_code": "901234"
        },
        {
            "username": "javier",
            "password": "javier123",
            "first_name": "Javier",
            "last_name": "Fernández",
            "role": roles["CHEF"],
            "pin_code": "567890"
        }
    ]
    
    for emp_data in employees_data:
        user = User.objects.create_user(
            username=emp_data["username"],
            password=emp_data["password"]
        )
        Employee.objects.create(
            user=user,
            first_name=emp_data["first_name"],
            last_name=emp_data["last_name"],
            role=emp_data["role"],
            pin_code=emp_data["pin_code"]
        )
    
    # Crear categorías
    print("Creando categorías...")
    categories = {
        "ENTRADAS": Category.objects.create(name="Entradas", description="Platos para comenzar"),
        "PLATOS_PRINCIPALES": Category.objects.create(name="Platos Principales", description="Platos fuertes"),
        "POSTRES": Category.objects.create(name="Postres", description="Dulces y postres"),
        "BEBIDAS": Category.objects.create(name="Bebidas", description="Bebidas frías y calientes"),
        "GUARNICIONES": Category.objects.create(name="Guarniciones", description="Acompañamientos para los platos")
    }
    
    # Crear ingredientes
    print("Creando ingredientes...")
    ingredients = [
        Ingredient.objects.create(name="Pollo", unit="kg", current_stock=50, minimum_stock=10),
        Ingredient.objects.create(name="Carne de res", unit="kg", current_stock=30, minimum_stock=5),
        Ingredient.objects.create(name="Pescado", unit="kg", current_stock=20, minimum_stock=5),
        Ingredient.objects.create(name="Lechuga", unit="kg", current_stock=15, minimum_stock=3),
        Ingredient.objects.create(name="Tomate", unit="kg", current_stock=20, minimum_stock=4),
        Ingredient.objects.create(name="Cebolla", unit="kg", current_stock=25, minimum_stock=5),
        Ingredient.objects.create(name="Papas", unit="kg", current_stock=40, minimum_stock=10),
        Ingredient.objects.create(name="Arroz", unit="kg", current_stock=50, minimum_stock=10),
        Ingredient.objects.create(name="Azúcar", unit="kg", current_stock=30, minimum_stock=5),
        Ingredient.objects.create(name="Harina", unit="kg", current_stock=25, minimum_stock=5),
        Ingredient.objects.create(name="Chocolate", unit="kg", current_stock=10, minimum_stock=2),
        Ingredient.objects.create(name="Leche", unit="l", current_stock=40, minimum_stock=10),
        Ingredient.objects.create(name="Café", unit="kg", current_stock=5, minimum_stock=1),
        Ingredient.objects.create(name="Limón", unit="kg", current_stock=15, minimum_stock=3),
        Ingredient.objects.create(name="Frijoles", unit="kg", current_stock=20, minimum_stock=5),
    ]
    
    # Crear grupos de modificadores
    print("Creando grupos de modificadores...")
    modifier_groups = {
        "PUNTO_COCCION": ModifierGroup.objects.create(name="Punto de Cocción", is_required=True, multiple_selection=False),
        "ADICIONALES": ModifierGroup.objects.create(name="Adicionales", is_required=False, multiple_selection=True),
        "TAMANO": ModifierGroup.objects.create(name="Tamaño", is_required=True, multiple_selection=False),
        "TEMPERATURA": ModifierGroup.objects.create(name="Temperatura", is_required=True, multiple_selection=False),
    }
    
    # Crear modificadores
    print("Creando modificadores...")
    modifiers = {
        # Puntos de cocción
        "POCO_HECHO": ProductModifier.objects.create(name="Poco hecho", group=modifier_groups["PUNTO_COCCION"]),
        "TERMINO_MEDIO": ProductModifier.objects.create(name="Término medio", group=modifier_groups["PUNTO_COCCION"]),
        "BIEN_HECHO": ProductModifier.objects.create(name="Bien hecho", group=modifier_groups["PUNTO_COCCION"]),
        
        # Adicionales
        "QUESO_EXTRA": ProductModifier.objects.create(name="Queso extra", additional_price=Decimal('2.50'), group=modifier_groups["ADICIONALES"]),
        "TOCINO": ProductModifier.objects.create(name="Tocino", additional_price=Decimal('3.00'), group=modifier_groups["ADICIONALES"]),
        "AGUACATE": ProductModifier.objects.create(name="Aguacate", additional_price=Decimal('2.00'), group=modifier_groups["ADICIONALES"]),
        "HUEVO": ProductModifier.objects.create(name="Huevo frito", additional_price=Decimal('1.50'), group=modifier_groups["ADICIONALES"]),
        
        # Tamaños
        "PEQUENO": ProductModifier.objects.create(name="Pequeño", additional_price=Decimal('-1.00'), group=modifier_groups["TAMANO"]),
        "MEDIANO": ProductModifier.objects.create(name="Mediano", group=modifier_groups["TAMANO"]),
        "GRANDE": ProductModifier.objects.create(name="Grande", additional_price=Decimal('2.00'), group=modifier_groups["TAMANO"]),
        
        # Temperatura
        "FRIO": ProductModifier.objects.create(name="Frío", group=modifier_groups["TEMPERATURA"]),
        "CALIENTE": ProductModifier.objects.create(name="Caliente", group=modifier_groups["TEMPERATURA"]),
    }
    
    # Crear productos
    print("Creando productos...")
    products = [
        # Entradas
        Product.objects.create(name="Nachos con queso", description="Nachos con queso cheddar derretido", price=Decimal('8.99'), cost=Decimal('3.00'), category=categories["ENTRADAS"]),
        Product.objects.create(name="Aros de cebolla", description="Aros de cebolla fritos", price=Decimal('6.99'), cost=Decimal('2.00'), category=categories["ENTRADAS"]),
        Product.objects.create(name="Guacamole", description="Guacamole casero con totopos", price=Decimal('7.50'), cost=Decimal('2.50'), category=categories["ENTRADAS"]),
        
        # Platos Principales
        Product.objects.create(name="Hamburguesa clásica", description="Hamburguesa con lechuga, tomate y queso", price=Decimal('12.99'), cost=Decimal('5.00'), category=categories["PLATOS_PRINCIPALES"]),
        Product.objects.create(name="Filete de res", description="Filete de res de 300g", price=Decimal('24.99'), cost=Decimal('10.00'), category=categories["PLATOS_PRINCIPALES"]),
        Product.objects.create(name="Pasta Alfredo", description="Pasta con salsa Alfredo", price=Decimal('14.99'), cost=Decimal('4.00'), category=categories["PLATOS_PRINCIPALES"]),
        Product.objects.create(name="Pescado a la plancha", description="Filete de pescado a la plancha con limón", price=Decimal('18.99'), cost=Decimal('7.00'), category=categories["PLATOS_PRINCIPALES"]),
        
        # Postres
        Product.objects.create(name="Tarta de chocolate", description="Tarta de chocolate con helado de vainilla", price=Decimal('7.99'), cost=Decimal('3.00'), category=categories["POSTRES"]),
        Product.objects.create(name="Flan", description="Flan casero con caramelo", price=Decimal('5.99'), cost=Decimal('2.00'), category=categories["POSTRES"]),
        Product.objects.create(name="Helado surtido", description="Tres bolas de helado a elegir", price=Decimal('6.50'), cost=Decimal('2.50'), category=categories["POSTRES"]),
        
        # Bebidas
        Product.objects.create(name="Refresco", description="Refresco de cola, naranja o limón", price=Decimal('2.50'), cost=Decimal('0.80'), category=categories["BEBIDAS"]),
        Product.objects.create(name="Café", description="Café americano o expreso", price=Decimal('2.99'), cost=Decimal('0.70'), category=categories["BEBIDAS"]),
        Product.objects.create(name="Limonada", description="Limonada fresca casera", price=Decimal('3.50'), cost=Decimal('1.00'), category=categories["BEBIDAS"]),
        
        # Guarniciones
        Product.objects.create(name="Papas fritas", description="Porción de papas fritas", price=Decimal('4.99'), cost=Decimal('1.50'), category=categories["GUARNICIONES"]),
        Product.objects.create(name="Ensalada", description="Ensalada fresca de la casa", price=Decimal('5.99'), cost=Decimal('2.00'), category=categories["GUARNICIONES"]),
        Product.objects.create(name="Arroz", description="Porción de arroz", price=Decimal('3.99'), cost=Decimal('1.00'), category=categories["GUARNICIONES"]),
    ]
    
    # Asignar ingredientes a productos (ejemplo)
    print("Asignando ingredientes a productos...")
    # Hamburguesa
    hamburguesa = Product.objects.get(name="Hamburguesa clásica")
    ProductIngredient.objects.create(product=hamburguesa, ingredient=Ingredient.objects.get(name="Carne de res"), quantity=Decimal('0.15'))
    ProductIngredient.objects.create(product=hamburguesa, ingredient=Ingredient.objects.get(name="Lechuga"), quantity=Decimal('0.05'))
    ProductIngredient.objects.create(product=hamburguesa, ingredient=Ingredient.objects.get(name="Tomate"), quantity=Decimal('0.05'))
    
    # Filete
    filete = Product.objects.get(name="Filete de res")
    ProductIngredient.objects.create(product=filete, ingredient=Ingredient.objects.get(name="Carne de res"), quantity=Decimal('0.3'))
    
    # Pasta
    pasta = Product.objects.get(name="Pasta Alfredo")
    ProductIngredient.objects.create(product=pasta, ingredient=Ingredient.objects.get(name="Leche"), quantity=Decimal('0.2'))
    
    # Pescado
    pescado = Product.objects.get(name="Pescado a la plancha")
    ProductIngredient.objects.create(product=pescado, ingredient=Ingredient.objects.get(name="Pescado"), quantity=Decimal('0.25'))
    ProductIngredient.objects.create(product=pescado, ingredient=Ingredient.objects.get(name="Limón"), quantity=Decimal('0.05'))
    
    # Papas fritas
    papas = Product.objects.get(name="Papas fritas")
    ProductIngredient.objects.create(product=papas, ingredient=Ingredient.objects.get(name="Papas"), quantity=Decimal('0.2'))
    
    # Asignar modificadores a productos
    print("Asignando modificadores a productos...")
    # Hamburguesa: Punto de cocción y adicionales
    ProductModifierRelation.objects.create(product=hamburguesa, modifier_group=modifier_groups["PUNTO_COCCION"])
    ProductModifierRelation.objects.create(product=hamburguesa, modifier_group=modifier_groups["ADICIONALES"])
    
    # Filete: Punto de cocción
    ProductModifierRelation.objects.create(product=filete, modifier_group=modifier_groups["PUNTO_COCCION"])
    
    # Bebidas: Tamaño y temperatura
    for bebida in Product.objects.filter(category=categories["BEBIDAS"]):
        ProductModifierRelation.objects.create(product=bebida, modifier_group=modifier_groups["TAMANO"])
        if bebida.name != "Refresco":  # Solo café y limonada pueden ser calientes o fríos
            ProductModifierRelation.objects.create(product=bebida, modifier_group=modifier_groups["TEMPERATURA"])
    
    # Crear métodos de pago
    print("Creando métodos de pago...")
    PaymentMethod.objects.create(name="Efectivo")
    PaymentMethod.objects.create(name="Tarjeta de crédito")
    PaymentMethod.objects.create(name="Tarjeta de débito")
    PaymentMethod.objects.create(name="Transferencia")
    
    # Crear descuentos
    print("Creando descuentos...")
    Discount.objects.create(
        name="10% Descuento",
        description="10% de descuento en toda la cuenta",
        discount_type="PERCENTAGE",
        value=Decimal('10.00'),
        is_active=True,
        code="DESC10"
    )
    Discount.objects.create(
        name="Descuento de $5",
        description="$5 de descuento en toda la cuenta",
        discount_type="FIXED",
        value=Decimal('5.00'),
        is_active=True,
        code="FIJO5"
    )
    
    # Crear mesas
    print("Creando mesas...")
    for i in range(1, 11):  # 10 mesas
        capacity = 4
        if i <= 2:
            capacity = 2
        elif i >= 9:
            capacity = 8
        
        Table.objects.create(
            number=i,
            capacity=capacity,
            status="AVAILABLE",
            location=f"Zona {'A' if i <= 5 else 'B'}"
        )
    
    # Crear algunos clientes
    print("Creando clientes...")
    Customer.objects.create(
        first_name="Juan",
        last_name="Pérez",
        phone="5551234567",
        email="juan.perez@example.com"
    )
    Customer.objects.create(
        first_name="Laura",
        last_name="Martínez",
        phone="5559876543",
        email="laura.martinez@example.com"
    )
    Customer.objects.create(
        first_name="Roberto",
        last_name="González",
        phone="5554567890",
        email="roberto.gonzalez@example.com"
    )
    
    print("¡Datos iniciales creados con éxito!")

if __name__ == "__main__":
    create_initial_data()

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'tables', views.TableViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'payment-methods', views.PaymentMethodViewSet)
router.register(r'discounts', views.DiscountViewSet)
router.register(r'modifier-groups', views.ModifierGroupViewSet)
router.register(r'product-modifiers', views.ProductModifierViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'order-items', views.OrderItemViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'reports', views.ReportViewSet, basename='reports')

urlpatterns = [
    path('', include(router.urls)),
    path('health-check/', views.health_check, name='health-check'),
]

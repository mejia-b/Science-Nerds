from django.urls import path
from .views import HomeView, ProductsView, CustomerView, CreateOrderView, UpdateOrderView, DeleteOrderView

urlpatterns = [
    path('',HomeView.as_view(), name='home'),
    path('products', ProductsView.as_view(), name='products'),
    path('customer/<str:id>', CustomerView.as_view(), name='customer'),
    path('create_order/<str:id>',CreateOrderView.as_view(), name='create_order'),
    path('update_order/<str:id>', UpdateOrderView.as_view(), name='update_order'),
     path('delete_order/<str:id>', DeleteOrderView.as_view(), name='delete_order'),
]

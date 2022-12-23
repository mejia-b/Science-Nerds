from django.urls import path
from .views import HomeView, ProductsView, CustomerView

urlpatterns = [
    path('',HomeView.as_view(), name='home'),
    path('products', ProductsView.as_view(), name='products'),
    path('customer/<str:id>', CustomerView.as_view(), name='customer'),
]

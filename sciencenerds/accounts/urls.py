from django.urls import path
from .views import HomeView, ProductsView, CustomerView

urlpatterns = [
    path('',HomeView.as_view()),
    path('products', ProductsView.as_view()),
    path('customer', CustomerView.as_view()),
]

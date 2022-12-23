from django.shortcuts import render
from django.views import View
from .models import Customer, Product,Order
class HomeView(View):
    def get(self,request):
        orders = Order.objects.all()
        customers = Customer.objects.all()

        return render(
            request = request,
            template_name= 'accounts/dashboard.html',
            context={
                'orders':orders, 
                'customers':customers,
                }
        )

class ProductsView(View):
     def get(self,request):
        products = Product.objects.all()
        return render(
            request = request,
            template_name= 'accounts/products.html',
            context={'products':products},
        )
    

class CustomerView(View):
    def get(self,request):
        return render(
            request = request,
            template_name= 'accounts/customers.html',
        )






from django.shortcuts import render
from django.views import View

class HomeView(View):
    def get(self,request):
        return render(
            request = request,
            template_name= 'accounts/home.html',
        )

class ProductsView(View):
     def get(self,request):
        return render(
            request = request,
            template_name= 'accounts/products.html',
        )
    

class CustomerView(View):
    def get(self,request):
        return render(
            request = request,
            template_name= 'accounts/customers.html',
        )






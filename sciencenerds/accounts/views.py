from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product,Order
from .forms import OrderForm
class HomeView(View):
    def get(self,request):
        orders = list(Order.objects.all())[-5:]
        customers = Customer.objects.all()
        total_customers = customers.count()
        total_orders = Order.objects.all().count()
        delivered = Order.objects.filter(status='Delivered').count()
        pending = Order.objects.filter(status='Pending').count()

        return render(
            request = request,
            template_name= 'accounts/dashboard.html',
            context={
                'orders':orders, 
                'customers':customers,
                'total_customers':total_customers,
                'total_orders': total_orders,
                'delivered_count': delivered,
                'pending_count': pending,
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
    def get(self,request,id):
        customer = Customer.objects.get(id=id)
        orders = customer.order_set.all()
        total_orders = orders.count()
        return render(
            request = request,
            template_name= 'accounts/customers.html',
            context={
                'customer':customer,
                'orders': orders,
                'total_orders': total_orders,
            }
        )




class CreateOrderView(View):
    def get(self,request):
        # Create form object
        form = OrderForm()
        return render(
            request=request,
            template_name='accounts/order_form.html',
            context={'order_form':form},
        )

    def post(self,request):
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('home')


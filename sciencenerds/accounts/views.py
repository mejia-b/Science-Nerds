from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product,Order
from .forms import OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
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
        order_filter = OrderFilter(request.GET,queryset=orders)
        orders = order_filter.qs
        return render(
            request = request,
            template_name= 'accounts/customers.html',
            context={
                'customer':customer,
                'orders': orders,
                'total_orders': total_orders,
                'order_filter':order_filter,
            }
        )

class CreateOrderView(View):
    def get(self,request,id):
        # Create a form that can display multiple forms
        OrderFormSet = inlineformset_factory(Customer,Order, fields=['product','status'], extra=7)
        # Get customer associated with id
        customer = Customer.objects.get(id=id)
        # form object with multiple forms
        # arguments: queryset -> when selecting Order.objects.none() it will not populate any of the forms displayed to one of the 
        # customers orders. instance -> defines which customer object this formset will apply changes to 
        formset = OrderFormSet(queryset=Order.objects.none() ,instance=customer)
        # Create form object and set initial to a dictionary that will populate the form with the data provided
        #form = OrderForm(initial={'customer':customer})
        return render(
            request=request,
            template_name='accounts/order_form.html',
            context={'formset':formset},
        )

    def post(self,request,id):
        # Displays a single form
        #form = OrderForm(request.POST)
        # Form with multiple forms for order input
        OrderFormSet = inlineformset_factory(Customer,Order, fields=['product','status'])
        customer = Customer.objects.get(id=id)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()

        return redirect('home')

class UpdateOrderView(View):
    def get(self,request,id):
        order = Order.objects.get(id=id)
        form = OrderForm(instance=order)

        return render(
            request=request,
            template_name='accounts/update_form.html',
            context={
                'order_form':form,
            }
        )

    def post(self,request,id):
        order = Order.objects.get(id=id)
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()

        return redirect('home')

class DeleteOrderView(View):
    def get(self,request,id):
        order = Order.objects.get(id=id)
        return render(
            request=request,
            template_name='accounts/delete.html',
            context={'item':order},
        )

    def post(self,request,id):
        order = Order.objects.get(id=id)
        order.delete()

        return redirect('home')


class RegisterView(View):
    def get(self,request):
        form = CreateUserForm()
        return render(
            request=request,
            template_name='accounts/register.html',
            context= {
                'form':form,
            },
        )

    def post(self,request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(
            request=request,
            template_name='accounts/register.html',
             context= {
                'form':form,
            },
        )

class LoginView(View):
    def get(self,request):
        return render(
            request=request,
            template_name='accounts/login.html'
        )




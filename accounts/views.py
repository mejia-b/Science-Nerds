from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product,Order
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import allowed_users, admin_only
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group


@method_decorator(admin_only, name='get')
class HomeView(LoginRequiredMixin,View):
    login_url = 'login'
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
@method_decorator(allowed_users(allowed_roles=['admin']),name='get')
class ProductsView(LoginRequiredMixin,View):
     login_url = 'login'
     def get(self,request):
        products = Product.objects.all()
        return render(
            request = request,
            template_name= 'accounts/products.html',
            context={'products':products},
        )
    
@method_decorator(allowed_users(allowed_roles=['admin']),name='get')
class CustomerView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,id):
        customer = Customer.objects.get(id=id)
        orders = customer.order_set.all()
        total_orders = orders.count()
        # This is for the search bar
        # If there is any data that was entered to be filtered
        # The OrderFilter request.GET will execute and filter down the 
        # values that were set on the attribute of queryset
        order_filter = OrderFilter(request.GET,queryset=orders)
        orders = order_filter.qs
        return render(
            request = request,
            template_name= 'accounts/customer.html',
            context={
                'customer':customer,
                'orders': orders,
                'total_orders': total_orders,
                'order_filter':order_filter,
            }
        )
@method_decorator(allowed_users(allowed_roles=['admin']),name='get')
class CreateOrderView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,id):
        # Create a form that can display multiple forms
        # By doing this we can place multiple orders at once for a single customer
        # first parameter -> Parent model
        # second parameter -> Child model
        # fields-> what fields to allow for the child model
        OrderFormSet = inlineformset_factory(Customer,Order, fields=['product','status'], extra=4)
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
        OrderFormSet = inlineformset_factory(Customer,Order, fields=['product','status'],can_delete=False)
        customer = Customer.objects.get(id=id)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
        return redirect('home')

@method_decorator(allowed_users(allowed_roles=['admin']),name='get')
class UpdateOrderView(LoginRequiredMixin,View):
    login_url = 'login'
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
@method_decorator(allowed_users(allowed_roles=['admin']),name='get')
class DeleteOrderView(LoginRequiredMixin,View):
    login_url = 'login'
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
        # This prevents a logged in user from being able to see the Register page
        # If this endpoint is typed in the url then it will just redirect to the homepage
        if request.user.is_authenticated:
            return redirect('home')
        else:
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
        # get the username without getting any other attributes
        if form.is_valid():
            # Once this from gets saved a user is created and then the signal gets called
            # to make the connection where a User instance will also have a connection to a Customer instance
            form.save()
            username = form.cleaned_data.get('username')
            # message that gets displayed in the log in page once the account was successfully created
            messages.success(request,'Account was created for ' + username)
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
       # This prevents a logged in user from viewing the login page
       # If this endpoint is typed in the url it will just redirect to the home page
       if request.user.is_authenticated:
            return redirect('home')
       else:
            return render(
                request=request,
                template_name='accounts/login.html'
            )

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect')
            return redirect('login')

class LogoutUserView(View):
    def get(self,request):
        logout(request)
        return redirect('login')

@method_decorator(allowed_users(allowed_roles=['customer']),name='get')
class UserView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        orders = request.user.customer.order_set.all()
        total_orders = orders.count()
        delivered = orders.filter(status='Delivered').count()
        pending = orders.filter(status='Pending').count()
        return render(
            request=request,
            template_name='accounts/user.html',
            context={
                'orders':orders,
                'total_orders':total_orders,
                'delivered_count': delivered,
                'pending_count': pending,
                },
        )

@method_decorator(allowed_users(allowed_roles=['customer']),name='get')
class AccountSettingsView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        customer = request.user.customer
        form = CustomerForm(instance=customer)
        return render(
            request=request,
            template_name='accounts/account_settings.html',
            context={'form':form}
        )
    def post(self,request):
        customer = request.user.customer
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
        return redirect('account')

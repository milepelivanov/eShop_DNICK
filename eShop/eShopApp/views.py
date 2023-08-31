from django.contrib.auth import login

from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import Group, Permission
import random, string
from datetime import datetime
from .forms import CustomUserCreationForm, ProductForm
from .models import UserProfile, Product, ShoppingCart, ShoppingCartProduct, Order, OrderProduct


# Create your views here.


# LOGIN, REGISTER AND LOG OUT
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('products')


def custom_logout(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        print("DADA")
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile.objects.create(user=user, user_type=form.cleaned_data['user_type'])
            if user_profile.user_type == 'customer':
                user.groups.add(Group.objects.get(name='Buyer'))
            elif user_profile.user_type == 'seller':
                user.groups.add(Group.objects.get(name='Seller'))
                user.user_permissions.add(Permission.objects.get(codename='custom_add_product'))
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# SELLER OPTIONS
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)


    if request.user.userprofile.user_type == 'seller':
        product.delete()

    return redirect('products')


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form})


# BUYER OPTIONS
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    shopping_cart_product = None
    error_message = None

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            error_message = "Invalid quantity"
        elif quantity > product.stock:
            error_message = "Quantity exceeds available stock"
        else:
            shopping_cart_product, created = ShoppingCartProduct.objects.get_or_create(
                shopping_cart=shopping_cart,
                product=product,
                defaults={'quantity': quantity, 'price': product.price},
            )
            error_message = "Successfully added to cart"
            if not created:
                shopping_cart_product.quantity += quantity
                if shopping_cart_product.quantity <= product.stock:
                    shopping_cart_product.save()
                    error_message = "Successfully added to cart"
                else:
                    error_message = "Quantity exceeds available stock"

    context = {
        'products': Product.objects.all(),
        'user': request.user,
        'error_message': error_message,  
    }
    return render(request, "products.html", context)


def shopping_cart(request):
    user = request.user
    shopping_cart_products = ShoppingCartProduct.objects.filter(shopping_cart__user=user)
    total_price = sum(item.quantity * item.product.price for item in shopping_cart_products)

    context = {'shopping_cart_products': shopping_cart_products,
               'total_price': total_price, }

    if request.method == 'POST':
        current_page_url = reverse('shopping_cart')
        item_id_to_delete = request.POST.get('item_id_to_delete')
        if item_id_to_delete:
            item_to_delete = ShoppingCartProduct.objects.filter(id=item_id_to_delete, shopping_cart__user=user).first()
            if item_to_delete:
                item_to_delete.delete()
                return redirect(current_page_url)

    return render(request, 'shopping_cart.html', context)


def checkout(request):
    user = request.user
    shopping_cart_products = ShoppingCartProduct.objects.filter(shopping_cart__user=user)
    total_price = sum(item.quantity * item.product.price for item in shopping_cart_products)

    if request.method == 'POST':
        user_input = request.POST.get('user')
        address = request.POST.get('address')

       
        order_number = "#" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

        
        order = Order.objects.create(
            user=user,
            order_number=order_number,
            created_at=datetime.now(),
            total_price=total_price,
            address=address
        )

        
        for cart_product in shopping_cart_products:
            OrderProduct.objects.create(
                order=order,
                product=cart_product.product,
                quantity=cart_product.quantity,
                price=cart_product.product.price * cart_product.quantity
            )

    
        shopping_cart_products.delete()

  
        return redirect('products')

    context = {'shopping_cart_products': shopping_cart_products, 'total_price': total_price}
    return render(request, 'checkout.html', context)


def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user)

    context = {
        'orders': orders,
    }
    return render(request, 'order_history.html', context)


def products(request):
    categories = Product.objects.values_list('category__name', flat=True).distinct()
    selected_category = request.GET.get('category')
    filtered_products = Product.objects.all()

    if selected_category:
        if selected_category == '':
            selected_category = None
        else:
            filtered_products = Product.objects.filter(category__name=selected_category)

    return render(request, "products.html",
                  {'products': filtered_products, 'categories': categories, 'user': request.user,
                   'selected_category': selected_category})

"""
URL configuration for eShop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from eShopApp import views
from eShopApp.views import CustomLoginView
from eShopApp.views import register

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('admin/', admin.site.urls),
    path('products/', views.products, name="products"),
    path('products/delete/<int:product_id>', views.delete_product, name='delete_product'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>', views.edit_product, name='edit_product'),
    path('products/add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('shoppingCart/', views.shopping_cart, name="shopping_cart"),
    path('checkout/', views.checkout, name='checkout'),
    path('order_history/', views.order_history, name='order_history'),
    path('logout/', views.custom_logout, name='logout'),
]

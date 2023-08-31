from django.contrib import admin
from .models import Product, Order, OrderProduct, ShoppingCart, ShoppingCartProduct, Category


# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    admin.site.register(Product)


class OrderAdmin(admin.ModelAdmin):
    exclude = ["user", "order_number"]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Order, OrderAdmin)


class OrderProductAdmin(admin.ModelAdmin):
    admin.site.register(OrderProduct)


class ShoppingCartAdmin(admin.ModelAdmin):
    readonly_fields = ["user"]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        # Check if the user already has a shopping cart
        user_has_cart = ShoppingCart.objects.filter(user=request.user).exists()
        return not user_has_cart


admin.site.register(ShoppingCart, ShoppingCartAdmin)


class ShoppingCartProductAdmin(admin.ModelAdmin):
    admin.site.register(ShoppingCartProduct)


class CategoryAdmin(admin.ModelAdmin):
    admin.site.register(Category)

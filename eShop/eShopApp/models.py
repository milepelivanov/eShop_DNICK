from django.db import models
from django.contrib.auth.models import User
import random
import string


# PRODUCT
# CATEGORY
# SHOPPING CART
# ORDER
# Create your models here.

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('customer', 'Buyer'),
        ('seller', 'Seller'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='regular')


class Category(models.Model):
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    SEX = [("M", "Male"),
            ("F", "Female"),
            ("U", "Unisex"),
            ]
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    price = models.IntegerField()
    img = models.URLField(max_length=255)
    stock = models.IntegerField()
    color = models.CharField(max_length=255)
    sex = models.CharField(max_length=1, choices=SEX)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("custom_add_product", "Can add product"),
            ("custom_edit_product", "Can edit product"),
            ("custom_delete_product", "Can delete product")
            
        ]

    def __str__(self):
        return self.name + " " + self.desc + " " + str(self.price)


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class ShoppingCartProduct(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return str(self.shopping_cart) + " " + str(self.product)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField()
    address = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_random_order_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user) + " " + self.order_number


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return str(self.order) + " " + str(self.price)

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class ProductCategory(models.Model):
    id = models.AutoField(),
    name = models.CharField(max_length=60)


class ProductBrand(models.Model):
    id = models.AutoField(),
    name = models.CharField(max_length=60)


class Product(models.Model):
    id = models.AutoField()
    name = models.CharField(max_length=60, null=False)
    brand = models.ForeignKey(ProductBrand, on_delete=models.SET_NULL)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL)
    image = models.TextField(null=True)
    price = models.FloatField(null=False)


class User(AbstractUser):
    id = models.AutoField()
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)


class Checkout(models.Model):
    reference = models.UUIDField(null=False)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL)
    auth_code = models.CharField(max_length=20, null=True)
    payment_service = models.CharField(max_length=30, null=False)
    total = models.IntegerField()


class CheckoutProductsInfo(models.Model):
    id = models.AutoField()
    checkout = models.ForeignKey(Checkout, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL)
    quantity = models.IntegerField(null=False)
    sub_total = models.FloatField(null=False)


class Order(models.Model):
    id = models.AutoField()
    reference = models.UUIDField(null=False)
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)

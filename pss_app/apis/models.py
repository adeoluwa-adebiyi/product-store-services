from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class ProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)


class ProductBrand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, null=False)
    brand = models.ForeignKey(ProductBrand, on_delete=models.SET_NULL,null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    image = models.TextField(null=True)
    price = models.FloatField(null=False)


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)


class Checkout(models.Model):
    id = models.AutoField(primary_key=True)
    reference = models.UUIDField(null=False)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment_service = models.CharField(max_length=30, null=False)
    total = models.FloatField()


class CheckoutProductsInfo(models.Model):
    id = models.AutoField(primary_key=True)
    checkout = models.ForeignKey(Checkout, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=False)
    sub_total = models.FloatField(null=False)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    reference = models.UUIDField(null=False)
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, null=True)
    payment_status = models.BooleanField(default=False)
    access_code = models.CharField(max_length=20, null=True)
    payment_details = models.ForeignKey("PaymentDetails", on_delete=models.SET_NULL, null=True)


class PaymentDetails(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_id = models.CharField(max_length=20, null=False)
    reference = models.CharField(max_length=40)
    json_dump = models.TextField()
    payment_gateway = models.CharField(max_length=20)

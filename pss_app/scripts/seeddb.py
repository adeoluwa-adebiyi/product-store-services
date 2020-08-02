from apis.models import ProductCategory, ProductBrand, Product
from faker import Faker
import random

faker = Faker()


def seed_product_categories():
    models = []
    for i in range(0,5):
        model = ProductCategory.objects.create(name=faker.name())
        models.append(model)
    return models


def seed_products():
    product_cat = seed_product_categories()
    product_brands = seed_product_brands()
    models = []
    for i in range(0, 100):
        model = Product.objects.create(name=faker.name(), brand=product_brands[i%5], category=product_cat[i%5],
                                       image="", price=random.randint(0, 200))
        models.append(model)
    return models


def seed_product_brands():
    models = []
    for i in range(0, 10):
        model = ProductBrand.objects.create(name=faker.company())
        models.append(model)
    return models


def run():
    seed_products()
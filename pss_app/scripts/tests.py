from unittest import TestCase
from .seeddb import seed_products, seed_product_brands, seed_product_categories
from apis.models import Product, ProductCategory, ProductBrand


class SeedProductsTestCase(TestCase):

    def setUp(self):
        Product.objects.all().delete()

    def test_seed_products(self):
        self.assertEquals(seed_products(), list(Product.objects.all()))

    def doCleanups(self):
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()
        ProductBrand.objects.all().delete()


class SeedProductCategoriesTestCase(TestCase):

    def setUp(self):
        ProductCategory.objects.all().delete()

    def test_seed_product_categories(self):
        self.assertEquals(seed_product_categories(), list(ProductCategory.objects.all()))

    def doCleanups(self):
        ProductCategory.objects.all().delete()


class SeedProductBrandsTestCase(TestCase):

    def setUp(self):
        ProductBrand.objects.all().delete()

    def test_seed_products_brands(self):
        self.assertEquals(seed_product_brands(), list(ProductBrand.objects.all()))

    def doCleanups(self):
        ProductBrand.objects.all().delete()

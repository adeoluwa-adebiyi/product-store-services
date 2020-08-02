import json

import graphene
from django.test import TestCase, Client

# Create your tests here.
from apis.usecases.products.products import fetch_products_by_category, fetch_category_listing
from apis.models import ProductCategory, Product
from graphene_django.utils import GraphQLTestCase
from scripts.seeddb import seed_products
from apis.serializers import ProductSerializer, ProductCategorySerializer
from apis.views import RootQuery


class ProductsUseCasesTestCase(TestCase):

    def setUp(self):
        seed_products()
        pass

    def test_fetch_products_by_category(self):
        category = ProductCategory.objects.first()
        queryset = fetch_products_by_category(category=category.name)
        self.assertEquals(len(queryset), 10)
        self.assertEquals(ProductSerializer(Product.objects.filter(category=category)[:10],many=True).data,
                          ProductSerializer(queryset, many=True).data)

    def test_fetch_category_listing(self):
        categories = ProductCategory.objects.all()
        queryset = fetch_category_listing()
        self.assertEquals(len(queryset), len(categories))
        self.assertEquals(ProductCategorySerializer(categories, many=True).data,
                          ProductCategorySerializer(queryset, many=True).data)


class GetProductsByCategoryTestCase(TestCase):

    def setUp(self):
        seed_products()

    def test_fetch_products_by_category_query(self):
        schema = graphene.Schema(query=RootQuery)
        query = """
            query GetProductsQuery($category: String!, $page: Int!){
                  getProducts(category: $category, page:$page) {
                    brand
                    category{
                      name
                    }
                    name
                    image
                    price
                  }
            }
        """
        result = schema.execute(query, variables={"category": ProductCategory.objects.first().name, "page":1})
        self.assertIsNotNone(result)
        print(result.data)
        self.assertTrue(len(result.data["getProducts"]), 10)


class FetchProductCategoryTestCase(TestCase):

    def setUp(self):
        seed_products()

    def test_fetch_product_categories_query(self):
        schema = graphene.Schema(query=RootQuery)
        query = """
              query ListAllCategories{
                allProductCategories{
                  name
                }
              }
        """
        result = schema.execute(query)
        self.assertIsNotNone(result.data)
        print(result.data)
        self.assertTrue(len(result.data["allProductCategories"]), 10)

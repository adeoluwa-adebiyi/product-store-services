import json
from random import Random

import graphene
from django.test import TestCase, Client

# Create your tests here.
from apis.usecases.products.products import fetch_products_by_category, fetch_category_listing
from apis.models import ProductCategory, Product, Checkout, User, CheckoutProductsInfo
from graphene_django.utils import GraphQLTestCase
from scripts.seeddb import seed_products
from apis.serializers import ProductSerializer, ProductCategorySerializer
from apis.views import RootQuery

from apis.usecases.checkout.checkout import CheckoutService

from apis.usecases.payment.payment_services import PaystackPaymentService

from apis.models import Order

from apis.usecases.orders.orders import OrderService

from apis.queries.checkout import RootMutation


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


class CreateCheckoutTestCase(TestCase):

    def setUp(self):
        User.objects.create_superuser(first_name="Tom", last_name="Clancy",username="t_clancy", email="deeman24@yahoo.com", password="admin1234")
        seed_products()

    def create_test_purchasable_from_products(self, products=None):
        if products is None:
            return json.dumps({
                "data": {
                    "checkout": None
                }
            })
        return json.dumps({
            "data": {
                "checkout": [
                    {
                        "id": product.id,
                        "quantity": Random().randint(1, 4)
                    } for product in products
                ]
            }
        })

    def get_total_price_of_checkout(self, checkout=None):
        return CheckoutService().get_total_price_of_checkout(checkout=checkout)

    def get_sum_checkout_info_sub_totals(self, checkout_product_infos=[]):
        if checkout_product_infos is None:
            raise Exception("checkout product infos cannot be null")
        sum = 0
        for item in checkout_product_infos:
            sum += item.sub_total

        return sum

    def test_create_checkout(self):
        data = json.loads(self.create_test_purchasable_from_products(products=Product.objects.all()[:5]))
        self.assertEquals(len([Product.objects.get(id=item["id"]) for item in data["data"]["checkout"]]), 5)
        self.assertTrue(isinstance(CheckoutService(payment_service=PaystackPaymentService(api_key="HDJBDJBD")).create_checkout(data=data, user=User.objects.all().first()), Checkout))
        checkout = CheckoutService(payment_service=PaystackPaymentService(api_key="HDJBDJBD")).create_checkout(data=data, user=User.objects.all().first())
        self.assertEquals(checkout.total, self.get_total_price_of_checkout(checkout=data["data"]["checkout"]))
        checkout_product_infos = CheckoutProductsInfo.objects.filter(checkout=checkout)
        self.assertEquals([item.product.id for item in checkout_product_infos], [item["id"] for item in data["data"]["checkout"]])
        self.assertEquals(self.get_sum_checkout_info_sub_totals(checkout_product_infos=checkout_product_infos), checkout.total)

    def test_create_order(self):
        data = json.loads(self.create_test_purchasable_from_products(products=Product.objects.all()[:5]))
        checkout = CheckoutService(payment_service=PaystackPaymentService(api_key="HDJBDJBD")).create_checkout(data=data, user=User.objects.all().first())
        order_service = OrderService(payment_service=PaystackPaymentService(api_key="HDJBDJBD"))
        self.assertTrue(isinstance(order_service.create_order(checkout=checkout), Order))

    def test_checkout_api(self):
        data = self.create_test_purchasable_from_products(products=Product.objects.all()[:5])
        schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
        query = """
                    mutation CheckoutPurchasables($data: String!){
                          checkout(data: $data) {
                            order{
                                reference
                                accessCode
                            }
                        }
                    }
                """
        result = schema.execute(query, variables={"data": data})
        self.assertIsNotNone(result.data)
        self.assertIsNotNone(result.data["checkout"]["order"]["reference"])
        self.assertTrue(isinstance(result.data["checkout"]["order"]["reference"], str) and result.data["checkout"]["order"]["reference"] != "")
        self.assertIsNotNone(result.data["checkout"]["order"]["accessCode"])
        self.assertTrue(isinstance(result.data["checkout"]["order"]["accessCode"], str) and result.data["checkout"]["order"]["accessCode"] != "")
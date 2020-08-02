from graphene import ObjectType
import graphene
from apis.serializers import ProductSerializer
from apis.usecases.products.products import fetch_products_by_category, fetch_category_listing
from apis.models import Product, ProductCategory, ProductBrand
from graphene_django import DjangoObjectType


class CategoryType(ObjectType):
    name = graphene.String()


class BrandType(DjangoObjectType):
    class Meta:
        model = ProductBrand


class ProductsType(ObjectType):
    id = graphene.Int()
    name = graphene.String()
    image = graphene.String()
    brand = graphene.String()
    category = graphene.Field(CategoryType)
    price = graphene.Float()


class ProductQuery(object):

    getProducts = graphene.List(ProductsType, category=graphene.String(), page=graphene.Int())

    allProductCategories = graphene.List(CategoryType)

    def resolve_getProducts(self, info, **kwargs):
        result = fetch_products_by_category(**kwargs)
        result = [
            ProductsType(id=prod.id,
                         name=prod.name,
                         image=prod.image,
                         brand=prod.brand.name,
                         category=CategoryType(name=prod.category.name),
                         price=prod.price)
            for prod in result
        ]
        return result

    def resolve_allProductCategories(self, info, **kwargs):
        result = fetch_category_listing()
        return result

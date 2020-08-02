from rest_framework.serializers import ModelSerializer
from apis.models import Product, ProductCategory, ProductBrand


class ProductCategorySerializer(ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class ProductBrandSerializer(ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ["id"]

    category = ProductCategorySerializer()
    brand = ProductBrandSerializer()

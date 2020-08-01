from apis.models import ProductCategory, Product
from django.core.paginator import Paginator


def fetch_products_by_category(category=None, page=1, page_size=10):
    assert (category is not None)
    product_category = ProductCategory.objects.get(name=category)
    products_queryset = Product.objects.filter(category=product_category)
    paginator = Paginator(products_queryset, per_page=page_size)
    return paginator.page(page)


def fetch_category_listing():
    return ProductCategory.objects.all()

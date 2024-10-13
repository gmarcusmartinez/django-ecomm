import factory
from ecommerce.product.models import Brand, Category, Product, ProductLine


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = "test_brand"


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.sequence(lambda n: f"Category_{n}")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    description = "test_description"
    is_active = True
    is_digital = False
    name = "test_product"
    slug = factory.sequence(lambda n: f"test-slug-{n}")


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    is_active = True
    price = 100
    product = factory.SubFactory(ProductFactory)
    sequence = 1
    sku = factory.sequence(lambda n: f"sku-{n}")
    stock_qty = 10

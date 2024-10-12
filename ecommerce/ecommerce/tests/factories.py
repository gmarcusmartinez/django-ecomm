import factory
from ecommerce.product.models import Brand, Category, Product


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

    name = "test_product"
    description = "test_description"
    is_digital = False
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from ecommerce.product.fields import OrderField


class ActiveQuerySet(models.QuerySet):
    def isactive(self):
        return self.filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=255, unique=True)
    parent = TreeForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey('Category', null=True,
                              blank=True, on_delete=models.SET_NULL)

    objects = ActiveQuerySet.as_manager()

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    is_active = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=255)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_line")
    sequence = OrderField(unique_for_field="product", blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.stock_qty}"

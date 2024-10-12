from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


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
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey('Category', null=True,
                              blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    is_active = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=255)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

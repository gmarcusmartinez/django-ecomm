from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.core.exceptions import ValidationError
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
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey('Category', null=True,
                              blank=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    is_digital = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    objects = ActiveQuerySet.as_manager()

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    is_active = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_line")
    sequence = OrderField(unique_for_field="product", blank=True)
    sku = models.CharField(max_length=255)
    stock_qty = models.IntegerField()

    def clean(self):
        qs = ProductLine.objects.filter(product=self.product_id)
        for obj in qs:
            if self.id != obj.id and self.sequence == obj.sequence:
                raise ValidationError("Duplicate value.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self):
        return self.sku


class ProductImage(models.Model):
    alt_text = models.CharField(max_length=255)
    product_line = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image")
    sequence = OrderField(unique_for_field="product_line", blank=True)
    url = models.ImageField(upload_to=None, default="test.jpg")

    def clean(self):
        qs = ProductImage.objects.filter(product_line=self.product_line)
        for obj in qs:
            if self.id != obj.id and self.sequence == obj.sequence:
                raise ValidationError(
                    "Sequence must be unique per product line")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)

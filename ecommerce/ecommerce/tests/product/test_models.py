import pytest
from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db


class TestBrandModel:
    def test_str_method(self, brand_factory):
        data = brand_factory(name="nike")
        assert data.__str__() == "nike"


class TestCategoryModel:
    def test_str_method(self, category_factory):
        data = category_factory(name="clothes")
        assert data.__str__() == "clothes"


class TestProductModel:
    def test_str_method(self, product_factory):
        data = product_factory(name="hoodie")
        assert data.__str__() == "hoodie"


class TestProductLineModel:
    def test_str_method(self, product_line_factory):
        data = product_line_factory(sku="sku-1")
        assert data.__str__() == "sku-1"

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(product=obj, sequence=1)
        with pytest.raises(ValidationError):
            product_line_factory(product=obj, sequence=1).clean()

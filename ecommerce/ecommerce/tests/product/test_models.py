import pytest

pytestmark = pytest.mark.django_db


class TestBrandModel:
    def test_str_method(self, brand_factory):
        # Arrange & Act
        data = brand_factory(name="nike")
        # Assert
        assert data.__str__() == "nike"


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Arrange & Act
        data = category_factory(name="clothes")
        # Assert
        assert data.__str__() == "clothes"


class TestProductModel:
    def test_str_method(self, product_factory):
        data = product_factory(name="hoodie")
        assert data.__str__() == "hoodie"

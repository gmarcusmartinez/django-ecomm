import pytest

pytestmark = pytest.mark.django_db


class TestBrandModel:
    def test_str_method():
        # Arrange
        # Act
        # Assert
        pass


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Arrange & Act
        data = category_factory()
        # Assert
        assert data.__str__() == "test_category"

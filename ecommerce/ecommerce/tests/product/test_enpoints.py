import pytest
import json

pytestmark = pytest.mark.django_db


class TestBrandEndpoints:
    endpoint = '/api/brand/'

    def test_get_brands(self, brand_factory, client):
        brand_factory.create_batch(3)
        response = client.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3


class TestCategoryEndpoints:
    endpoint = '/api/category/'

    def test_get_categories(self, category_factory, client):
        category_factory.create_batch(3)
        response = client.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3


class TestProductEndpoints:
    endpoint = '/api/product/'

    def test_get_products(self, product_factory, client):
        product_factory.create_batch(3)
        response = client.get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

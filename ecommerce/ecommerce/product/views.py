from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from .models import Brand, Category, Product
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer


class BrandViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all brands
    """
    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all categories
    """
    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    queryset = Product.objects.all().isactive()
    lookup_field = 'slug'

    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(self.queryset.filter(
            slug=slug).select_related("category", "brand"), many=True)
        return Response(serializer.data)

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        """
         A simple Viewset for viewing all brands
        """
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path=r"category/(?P<category>\w+)/all")
    def list_products_by_category(self, request, category=None):
        """
         An endpoint to list all products by category
        """
        serializer = ProductSerializer(
            self.queryset.filter(category__name=category), many=True)
        return Response(serializer.data)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.db.models import Avg

from . import models
from . import serializers


# Category
class CategoryListAPIView(APIView):

    def get(self, request):
        categories = models.Category.objects.annotate(
            products_count=Count('products')
        )

        data = serializers.CategorySerializer(
            categories,
            many=True
        ).data

        return Response(data=data)

    def post(self, request):
        serializer = serializers.CategorySerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


class CategoryDetailAPIView(APIView):

    def get_object(self, id):
        return models.Category.objects.filter(id=id).first()

    def get(self, request, id):
        category = self.get_object(id)

        if not category:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        data = serializers.CategorySerializer(
            category
        ).data

        return Response(data=data)

    def put(self, request, id):
        category = self.get_object(id)

        if not category:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = serializers.CategorySerializer(
            category,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)

    def delete(self, request, id):
        category = self.get_object(id)

        if not category:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        category.delete()

        return Response(
            {"message": "Category deleted"}
        )


# Product
class ProductListAPIView(APIView):

    def get(self, request):
        products = models.Product.objects.select_related(
            'category'
        ).all()

        data = serializers.ProductSerializer(
            products,
            many=True
        ).data

        return Response(data=data)

    def post(self, request):
        serializer = serializers.ProductSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


class ProductDetailAPIView(APIView):

    def get_object(self, id):
        return models.Product.objects.filter(id=id).first()

    def get(self, request, id):
        product = self.get_object(id)

        if not product:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        data = serializers.ProductSerializer(
            product
        ).data

        return Response(data=data)

    def put(self, request, id):
        product = self.get_object(id)

        if not product:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = serializers.ProductSerializer(
            product,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)

    def delete(self, request, id):
        product = self.get_object(id)

        if not product:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        product.delete()

        return Response(
            {"message": "product deleted"}
        )


# Review
class ReviewListAPIView(APIView):

    def get(self, request):
        reviews = models.Review.objects.select_related(
            'product'
        ).all()

        data = serializers.ReviewSerializer(
            reviews,
            many=True
        ).data

        return Response(data=data)

    def post(self, request):
        serializer = serializers.ReviewSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


class ReviewDetailAPIView(APIView):

    def get_object(self, id):
        return models.Review.objects.filter(id=id).first()

    def get(self, request, id):
        review = self.get_object(id)

        if not review:
            return Response(
                {"error": "Review not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        data = serializers.ReviewSerializer(
            review
        ).data

        return Response(data=data)

    def put(self, request, id):
        review = self.get_object(id)

        if not review:
            return Response(
                {"error": "Review not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = serializers.ReviewSerializer(
            review,
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)

    def delete(self, request, id):
        review = self.get_object(id)

        if not review:
            return Response(
                {"error": "Review not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        review.delete()

        return Response(
            {"message": "review deleted"}
        )


# Product Reviews
class ProductReviewsAPIView(APIView):

    def get(self, request):

        products = (
            models.Product.objects
            .prefetch_related('reviews')
            .annotate(
                rating=Avg('reviews__stars')
            )
        )

        data = serializers.ProductReviewSerializer(
            products,
            many=True
        ).data

        return Response(data=data)
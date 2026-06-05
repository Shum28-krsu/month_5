from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.db.models import Avg
from . import serializers
from . import models 

#Category
@api_view(['GET', 'POST'])
def category_list_api_view(request):

    if request.method == 'GET':
        categories = models.Category.objects.annotate(products_count=Count('products'))

        list_ = serializers.CategorySerializer( categories, many=True).data
        return Response(data=list_)

    elif request.method == 'POST':
        serializer = serializers.CategorySerializer( data=request.data  )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED  )
    
@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):

    try:
        category = models.Category.objects.get(id=id)
    except models.Category.DoesNotExist:
        return Response(
            data={'error': 'category not found!'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        data = serializers.CategorySerializer(category, many=False).data

        return Response(data=data)

    elif request.method == 'PUT':
        serializer = serializers.CategorySerializer( category, data=request.data )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)

    elif request.method == 'DELETE':
        category.delete()

        return Response( data={'message': 'category deleted'} )

#Product
@api_view(['GET', 'POST'])
def product_list_api_view(request):

    if request.method == 'GET':
        products = models.Product.objects.select_related( 'category' ).all()

        list_ = serializers.ProductSerializer( products, many=True ).data

        return Response(data=list_)

    elif request.method == 'POST':
        serializer = serializers.ProductSerializer( data=request.data )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):

    try:
        product = models.Product.objects.get(id=id)
    except models.Product.DoesNotExist:
        return Response(
            data={'error': 'product not found!'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        data = serializers.ProductSerializer( product, many=False ).data

        return Response(data=data)

    elif request.method == 'PUT':
        serializer = serializers.ProductSerializer( product, data=request.data )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)

    elif request.method == 'DELETE':
        product.delete()

        return Response(data={'message': 'product deleted'})

#Review
@api_view(['GET', 'POST'])
def review_list_api_view(request):

    if request.method == 'GET':
        reviews = models.Review.objects.select_related('product').all()

        list_ = serializers.ReviewSerializer( reviews, many=True ).data

        return Response(data=list_)

    elif request.method == 'POST':
        serializer = serializers.ReviewSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):

    try:
        review = models.Review.objects.get(id=id)
    except models.Review.DoesNotExist:
        return Response(
            data={'error': 'review not found!'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        data = serializers.ReviewSerializer( review, many=False ).data

        return Response(data=data)

    elif request.method == 'PUT':
        serializer = serializers.ReviewSerializer( review, data=request.data )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)

    elif request.method == 'DELETE':
        review.delete()

        return Response( data={'message': 'review deleted'}  )


@api_view(['GET'])
def product_reviews_api_view(request):
    
    products = models.Product.objects.prefetch_related('reviews').annotate(rating=Avg('reviews__stars'))

    list_ = serializers.ProductReviewSerializer( products, many=True ).data

    return Response(data=list_)
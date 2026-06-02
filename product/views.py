from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from . import models 

#Category
@api_view(['GET'])
def category_list_api_view(request):

    categories = models.Category.objects.all()

    list_ = serializers.CategorySerializer(categories, many=True).data

    return Response( data=list_ )

@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = models.Category.objects.get(id=id)
    except models.Category.DoesNotExist:
        return Response(
            data={'error': 'category not found!'},
            status=status.HTTP_404_NOT_FOUND
        )

    data = serializers.CategorySerializer(category, many=False).data

    return Response(data=data)


#Product
@api_view(['GET'])
def product_list_api_view(request):

    products = models.Product.objects.select_related('category').all()
   
    list_ = serializers.ProductSerializer(products, many=True).data

    return Response( data=list_ )

@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = models.Product.objects.get(id=id)
    except models.Product.DoesNotExist:
        return Response(
            data={'error': 'product not found!'},
            status=status.HTTP_404_NOT_FOUND
        )

    data = serializers.ProductSerializer(product, many=False).data

    return Response(data=data)

#Review
@api_view(['GET'])
def review_list_api_view(request):

    reviews = models.Review.objects.select_related('product').all()

    list_ = serializers.ReviewSerializer(reviews, many=True).data

    return Response( data=list_  )

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = models.Review.objects.get(id=id)
    except models.Review.DoesNotExist:
        return Response(
            data={'error': 'review not found!'},
            status=status.HTTP_404_NOT_FOUND
        )

    data = serializers.ReviewSerializer(review, many=False).data

    return Response(data=data)


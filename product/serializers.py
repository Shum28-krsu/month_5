from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'products_count']

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError("Category name must be at least 2 characters")

        if models.Category.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Category with this name already exists")

        return value


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = '__all__'

    def validate_title(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Product title is too short")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value

    def validate_category(self, value):
        if value is None:
            raise serializers.ValidationError("Category is required")

        if not models.Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Category does not exist")

        return value


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Review
        fields = '__all__'

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Stars must be between 1 and 5")
        return value

    def validate_product(self, value):
        if not models.Product.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Product does not exist")
        return value


class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.FloatField()

    class Meta:
        model = models.Product
        fields = ['id', 'title', 'description', 'price', 'rating', 'reviews']
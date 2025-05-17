from rest_framework import serializers
from .models import *

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'  # 序列化所有字段，也可以指定特定字段


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  # 序列化所有字段，也可以指定特定字段


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'  # 序列化所有字段，也可以指定特定字段

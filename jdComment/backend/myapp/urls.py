from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'productCategory', ProductCategoryViewSet, basename='productCategory')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'productReview', ProductReviewViewSet, basename='productReview')

urlpatterns = [
    path('', include(router.urls)),  # 生成通用 CRUD 路由
]

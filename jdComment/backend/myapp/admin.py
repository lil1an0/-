from django.contrib import admin
from myapp.models import *


def get_all_fields(model):
    return [field.name for field in model._meta.get_fields()]


class DbProduct(admin.ModelAdmin):
    list_display = get_all_fields(Product)
    list_per_page = 20


class DbProductCategory(admin.ModelAdmin):
    list_display = get_all_fields(ProductCategory)
    list_per_page = 20


class DbProductReview(admin.ModelAdmin):
    list_display = get_all_fields(ProductReview)
    list_per_page = 20


admin.site.register(Product, DbProduct)
admin.site.register(ProductCategory, DbProductCategory)
admin.site.register(ProductReview, DbProductReview)


admin.site.site_header = "基于网络爬虫的京东用户评论分析及可视化设计"

from django.db import models

member_list = [
    {"name": "会员", "value": 12164},
    {"name": "非会员", "value": 33010},
]

class ProductCategory(models.Model):
    category_id = models.CharField(max_length=10, primary_key=True)  # 使用 CharField 以便存储类似 "CATE_0" 这样的字符串
    category_name = models.CharField(max_length=255)  # 类别名称

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_id = models.CharField(max_length=50, primary_key=True)  # 商品ID，作为主键
    product_name = models.TextField()
    categories = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.product_name


class ProductReview(models.Model):
    """Product review model"""
    data_id = models.CharField(max_length=50, unique=True)
    user_id = models.FloatField(verbose_name="User ID")
    product_id = models.CharField(max_length=50, verbose_name="Product ID")
    review_timestamp = models.IntegerField(verbose_name="Review Timestamp")
    review_time = models.DateTimeField(verbose_name="Review Time")
    review_title = models.CharField(max_length=255)
    review_content = models.TextField()
    rating = models.FloatField()
    label = models.CharField(max_length=10)

    def __str__(self):
        return f'Review for {self.product_id} by User {self.user_id}'

    class Meta:
        # 设置表名
        db_table = 'product_reviews'  # 在数据库中保存为 'product_reviews' 表
        # 可以根据需要添加索引，优化查询性能
        indexes = [
            models.Index(fields=['product_id']),
            models.Index(fields=['user_id']),
        ]
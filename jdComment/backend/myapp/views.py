from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db import connection
import random
from collections import defaultdict
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import jieba
from collections import Counter
from functools import lru_cache
from application.settings import BASE_DIR
from .chatPredict import sentiment_predict

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from datetime import datetime, timedelta

cursor = connection.cursor()


file_path = str(BASE_DIR) + "/哈工大停用词表.txt"

def load_stopwords(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        stopwords = set([line.strip() for line in f.readlines()])
    return stopwords


def preprocess_text(text, stopwords):
    words = jieba.cut(text)
    return [word for word in words if word not in stopwords and len(word) > 1]


stopwords = load_stopwords(file_path)

word_cloud_cache = {}


def wordCloud(comments, n):
    comments_hash = hash(comments.to_string()) 
    if comments_hash in word_cloud_cache:
        return word_cloud_cache[comments_hash]
    comments_cleaned = comments.apply(lambda x: preprocess_text(x, stopwords))
    all_words = [word for comment in comments_cleaned for word in comment]
    word_counts = Counter(all_words)
    result = [{"name": word, "value": count} for word, count in word_counts.most_common(n)]
    word_cloud_cache[comments_hash] = result
    return result





class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = '__all__'
    search_fields = '__all__'
    ordering_fields = '__all__'
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = '__all__'
    search_fields = '__all__'
    ordering_fields = '__all__'



class ProductReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = '__all__'
    search_fields = '__all__'
    ordering_fields = '__all__'


    @action(detail=False, methods=['get'], url_path='get_data')
    def get_data(self, request):
        sql = """
            select 
                a.user_id , a.product_id , b.product_name,
                a.review_time , a.review_title , a.review_content, a.rating , a.label 
            from product_reviews a 
            left join myapp_product b on a.product_id = b.product_id 
            order by a.review_time desc
        """
        cursor.execute(sql)
        fetch_result = cursor.fetchall()
        columns = ['用户ID', '商品ID', '评论时间', '评论标题', '评论内容', '评分', '评价标签']
        fields = [
            'user_id', 'product_id', 'product_name',
            'review_time', 'review_title', 'review_content', 'rating', 'label'
        ]
        result = []
        for _ in fetch_result[:100]:
            # print(_)
            result.append(dict(zip(fields, _)))
        return Response({
            "data": result
        })

    
    @action(detail=False, methods=['get'], url_path='get_sentiment')
    def get_sentiment(self, request):
        sql1 = """
            select 
                a.label, count(1) cnt
            from product_reviews a 
            group by 1 
        """
        cursor.execute(sql1)
        fetch_result1 = cursor.fetchall()
        sql1_result = []
        for _ in fetch_result1:
            sql1_result.append({
                "name": _[0],
                "value": _[1]
            })

        sql2 = """
            select 
                a.label, date_format(review_time, '%Y-%m-%d') , count(1) cnt
            from product_reviews a 
            group by 1 ,2
            order by 1,2 asc
        """
        cursor.execute(sql2)
        fetch_result2 = cursor.fetchall()
        good, midele, bad = [], [], []
        good_day, midele_day, bad_day = [], [], []
        for _ in fetch_result2: 
            if _[0] == "好评":
                good.append(_[2])
                good_day.append(_[1])
            elif _[0] == "中评":
                midele.append(_[2])
                midele_day.append(_[1])
            else:
                bad.append(_[2])
                bad_day.append(_[1])

        max_length = max(len(good_day), len(midele_day), len(bad_day))

        # 补充列表的函数（前向填充）
        def forward_fill(lst, max_len):
            while len(lst) < max_len:
                lst.append(lst[-1])  # 用最后一个有效值填充
            return lst

        # 对日期列表和内容列表进行补充
        good_day = forward_fill(good_day, max_length)
        midele_day = forward_fill(midele_day, max_length)
        bad_day = forward_fill(bad_day, max_length)

        good = forward_fill(good, max_length)
        midele = forward_fill(midele, max_length)
        bad = forward_fill(bad, max_length)

        # 计算好评率
        total_reviews = [g + m + b for g, m, b in zip(good, midele, bad)]
        good_rates = [g / t if t > 0 else 0 for g, t in zip(good, total_reviews)]

        # 只用最近3个月的历史数据
        if good_day:
            last_date = datetime.strptime(good_day[-1], '%Y-%m-%d')
            three_months_ago = last_date - timedelta(days=60)
            start_idx = 0
            for i, d in enumerate(good_day):
                if datetime.strptime(d, '%Y-%m-%d') >= three_months_ago:
                    start_idx = i
                    break
            history_dates = good_day[start_idx:]
            history_rates = good_rates[start_idx:]
        else:
            history_dates = good_day
            history_rates = good_rates

        # 预测未来
        future_steps = 30
        X = np.array(range(len(history_rates))).reshape(-1, 1)
        y = np.array(history_rates)
        X_future = np.array(range(len(history_rates), len(history_rates) + future_steps)).reshape(-1, 1)

        # 多项式回归
        poly = PolynomialFeatures(degree=3)
        X_poly = poly.fit_transform(X)
        X_poly_future = poly.transform(X_future)
        poly_model = LinearRegression()
        poly_model.fit(X_poly, y)
        poly_pred_future = poly_model.predict(X_poly_future)

        # 岭回归
        ridge_model = Ridge(alpha=1.0)
        ridge_model.fit(X, y)
        ridge_pred_future = ridge_model.predict(X_future)

        # 生成未来日期
        if history_dates:
            last_date = datetime.strptime(history_dates[-1], '%Y-%m-%d')
            future_dates = [(last_date + timedelta(days=i+1)).strftime('%Y-%m-%d') for i in range(future_steps)]
        else:
            future_dates = []

        # 拼接历史和预测，方便前端连线
        all_dates = history_dates + future_dates
        all_poly_pred = history_rates + poly_pred_future.tolist()
        all_ridge_pred = history_rates + ridge_pred_future.tolist()
        split_index = len(history_rates) - 1

        reviews_list = list(ProductReviewViewSet.queryset.values())
        df = pd.DataFrame(reviews_list)
        good_comment = df[df.label == "好评"]["review_content"]
        middle_comment = df[df.label == "中评"]["review_content"]
        bad_comment = df[df.label == "差评"]["review_content"]

        good_wordcloud = wordCloud(good_comment, 20)
        middle_wordcloud = wordCloud(middle_comment, 20)
        bad_wordcloud = wordCloud(bad_comment, 20)

        return Response({
            "result1": sql1_result,
            "result2":{
                "columns": good_day,
                "data": [
                    good, midele, bad
                ]
            },
            "result3":{
                "good": good_wordcloud,
                "middle": middle_wordcloud,
                "bad": bad_wordcloud
            },
            "result4": {
                "history_dates": history_dates,
                "history_rates": history_rates,
                "future_dates": future_dates,
                "poly_pred": poly_pred_future.tolist(),
                "ridge_pred": ridge_pred_future.tolist(),
                "all_dates": all_dates,
                "all_poly_pred": all_poly_pred,
                "all_ridge_pred": all_ridge_pred,
                "split_index": split_index
            }
        })
    
        


    @action(detail=False, methods=['get'], url_path='get_comments')
    def get_comments(self, request):
        sql1 = """
            select 
                date_format(review_time, '%Y-%m-%d') comment_date,
                count(1) cnt
            from product_reviews
            group by 1
            order by 1 asc
        """
        cursor.execute(sql1)
        fetch_result1 = cursor.fetchall()
        result1 = {
            "date": [],
            "counts": []
        } 
        for _ in fetch_result1:
            result1["date"].append(_[0])
            result1["counts"].append(_[1])

        print(result1)
        # 保留原始数据
        orig_dates = result1["date"]
        orig_counts = result1["counts"]



        # 将原始数据和预测数据合并
        combined_dates = orig_dates 
        combined_counts = orig_counts 
        result1 = {"date": combined_dates, "counts": combined_counts}
        reviews_list = list(ProductReviewViewSet.queryset.values())
        df = pd.DataFrame(reviews_list)
        comments = wordCloud(df["review_content"], 30)
        result2 = {
            "columns": [],
            "data": []
        }
        for _ in comments:
            result2["columns"].append(list(_.values())[0])
            result2["data"].append(list(_.values())[1])
  
        result3 = wordCloud(df["review_content"], 100)


        sql5 = """
            select 
                b.category_name, count(1) cnt
            from(
                select 
                    substring_index(b.categories, ',', 1) category_id , a.*
                from product_reviews a 
                left join myapp_product b on a.product_id = b.product_id 
            )a 
            left join myapp_productcategory b  on a.category_id = b.category_id
            group by 1
            order by 2 desc
        """

        cursor.execute(sql5)
        fetch_result5 = cursor.fetchall()
        sql5_result = []
        sql5_columns = []
        for _ in fetch_result5:
            sql5_columns.append(_[0])
            sql5_result.append({
                "name": _[0],
                "value": _[1]
            })

        return Response({
            "result1": result1,
            # "result1_forecast": forecast,
            "result2": result2,
            "result3": result3,
            "result4": member_list,
            "result5": sql5_result
        })

    


    @action(detail=False, methods=['post'], url_path='predict')
    def predict(self, request):
        input_content = request.data["content"]
        
        result = sentiment_predict(input_content)

        return Response({
            "data": result
        })



        

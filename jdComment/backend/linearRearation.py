import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score

# 1. 模拟数据生成
np.random.seed(42)
days = np.arange(1, 31)  # 30 天的数据
comments = 50 + 3 * days + np.random.normal(0, 10, size=len(days))  # 评论数 = 50 + 3 * 天数 + 噪声

# 将数据转换为 DataFrame
data = pd.DataFrame({
    'Day': days,
    'Comments': comments
})

# 2. 特征工程：增加日期衍生特征（例如，天数对应的周几）
data['Weekday'] = data['Day'] % 7  # 周几
data['Day_of_month'] = data['Day'] % 30  # 月中的天数

# 3. 准备数据
X = data[['Day', 'Weekday', 'Day_of_month']]  # 特征：天数、周几、月中的天数
y = data['Comments']  # 目标：评论数

# 标准化特征
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 4. 多项式回归
poly = PolynomialFeatures(degree=3)  # 使用三次多项式特征
X_poly_train = poly.fit_transform(X_train)
X_poly_test = poly.transform(X_test)

# 5. 训练带有岭回归的多项式回归模型
model = Ridge(alpha=1.0)  # L2 正则化，防止过拟合
model.fit(X_poly_train, y_train)

# 6. 预测
y_pred = model.predict(X_poly_test)

# 7. 评估模型
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"均方误差 (MSE): {mse:.2f}")
print(f"R² 分数: {r2:.2f}")

# 8. 交叉验证：评估模型的稳定性
cross_val_score_mean = np.mean(cross_val_score(model, X_poly_train, y_train, cv=5))
print(f"交叉验证得分: {cross_val_score_mean:.2f}")


# 10. 预测未来几天的评论数
future_days = np.array([[31, 31 % 7, 31 % 30], [32, 32 % 7, 32 % 30], [33, 33 % 7, 33 % 30]])  # 预测第 31、32、33 天的评论数
future_days_scaled = scaler.transform(future_days)  # 标准化
future_days_poly = poly.transform(future_days_scaled)  # 多项式特征转换
future_comments = model.predict(future_days_poly)
print(f"未来几天的预测评论数: {future_comments}")

import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from datetime import datetime
import os

# 路径配置
PUBLIC_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../rendering/public")
)
ORDERS_PATH = os.path.join(PUBLIC_DIR, "orders.json")
ORDER_ITEMS_PATH = os.path.join(PUBLIC_DIR, "order_items.json")
USERS_PATH = os.path.join(PUBLIC_DIR, "users.json")

# 输出文件
RFM_SCATTER_PATH = os.path.join(PUBLIC_DIR, "rfm_scatter.json")
RFM_RADAR_PATH = os.path.join(PUBLIC_DIR, "rfm_radar.json")
RFM_BUBBLE_PATH = os.path.join(PUBLIC_DIR, "rfm_bubble.json")

# 1. 读取数据
orders = pd.read_json(ORDERS_PATH)
order_items = pd.read_json(ORDER_ITEMS_PATH)
users = pd.read_json(USERS_PATH)

# 新增：计算每一行明细的金额
order_items["amount"] = order_items["price"] * order_items["quantity"]

# 2. 合并订单和订单明细，计算每个订单总金额
total_amount = order_items.groupby("order_id")["amount"].sum().reset_index()
orders = orders.merge(
    total_amount, on="order_id", how="left", suffixes=("", "_orderitem")
)
orders["amount"] = orders["amount"].fillna(0)

# 3. 计算 RFM 指标
# R: 距离最近一次消费的天数
# F: 订单数
# M: 消费总额
now = pd.to_datetime(orders["order_date"]).max() + pd.Timedelta(days=1)
rfm = (
    orders.groupby("user_id")
    .agg(
        {
            "order_date": lambda x: (now - pd.to_datetime(x).max()).days,
            "order_id": "count",
            "amount": "sum",
        }
    )
    .reset_index()
    .rename(
        columns={"order_date": "recency", "order_id": "frequency", "amount": "monetary"}
    )
)

# 4. 标准化
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[["recency", "frequency", "monetary"]])

# 5. KMeans 聚类
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
rfm["cluster"] = kmeans.fit_predict(rfm_scaled)

# 6. t-SNE 降维
tsne = TSNE(n_components=2, random_state=42)
tsne_result = tsne.fit_transform(rfm_scaled)
rfm["x"] = tsne_result[:, 0]
rfm["y"] = tsne_result[:, 1]

# 7. 输出 rfm_scatter.json
data_scatter = rfm[["user_id", "x", "y", "cluster"]].to_dict(orient="records")
with open(RFM_SCATTER_PATH, "w", encoding="utf-8") as f:
    json.dump(data_scatter, f, ensure_ascii=False, indent=2)

# 8. 输出 rfm_radar.json（每个集群的均值，标准化后）
rfm["recency_z"] = rfm_scaled[:, 0]
rfm["frequency_z"] = rfm_scaled[:, 1]
rfm["monetary_z"] = rfm_scaled[:, 2]
radar = (
    rfm.groupby("cluster")
    .agg({"recency_z": "mean", "frequency_z": "mean", "monetary_z": "mean"})
    .reset_index()
    .rename(
        columns={
            "recency_z": "recency",
            "frequency_z": "frequency",
            "monetary_z": "monetary",
        }
    )
)
data_radar = radar.to_dict(orient="records")
with open(RFM_RADAR_PATH, "w", encoding="utf-8") as f:
    json.dump(data_radar, f, ensure_ascii=False, indent=2)

# 9. 输出 rfm_bubble.json（原始 RFM + cluster）
data_bubble = rfm[["user_id", "recency", "frequency", "monetary", "cluster"]].to_dict(
    orient="records"
)
with open(RFM_BUBBLE_PATH, "w", encoding="utf-8") as f:
    json.dump(data_bubble, f, ensure_ascii=False, indent=2)

print("RFM 数据提取与聚类完成！")

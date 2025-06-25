import pandas as pd
import json
import os
import itertools

# 路径配置
PUBLIC_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../rendering/public")
)
ORDER_ITEMS_PATH = os.path.join(PUBLIC_DIR, "order_items.json")
PRODUCTS_PATH = os.path.join(PUBLIC_DIR, "products.json")
COOCCURRENCE_PATH = os.path.join(PUBLIC_DIR, "category_cooccurrence.json")

# 读取数据
order_items = pd.read_json(ORDER_ITEMS_PATH)
products = pd.read_json(PRODUCTS_PATH)

# 构建产品ID到品类的映射
gid2cat = products.set_index("product_id")["category"].to_dict()

# 每个订单的所有品类集合
grouped = order_items.groupby("order_id")["product_id"].apply(list)
cooccur = {}
for prod_list in grouped:
    cats = list(set(gid2cat.get(pid, "未知") for pid in prod_list))
    # 统计两两组合
    for c1, c2 in itertools.combinations_with_replacement(cats, 2):
        key = tuple(sorted([c1, c2]))
        cooccur[key] = cooccur.get(key, 0) + 1

# 转为json格式
result = [{"cat1": k[0], "cat2": k[1], "count": v} for k, v in cooccur.items()]

with open(COOCCURRENCE_PATH, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("品类共现矩阵已生成：", COOCCURRENCE_PATH)

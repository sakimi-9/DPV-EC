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
dict_prod_cat = dict(zip(products["product_id"], products["category"]))

# 为每个订单分配品类集合
order_items["category"] = order_items["product_id"].map(dict_prod_cat)
order_cat = (
    order_items.groupby("order_id")["category"]
    .apply(lambda x: set(x.dropna()))
    .reset_index()
)

# 统计品类两两共现
cooccur = {}
for cats in order_cat["category"]:
    cats = list(cats)
    for c1, c2 in itertools.combinations(sorted(cats), 2):
        key = (c1, c2)
        cooccur[key] = cooccur.get(key, 0) + 1

# 转为列表格式
data = [{"cat1": k[0], "cat2": k[1], "count": v} for k, v in cooccur.items()]

# 保存为 json
with open(COOCCURRENCE_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("品类共现矩阵已生成！")

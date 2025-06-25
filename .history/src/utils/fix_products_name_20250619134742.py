import json
import os

PUBLIC_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../rendering/public")
)
PRODUCTS_PATH = os.path.join(PUBLIC_DIR, "products.json")

with open(PRODUCTS_PATH, "r", encoding="utf-8") as f:
    products = json.load(f)

for prod in products:
    if not prod.get("name"):
        prod["name"] = prod.get("category", "")

with open(PRODUCTS_PATH, "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print("products.json 已修正，所有产品均有中文 name 字段！")

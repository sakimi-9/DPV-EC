import os
import pandas as pd

# 定义原始数据和清洗后数据的路径
data_dir = os.path.join(os.path.dirname(__file__), "D:/期末数据分析及可视化/src/data")
cleaned_dir = os.path.join(
    os.path.dirname(__file__), "D:/期末数据分析及可视化/src/data_cleaned"
)
os.makedirs(cleaned_dir, exist_ok=True)

# 文件名列表
files = [
    "users.csv",
    "orders.csv",
    "order_items.csv",
    "products.csv",
    "user_logs.csv",
]

# 日期/时间字段自动识别规则
DATE_KEYWORDS = ["date", "time", "day"]


def auto_parse_dates(df):
    for col in df.columns:
        if any(key in col.lower() for key in DATE_KEYWORDS):
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
            except Exception as e:
                print(f"字段 {col} 转换为日期失败: {e}")
    return df


def clean_file(filename):
    print(f"正在处理: {filename}")
    path = os.path.join(data_dir, filename)
    df = pd.read_csv(path)
    df = auto_parse_dates(df)
    # 简单缺失值处理：删除全空行，日期字段空值不做特殊处理
    df = df.dropna(how="all")
    # 可根据需要添加更多清洗逻辑
    cleaned_path = os.path.join(cleaned_dir, filename)
    df.to_csv(cleaned_path, index=False)
    print(f"已保存清洗后数据: {cleaned_path}")


if __name__ == "__main__":
    for f in files:
        clean_file(f)
    print("所有文件清洗完成！")

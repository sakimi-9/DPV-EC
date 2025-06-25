import os
import pandas as pd

# 定义清洗后数据的路径
data_cleaned_dir = os.path.join(os.path.dirname(__file__), "../data_cleaned/json")


# 遍历所有csv文件
def convert_all_csv_to_json():
    for filename in os.listdir(data_cleaned_dir):
        if filename.endswith(".csv"):
            csv_path = os.path.join(data_cleaned_dir, filename)
            json_path = os.path.join(
                data_cleaned_dir, filename.replace(".csv", ".json")
            )
            print(f"正在转换: {csv_path} -> {json_path}")
            df = pd.read_csv(csv_path)
            # pandas的to_json默认orient为columns，前端常用records
            df.to_json(json_path, orient="records", force_ascii=False, indent=2)
            print(f"已生成: {json_path}")


if __name__ == "__main__":
    convert_all_csv_to_json()
    print("所有CSV已转换为JSON！")

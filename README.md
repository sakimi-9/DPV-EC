# 电商数据分析及可视化项目

## 📝 项目简介

本项目是一个完整的电商数据分析与可视化解决方案，包含数据清洗、分析和Web可视化展示。项目采用Python进行数据处理分析，Vue3构建现代化的数据可视化仪表板。

## 🛠️ 技术栈

### 前端技术栈
- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - 类型安全的JavaScript超集
- **Vite** - 现代化的前端构建工具
- **ECharts 5.6** - 强大的数据可视化图表库
- **Bun** - 快速的JavaScript运行时和包管理器
- **Nginx** - 高性能Web服务器（生产环境）

### 后端数据处理
- **Python 3** - 数据处理和分析
- **Pandas** - 数据操作和分析库
- **NumPy** - 科学计算库
- **Scikit-learn** - 机器学习库（RFM聚类分析）

### 功能特性
- **RFM客户价值分析** - 客户细分和价值评估
- **销售趋势分析** - 月度销售数据趋势
- **用户行为分析** - 用户行为路径和转化分析
- **产品销售排行** - 热销产品排名
- **支付方式分析** - 支付偏好分析
- **地域消费分析** - 城市消费分布
- **品类关联分析** - 商品关联性热力图
- **年龄段消费分析** - 不同年龄段消费特征
- **性别消费对比** - 性别消费差异分析
- **用户留存分析** - 用户留存率统计


## 🚀 本地部署指南

### 前置要求
- Node.js 18+ 或 Bun
- Python 3.8+
- Git

### 方法1：前端开发模式

1. **克隆项目**
```bash
git clone https://github.com/sakimi-9/DPV-EC.git
cd src/rendering
```

2. **安装依赖**
```bash
# 使用 Bun（推荐）
bun install

# 或使用 npm
npm install
```

3. **启动开发服务器**
```bash
# 使用 Bun
bun run dev

# 或使用 npm
npm run dev
```

4. **访问应用**
打开浏览器访问：http://localhost:5173

### 方法2：数据处理 + 前端完整流程

1. **数据处理环境准备**
```bash
cd src/processing
pip install -r requirements.txt
```

2. **数据清洗**
```bash
python data_cleaning.py
```

3. **数据格式转换**
```bash
cd ../utils
python csv_to_json.py
python extract_rfm_data.py
python extract_category_cooccurrence.py
```

4. **启动前端**
```bash
cd ../rendering
bun install
bun run dev
```

### 方法3：生产环境构建

1. **构建前端**
```bash
cd src/rendering
bun run build
```

2. **预览构建结果**
```bash
bun run preview
```


## 🐳 Docker 部署(前端可视化部分)

### 方法1：使用预构建镜像
```bash
# 拉取镜像
docker pull sakimi9/ecommerce-analysis-frontend:latest

# 运行容器
docker run -d -p 8080:80 --name ecommerce-frontend sakimi9/ecommerce-analysis-frontend:latest
```

### 方法2：Docker Compose（推荐）
```bash
# 克隆项目
git clone https://github.com/sakimi-9/DPV-EC.git
cd src/rendering

# 使用 Docker Compose 启动
docker-compose up -d
```

### 方法3：本地构建镜像
```bash
cd src/rendering
docker build -t ecommerce-analysis-frontend .
docker run -d -p 8080:80 --name ecommerce-frontend ecommerce-analysis-frontend
```


## 📁 项目结构
```
电商数据分析及可视化/
├── src/
│   ├── data/                    # 原始数据文件
│   │   ├── users.csv           # 用户数据
│   │   ├── orders.csv          # 订单数据
│   │   ├── order_items.csv     # 订单明细
│   │   ├── products.csv        # 产品数据
│   │   └── user_logs.csv       # 用户行为日志
│   ├── data_cleaned/           # 清洗后的数据
│   │   ├── csv/               # CSV格式
│   │   └── json/              # JSON格式
│   ├── processing/             # 数据处理脚本
│   │   ├── data_cleaning.py   # 数据清洗
│   │   └── requirements.txt   # Python依赖
│   ├── rendering/              # 前端可视化项目
│   │   ├── src/
│   │   │   ├── components/    # Vue组件
│   │   │   ├── views/         # 页面视图
│   │   │   └── App.vue        # 主应用
│   │   ├── public/            # 静态资源
│   │   ├── Dockerfile         # Docker配置
│   │   └── package.json       # 前端依赖
│   └── utils/                  # 工具脚本
│       ├── csv_to_json.py     # 格式转换
│       ├── extract_rfm_data.py # RFM数据提取
│       └── extract_category_cooccurrence.py # 品类关联分析
├── images/                     # 项目截图
└── doc/                       # 文档
```

## 📋 访问应用

### 开发模式
- 前端开发服务器：http://localhost:5173
- 预览构建结果：http://localhost:4173

### 生产模式
- Docker容器访问：http://localhost:8080

## 🛠️ 容器管理命令
```bash
# 查看运行状态
docker ps

# 查看容器日志
docker logs ecommerce-frontend

# 停止容器
docker stop ecommerce-frontend

# 删除容器
docker rm ecommerce-frontend

# 使用 Docker Compose 管理
docker-compose ps          # 查看服务状态
docker-compose logs -f     # 查看实时日志
docker-compose down        # 停止所有服务
docker-compose up --build -d  # 重新构建并启动
```

## 📊 数据分析功能

### 核心分析模块
1. **月度销售趋势** - 展示销售额随时间变化趋势
2. **产品销售排行** - TOP销售产品排名
3. **用户行为分布** - 用户行为路径分析
4. **转化漏斗分析** - 用户转化率统计
5. **RFM客户价值分群** - 基于购买频率、金额、时间的客户细分
6. **RFM雷达图分析** - 各客户群体特征对比
7. **客户价值气泡图** - 客户价值分布可视化
8. **各品类销售额** - 产品类别销售对比
9. **品类关联热力图** - 商品购买关联性分析
10. **支付方式分布** - 支付偏好统计
11. **各年龄段消费能力** - 年龄与消费关系
12. **性别消费对比** - 性别消费差异
13. **用户留存分析** - 用户留存率趋势
14. **TOP10城市消费** - 地域消费分布

## 🔧 开发指南

### 添加新的数据分析视图

1. **在 `src/rendering/src/views/` 创建新的Vue组件**
2. **在 `src/rendering/src/App.vue` 中引入并注册组件**
3. **准备对应的数据文件到 `public/` 目录**
4. **使用ECharts进行图表渲染**

### 数据处理流程

1. **原始数据** (`src/data/`) → **数据清洗** (`src/processing/data_cleaning.py`)
2. **清洗后数据** (`src/data_cleaned/csv/`) → **格式转换** (`src/utils/csv_to_json.py`)
3. **JSON数据** (`src/data_cleaned/json/`) → **特殊分析** (`src/utils/extract_*.py`)
4. **分析结果** → **前端展示** (`src/rendering/public/`)

## 📝 技术要点

- **响应式设计** - 支持移动端和桌面端
- **组件化开发** - 可复用的ECharts组件
- **类型安全** - TypeScript确保代码质量
- **现代化构建** - Vite提供快速的开发体验
- **容器化部署** - Docker支持一键部署
- **数据驱动** - 基于真实电商数据分析



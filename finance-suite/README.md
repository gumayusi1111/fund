# 📈 个人指数分析平台

专为个人投资者打造的指数分析、基金对比和收益预测平台。基于现代化的前后端分离架构，提供专业的金融数据分析工具。

## ✨ 主要功能

### 🔍 指数分析
- **指数查询**: 支持沪深300、中证500、上证指数等主要指数
- **历史数据**: 获取任意时间范围的指数历史走势
- **实时行情**: 提供指数实时价格和涨跌幅
- **指数对比**: 多个指数同时对比分析

### 💰 基金分析  
- **基金搜索**: 快速查找和筛选基金产品
- **净值查询**: 获取基金历史净值和收益率
- **业绩分析**: 深入分析基金表现和风险指标
- **基金对比**: 多只基金横向对比

### 🔮 收益预测
- **投资预测**: 基于历史数据预测投资收益
- **定投分析**: 定期定额投资策略回测
- **风险评估**: 全面的风险指标分析
- **策略回测**: 不同投资策略的历史表现

## 🚀 快速开始

### 环境要求
- **Python**: 3.8+
- **Node.js**: 18+
- **操作系统**: macOS / Linux / Windows

### 一键启动

```bash
# 进入项目目录
cd finance-suite

# 一键启动前后端服务
./start.sh
```

启动脚本会自动：
1. ✅ 检查环境依赖
2. 🔧 创建Python虚拟环境  
3. 📦 安装后端依赖
4. 🖥️  启动FastAPI服务 (端口8000)
5. 📦 安装前端依赖
6. 🌐 启动Next.js服务 (端口3000)

### 访问地址
- **前端应用**: http://localhost:3000
- **后端API**: http://localhost:8000  
- **API文档**: http://localhost:8000/docs

## 🏗️ 技术架构

### 后端技术栈
```
FastAPI 0.104.1     # 现代Python Web框架
AKShare 1.11.52     # 金融数据源
Pandas 2.1.3        # 数据分析
NumPy 1.24.3        # 数值计算
Pydantic 2.5.0      # 数据验证
```

### 前端技术栈
```
Next.js 14          # React全栈框架
TypeScript          # 类型安全
Tailwind CSS        # 样式框架
ECharts             # 数据可视化
SWR                 # 数据获取
```

### 项目结构
```
finance-suite/
├── backend/                # 后端服务
│   ├── app/
│   │   ├── api/v1/        # API接口层
│   │   ├── services/      # 业务逻辑层  
│   │   ├── schemas/       # 数据模型层
│   │   ├── adapters/      # 数据适配层
│   │   └── core/          # 核心配置
│   └── requirements.txt   # Python依赖
├── frontend/              # 前端应用
│   ├── src/app/          # Next.js页面
│   ├── src/components/   # 可复用组件
│   └── package.json      # Node依赖
├── start.sh              # 一键启动脚本
└── README.md            # 项目文档
```

## 📊 API接口

### 指数管理
```http
GET /api/v1/indices/list              # 获取指数列表
GET /api/v1/indices/{code}            # 获取指数信息
GET /api/v1/indices/{code}/history    # 获取历史数据
POST /api/v1/indices/compare          # 指数对比
```

### 基金管理
```http
GET /api/v1/funds/list                # 获取基金列表
GET /api/v1/funds/{code}              # 获取基金信息
GET /api/v1/funds/{code}/history      # 获取历史净值
POST /api/v1/funds/compare            # 基金对比
```

### 收益预测
```http
POST /api/v1/predictions/fund-return  # 收益预测
POST /api/v1/predictions/dca-analysis # 定投分析
GET /api/v1/predictions/backtest/{code} # 策略回测
GET /api/v1/predictions/risk-analysis/{code} # 风险分析
```

## 🛠️ 手动部署

### 后端部署
```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端部署
```bash
cd frontend

# 安装依赖
npm install

# 开发模式
npm run dev

# 生产构建
npm run build
npm start
```

## 📝 使用示例

### 1. 指数分析
```python
# 获取沪深300指数信息
GET /api/v1/indices/000300

# 获取近一年历史数据
GET /api/v1/indices/000300/history?period=1y

# 对比多个指数
POST /api/v1/indices/compare
{
    "index_codes": ["000300", "000905", "399006"],
    "period": "1y"
}
```

### 2. 基金分析
```python
# 查询基金列表
GET /api/v1/funds/list?page=1&size=20

# 获取基金详情
GET /api/v1/funds/110020

# 基金历史净值
GET /api/v1/funds/110020/history?period=1y
```

### 3. 收益预测
```python
# 投资收益预测
POST /api/v1/predictions/fund-return
{
    "fund_code": "110020",
    "investment_amount": 10000,
    "investment_period": 12,
    "investment_type": "lump_sum"
}

# 定投策略分析
POST /api/v1/predictions/dca-analysis  
{
    "fund_code": "110020",
    "monthly_amount": 1000,
    "investment_months": 12
}
```

## 🎯 设计特色

### 🔒 高内聚低耦合
- **模块化设计**: 每个功能模块独立，职责单一
- **分层架构**: API层、服务层、数据层清晰分离
- **依赖注入**: 便于测试和维护

### 📈 专业金融分析
- **多维度指标**: 收益率、波动率、夏普比率、最大回撤
- **风险评估**: VaR、CVaR等专业风险指标
- **策略回测**: 历史数据验证投资策略

### 🎨 现代化界面
- **响应式设计**: 支持桌面和移动设备
- **直观图表**: ECharts专业金融图表
- **用户友好**: 简洁清晰的操作界面

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## ⚠️ 免责声明

本平台仅供学习和研究使用，所有数据和分析结果不构成投资建议。投资有风险，入市需谨慎。

## 📞 联系方式

- **项目地址**: https://github.com/your-username/finance-suite
- **问题反馈**: https://github.com/your-username/finance-suite/issues
- **邮箱**: your-email@example.com

---

> 💡 **提示**: 使用 `./start.sh` 一键启动，开始您的金融数据分析之旅！ 
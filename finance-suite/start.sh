#!/bin/bash

# 个人指数分析平台一键启动脚本
echo "🚀 启动个人指数分析平台..."

# 检查Node.js和Python
command -v node >/dev/null 2>&1 || { echo "❌ 请先安装 Node.js"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ 请先安装 Python 3"; exit 1; }

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 启动后端
echo "📡 启动后端服务..."
cd "$SCRIPT_DIR/backend"

# 检查并创建虚拟环境
if [ ! -d "venv" ]; then
    echo "🔧 创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔄 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📦 检查并安装依赖..."
pip install -r requirements.txt

# 启动后端服务（后台运行）
echo "🖥️  启动FastAPI服务器..."
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 等待后端启动
sleep 5

# 启动前端
echo "🌐 启动前端服务..."
cd "$SCRIPT_DIR/frontend"

# 安装前端依赖
echo "📦 安装前端依赖..."
npm install

# 启动前端服务（后台运行）
echo "⚡ 启动Next.js开发服务器..."
npm run dev &
FRONTEND_PID=$!

# 等待服务启动
sleep 3

echo ""
echo "✅ 服务启动完成！"
echo "📊 后端API地址: http://localhost:8000"
echo "📊 API文档地址: http://localhost:8000/docs"
echo "🌐 前端地址: http://localhost:3000"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap "echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait 
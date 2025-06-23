from fastapi import APIRouter
from .endpoints import indices, funds, predictions

# 创建API v1主路由
api_router = APIRouter()

# 注册各个功能模块的路由
api_router.include_router(
    indices.router,
    prefix="/indices",
    tags=["指数管理"]
)

api_router.include_router(
    funds.router,
    prefix="/funds", 
    tags=["基金管理"]
)

api_router.include_router(
    predictions.router,
    prefix="/predictions",
    tags=["收益预测"]
) 
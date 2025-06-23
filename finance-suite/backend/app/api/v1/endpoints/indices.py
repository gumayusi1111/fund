from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from datetime import datetime, timedelta
from app.services.index_service import IndexService
from app.schemas.index_schemas import (
    IndexInfo,
    IndexHistoryData,
    IndexComparisonResponse,
    IndexListResponse
)

# 创建指数路由
router = APIRouter()

# 依赖注入：获取指数服务实例
def get_index_service() -> IndexService:
    return IndexService()

@router.get("/list", response_model=IndexListResponse)
async def get_index_list(
    size: int = Query(50, description="返回数量"),
    service: IndexService = Depends(get_index_service)
):
    """获取支持的指数列表"""
    try:
        indices = await service.get_available_indices()
        # 限制返回数量
        total = len(indices)
        if size > 0:
            indices = indices[:size]
        
        return IndexListResponse(
            success=True,
            data=indices,
            total=total,
            page=1,
            size=len(indices),
            message="获取指数列表成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取指数列表失败: {str(e)}")

@router.get("/search")
async def search_indices(
    keyword: str = Query(..., description="搜索关键词"),
    size: int = Query(10, description="返回数量"),
    service: IndexService = Depends(get_index_service)
):
    """搜索指数"""
    try:
        indices = await service.search_indices(keyword, size)
        return {
            "success": True,
            "data": indices,
            "message": "搜索指数成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索指数失败: {str(e)}")

@router.get("/{index_code}", response_model=IndexInfo)
async def get_index_info(
    index_code: str,
    service: IndexService = Depends(get_index_service)
):
    """获取指定指数的基本信息"""
    try:
        index_info = await service.get_index_info(index_code)
        if not index_info:
            raise HTTPException(status_code=404, detail="指数不存在")
        return index_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取指数信息失败: {str(e)}")

@router.get("/{index_code}/info", response_model=IndexInfo)
async def get_index_info_detailed(
    index_code: str,
    service: IndexService = Depends(get_index_service)
):
    """获取指定指数的详细信息（与get_index_info相同，为了兼容前端调用）"""
    try:
        index_info = await service.get_index_info(index_code)
        if not index_info:
            raise HTTPException(status_code=404, detail="指数不存在")
        return index_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取指数信息失败: {str(e)}")

@router.get("/{index_code}/history", response_model=IndexHistoryData)
async def get_index_history(
    index_code: str,
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    period: str = Query("1y", description="时间周期: 1m, 3m, 6m, 1y, 2y, 5y"),
    service: IndexService = Depends(get_index_service)
):
    """获取指数历史数据"""
    try:
        # 如果没有指定日期，根据period计算
        if not start_date or not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
            period_days = {
                "1m": 30, "3m": 90, "6m": 180, 
                "1y": 365, "2y": 730, "5y": 1825
            }
            days = period_days.get(period, 365)
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        history_data = await service.get_index_history(index_code, start_date, end_date)
        return history_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史数据失败: {str(e)}")

@router.post("/compare", response_model=IndexComparisonResponse)
async def compare_indices(
    index_codes: List[str],
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    period: str = Query("1y", description="时间周期"),
    service: IndexService = Depends(get_index_service)
):
    """对比多个指数的表现"""
    try:
        if len(index_codes) < 2:
            raise HTTPException(status_code=400, detail="至少需要选择2个指数进行对比")
        
        if len(index_codes) > 5:
            raise HTTPException(status_code=400, detail="最多只能对比5个指数")
        
        # 计算日期范围
        if not start_date or not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
            period_days = {
                "1m": 30, "3m": 90, "6m": 180, 
                "1y": 365, "2y": 730, "5y": 1825
            }
            days = period_days.get(period, 365)
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        comparison_data = await service.compare_indices(index_codes, start_date, end_date)
        return comparison_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"指数对比失败: {str(e)}")

@router.get("/{index_code}/realtime")
async def get_index_realtime(
    index_code: str,
    service: IndexService = Depends(get_index_service)
):
    """获取指数实时行情"""
    try:
        realtime_data = await service.get_realtime_data(index_code)
        return {
            "success": True,
            "data": realtime_data,
            "message": "获取实时数据成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取实时数据失败: {str(e)}") 
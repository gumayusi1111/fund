from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from datetime import datetime, timedelta
from app.services.fund_service import FundService
from app.schemas.fund_schemas import (
    FundInfo,
    FundListResponse,
    FundHistoryData,
    FundComparisonResponse
)

# 创建基金路由
router = APIRouter()

# 依赖注入：获取基金服务实例
def get_fund_service() -> FundService:
    return FundService()

@router.get("/list", response_model=FundListResponse)
async def get_fund_list(
    fund_type: Optional[str] = Query(None, description="基金类型"),
    page: int = Query(1, description="页码", ge=1),
    size: int = Query(20, description="每页数量", ge=1, le=100),
    service: FundService = Depends(get_fund_service)
):
    """获取基金列表"""
    try:
        funds = await service.get_fund_list(fund_type, page, size)
        return funds
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取基金列表失败: {str(e)}")

@router.get("/{fund_code}", response_model=FundInfo)
async def get_fund_info(
    fund_code: str,
    service: FundService = Depends(get_fund_service)
):
    """获取基金详细信息"""
    try:
        fund_info = await service.get_fund_info(fund_code)
        if not fund_info:
            raise HTTPException(status_code=404, detail="基金不存在")
        return fund_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取基金信息失败: {str(e)}")

@router.get("/{fund_code}/history", response_model=FundHistoryData)
async def get_fund_history(
    fund_code: str,
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    period: str = Query("1y", description="时间周期: 1m, 3m, 6m, 1y, 2y, 5y"),
    service: FundService = Depends(get_fund_service)
):
    """获取基金历史净值数据"""
    try:
        # 计算日期范围
        if not start_date or not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
            period_days = {
                "1m": 30, "3m": 90, "6m": 180, 
                "1y": 365, "2y": 730, "5y": 1825
            }
            days = period_days.get(period, 365)
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        history_data = await service.get_fund_history(fund_code, start_date, end_date)
        return history_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取基金历史数据失败: {str(e)}")

@router.post("/compare", response_model=FundComparisonResponse)
async def compare_funds(
    fund_codes: List[str],
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    period: str = Query("1y", description="时间周期"),
    service: FundService = Depends(get_fund_service)
):
    """对比多个基金的表现"""
    try:
        if len(fund_codes) < 2:
            raise HTTPException(status_code=400, detail="至少需要选择2个基金进行对比")
        
        if len(fund_codes) > 5:
            raise HTTPException(status_code=400, detail="最多只能对比5个基金")
        
        # 计算日期范围
        if not start_date or not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
            period_days = {
                "1m": 30, "3m": 90, "6m": 180, 
                "1y": 365, "2y": 730, "5y": 1825
            }
            days = period_days.get(period, 365)
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        comparison_data = await service.compare_funds(fund_codes, start_date, end_date)
        return comparison_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"基金对比失败: {str(e)}") 
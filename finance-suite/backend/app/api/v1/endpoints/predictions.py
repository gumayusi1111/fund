from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from app.services.prediction_service import PredictionService
from app.schemas.prediction_schemas import (
    InvestmentPrediction,
    DCAAnalysis,
    PredictionRequest,
    DCARequest
)

# 创建预测路由
router = APIRouter()

# 依赖注入：获取预测服务实例
def get_prediction_service() -> PredictionService:
    return PredictionService()

@router.post("/fund-return", response_model=InvestmentPrediction)
async def predict_fund_return(
    request: PredictionRequest,
    service: PredictionService = Depends(get_prediction_service)
):
    """预测基金投资收益"""
    try:
        prediction = await service.predict_fund_return(
            fund_code=request.fund_code,
            investment_amount=request.investment_amount,
            investment_period=request.investment_period,
            investment_type=request.investment_type
        )
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"收益预测失败: {str(e)}")

@router.post("/dca-analysis", response_model=DCAAnalysis)
async def analyze_dca_strategy(
    request: DCARequest,
    service: PredictionService = Depends(get_prediction_service)
):
    """定投策略分析"""
    try:
        analysis = await service.analyze_dca_strategy(
            fund_code=request.fund_code,
            monthly_amount=request.monthly_amount,
            investment_months=request.investment_months,
            start_date=request.start_date
        )
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"定投分析失败: {str(e)}")

@router.get("/backtest/{fund_code}")
async def backtest_investment(
    fund_code: str,
    investment_amount: float = Query(..., description="投资金额"),
    start_date: str = Query(..., description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    strategy: str = Query("lump_sum", description="投资策略: lump_sum, dca"),
    service: PredictionService = Depends(get_prediction_service)
):
    """投资策略回测"""
    try:
        backtest_result = await service.backtest_investment(
            fund_code=fund_code,
            investment_amount=investment_amount,
            start_date=start_date,
            end_date=end_date,
            strategy=strategy
        )
        return {
            "success": True,
            "data": backtest_result,
            "message": "回测分析完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"回测分析失败: {str(e)}")

@router.get("/risk-analysis/{fund_code}")
async def analyze_risk(
    fund_code: str,
    period: str = Query("1y", description="分析周期: 1y, 2y, 3y, 5y"),
    service: PredictionService = Depends(get_prediction_service)
):
    """风险分析"""
    try:
        risk_analysis = await service.analyze_risk(fund_code, period)
        return {
            "success": True,
            "data": risk_analysis,
            "message": "风险分析完成"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"风险分析失败: {str(e)}") 
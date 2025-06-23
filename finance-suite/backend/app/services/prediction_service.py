import logging
from typing import List, Optional
from datetime import datetime
import random

from app.services.fund_service import FundService
from app.schemas.prediction_schemas import (
    InvestmentPrediction, DCAAnalysis, PredictionScenario, DCADataPoint,
    BacktestResult, RiskAnalysis, InvestmentType
)

logger = logging.getLogger(__name__)


class PredictionService:
    """收益预测服务类"""
    
    def __init__(self):
        self.fund_service = FundService()
    
    async def predict_fund_return(self, fund_code: str, investment_amount: float,
                                investment_period: int, investment_type: InvestmentType) -> InvestmentPrediction:
        """预测基金投资收益"""
        try:
            fund_info = await self.fund_service.get_fund_info(fund_code)
            if not fund_info:
                raise ValueError(f"基金 {fund_code} 不存在")
            
            # 生成预测场景
            scenarios = [
                PredictionScenario(
                    scenario_name="乐观场景",
                    probability=0.2,
                    expected_return=15.0,
                    final_value=investment_amount * 1.15,
                    total_return=investment_amount * 0.15,
                    annualized_return=15.0
                ),
                PredictionScenario(
                    scenario_name="基准场景",
                    probability=0.6,
                    expected_return=8.0,
                    final_value=investment_amount * 1.08,
                    total_return=investment_amount * 0.08,
                    annualized_return=8.0
                ),
                PredictionScenario(
                    scenario_name="悲观场景",
                    probability=0.2,
                    expected_return=-5.0,
                    final_value=investment_amount * 0.95,
                    total_return=investment_amount * -0.05,
                    annualized_return=-5.0
                ),
            ]
            
            expected_final_value = sum(s.final_value * s.probability for s in scenarios)
            expected_total_return = expected_final_value - investment_amount
            expected_annualized_return = 8.0  # 简化计算
            
            return InvestmentPrediction(
                fund_code=fund_code,
                fund_name=fund_info.name,
                investment_amount=investment_amount,
                investment_period=investment_period,
                investment_type=investment_type,
                scenarios=scenarios,
                expected_final_value=expected_final_value,
                expected_total_return=expected_total_return,
                expected_annualized_return=expected_annualized_return,
                volatility=18.5,
                max_drawdown=12.3,
                var_95=-2.1,
                historical_performance={
                    "total_return": 12.5,
                    "volatility": 18.5,
                    "sharpe_ratio": 0.85,
                    "max_drawdown": 12.3
                },
                model_accuracy=0.75,
                prediction_date=datetime.now()
            )
        except Exception as e:
            logger.error(f"收益预测失败: {str(e)}")
            raise
    
    async def analyze_dca_strategy(self, fund_code: str, monthly_amount: float,
                                 investment_months: int, start_date: Optional[str] = None) -> DCAAnalysis:
        """定投策略分析"""
        try:
            fund_info = await self.fund_service.get_fund_info(fund_code)
            if not fund_info:
                raise ValueError(f"基金 {fund_code} 不存在")
            
            # 生成模拟定投数据
            data_points = []
            cumulative_investment = 0
            cumulative_shares = 0
            
            for month in range(investment_months):
                fund_price = 1.0 + random.uniform(-0.1, 0.1)  # 模拟价格波动
                shares_purchased = monthly_amount / fund_price
                
                cumulative_investment += monthly_amount
                cumulative_shares += shares_purchased
                market_value = cumulative_shares * fund_price
                total_return = market_value - cumulative_investment
                return_rate = (total_return / cumulative_investment * 100) if cumulative_investment > 0 else 0
                
                data_points.append(DCADataPoint(
                    date=f"2024-{month+1:02d}-01",
                    investment_amount=monthly_amount,
                    fund_price=fund_price,
                    shares_purchased=shares_purchased,
                    cumulative_investment=cumulative_investment,
                    cumulative_shares=cumulative_shares,
                    market_value=market_value,
                    total_return=total_return,
                    return_rate=return_rate
                ))
            
            total_investment = monthly_amount * investment_months
            final_value = data_points[-1].market_value if data_points else 0
            total_return = final_value - total_investment
            annualized_return = 8.5  # 简化计算
            
            return DCAAnalysis(
                fund_code=fund_code,
                fund_name=fund_info.name,
                monthly_amount=monthly_amount,
                investment_months=investment_months,
                start_date=start_date or "2024-01-01",
                data_points=data_points,
                total_investment=total_investment,
                final_value=final_value,
                total_return=total_return,
                annualized_return=annualized_return,
                volatility=15.2,
                max_drawdown=8.7,
                sharpe_ratio=0.95,
                lump_sum_comparison={
                    "lump_sum_final_value": total_investment * 1.06,
                    "dca_advantage": final_value - total_investment * 1.06,
                    "dca_advantage_pct": 2.3
                },
                analysis_date=datetime.now()
            )
        except Exception as e:
            logger.error(f"定投分析失败: {str(e)}")
            raise
    
    async def backtest_investment(self, fund_code: str, investment_amount: float,
                                start_date: str, end_date: Optional[str] = None,
                                strategy: str = "lump_sum") -> BacktestResult:
        """投资策略回测"""
        try:
            fund_info = await self.fund_service.get_fund_info(fund_code)
            if not fund_info:
                raise ValueError(f"基金 {fund_code} 不存在")
            
            # 模拟回测结果
            final_value = investment_amount * random.uniform(1.05, 1.25)
            total_return = final_value - investment_amount
            annualized_return = random.uniform(5, 15)
            
            return BacktestResult(
                fund_code=fund_code,
                fund_name=fund_info.name,
                start_date=start_date,
                end_date=end_date or datetime.now().strftime("%Y-%m-%d"),
                strategy=strategy,
                initial_investment=investment_amount,
                final_value=final_value,
                total_return=total_return,
                annualized_return=annualized_return,
                volatility=random.uniform(15, 25),
                max_drawdown=random.uniform(8, 15),
                sharpe_ratio=random.uniform(0.6, 1.2),
                calmar_ratio=random.uniform(0.8, 1.5),
                performance_data=[{"date": "2024-01-01", "value": investment_amount}]
            )
        except Exception as e:
            logger.error(f"回测分析失败: {str(e)}")
            raise
    
    async def analyze_risk(self, fund_code: str, period: str = "1y") -> RiskAnalysis:
        """风险分析"""
        try:
            fund_info = await self.fund_service.get_fund_info(fund_code)
            if not fund_info:
                raise ValueError(f"基金 {fund_code} 不存在")
            
            volatility = random.uniform(15, 25)
            max_drawdown = random.uniform(8, 15)
            
            # 简单的风险评估
            risk_score = (volatility * 0.6 + max_drawdown * 0.4) / 2
            
            if risk_score < 10:
                risk_level = "低风险"
            elif risk_score < 20:
                risk_level = "中低风险"
            elif risk_score < 30:
                risk_level = "中等风险"
            else:
                risk_level = "高风险"
            
            return RiskAnalysis(
                fund_code=fund_code,
                fund_name=fund_info.name,
                analysis_period=period,
                volatility=volatility,
                max_drawdown=max_drawdown,
                var_95=random.uniform(-3, -1),
                var_99=random.uniform(-5, -3),
                cvar_95=random.uniform(-4, -2),
                downside_deviation=random.uniform(10, 18),
                risk_level=risk_level,
                risk_score=risk_score,
                analysis_date=datetime.now()
            )
        except Exception as e:
            logger.error(f"风险分析失败: {str(e)}")
            raise 
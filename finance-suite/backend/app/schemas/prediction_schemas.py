from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class InvestmentType(str, Enum):
    """投资类型枚举"""
    LUMP_SUM = "lump_sum"    # 一次性投资
    DCA = "dca"              # 定期定额投资


class PredictionRequest(BaseModel):
    """收益预测请求"""
    fund_code: str = Field(..., description="基金代码")
    investment_amount: float = Field(..., description="投资金额", gt=0)
    investment_period: int = Field(..., description="投资期限(月)", gt=0)
    investment_type: InvestmentType = Field(InvestmentType.LUMP_SUM, description="投资类型")


class DCARequest(BaseModel):
    """定投分析请求"""
    fund_code: str = Field(..., description="基金代码")
    monthly_amount: float = Field(..., description="每月投资金额", gt=0)
    investment_months: int = Field(..., description="投资月数", gt=0)
    start_date: Optional[str] = Field(None, description="开始日期 YYYY-MM-DD")


class PredictionScenario(BaseModel):
    """预测场景"""
    scenario_name: str = Field(..., description="场景名称")
    probability: float = Field(..., description="概率", ge=0, le=1)
    expected_return: float = Field(..., description="预期收益率")
    final_value: float = Field(..., description="最终价值")
    total_return: float = Field(..., description="总收益")
    annualized_return: float = Field(..., description="年化收益率")


class InvestmentPrediction(BaseModel):
    """投资收益预测"""
    fund_code: str = Field(..., description="基金代码")
    fund_name: str = Field(..., description="基金名称")
    investment_amount: float = Field(..., description="投资金额")
    investment_period: int = Field(..., description="投资期限(月)")
    investment_type: InvestmentType = Field(..., description="投资类型")
    
    # 预测结果
    scenarios: List[PredictionScenario] = Field(..., description="预测场景")
    expected_final_value: float = Field(..., description="预期最终价值")
    expected_total_return: float = Field(..., description="预期总收益")
    expected_annualized_return: float = Field(..., description="预期年化收益率")
    
    # 风险指标
    volatility: float = Field(..., description="波动率")
    max_drawdown: float = Field(..., description="最大回撤")
    var_95: float = Field(..., description="95% VaR")
    
    # 其他信息
    historical_performance: Dict[str, float] = Field(..., description="历史表现")
    model_accuracy: float = Field(..., description="模型准确度")
    prediction_date: datetime = Field(..., description="预测日期")


class DCADataPoint(BaseModel):
    """定投数据点"""
    date: str = Field(..., description="投资日期")
    investment_amount: float = Field(..., description="投资金额")
    fund_price: float = Field(..., description="基金价格")
    shares_purchased: float = Field(..., description="购买份额")
    cumulative_investment: float = Field(..., description="累计投资")
    cumulative_shares: float = Field(..., description="累计份额")
    market_value: float = Field(..., description="市值")
    total_return: float = Field(..., description="总收益")
    return_rate: float = Field(..., description="收益率")


class DCAAnalysis(BaseModel):
    """定投策略分析"""
    fund_code: str = Field(..., description="基金代码")
    fund_name: str = Field(..., description="基金名称")
    monthly_amount: float = Field(..., description="每月投资金额")
    investment_months: int = Field(..., description="投资月数")
    start_date: str = Field(..., description="开始日期")
    
    # 分析结果
    data_points: List[DCADataPoint] = Field(..., description="定投数据点")
    total_investment: float = Field(..., description="总投资金额")
    final_value: float = Field(..., description="最终价值")
    total_return: float = Field(..., description="总收益")
    annualized_return: float = Field(..., description="年化收益率")
    
    # 风险指标
    volatility: float = Field(..., description="投资期间波动率")
    max_drawdown: float = Field(..., description="最大回撤")
    sharpe_ratio: float = Field(..., description="夏普比率")
    
    # 对比分析
    lump_sum_comparison: Dict[str, float] = Field(..., description="与一次性投资对比")
    analysis_date: datetime = Field(..., description="分析日期")


class BacktestResult(BaseModel):
    """回测结果"""
    fund_code: str = Field(..., description="基金代码")
    fund_name: str = Field(..., description="基金名称")
    start_date: str = Field(..., description="开始日期")
    end_date: str = Field(..., description="结束日期")
    strategy: str = Field(..., description="投资策略")
    
    # 回测结果
    initial_investment: float = Field(..., description="初始投资")
    final_value: float = Field(..., description="最终价值")
    total_return: float = Field(..., description="总收益")
    annualized_return: float = Field(..., description="年化收益率")
    
    # 风险指标
    volatility: float = Field(..., description="波动率")
    max_drawdown: float = Field(..., description="最大回撤")
    sharpe_ratio: float = Field(..., description="夏普比率")
    calmar_ratio: float = Field(..., description="卡玛比率")
    
    # 详细数据
    performance_data: List[Dict[str, Any]] = Field(..., description="业绩数据")


class RiskAnalysis(BaseModel):
    """风险分析"""
    fund_code: str = Field(..., description="基金代码")
    fund_name: str = Field(..., description="基金名称")
    analysis_period: str = Field(..., description="分析周期")
    
    # 风险指标
    volatility: float = Field(..., description="波动率")
    max_drawdown: float = Field(..., description="最大回撤")
    var_95: float = Field(..., description="95% VaR")
    var_99: float = Field(..., description="99% VaR")
    cvar_95: float = Field(..., description="95% CVaR")
    
    # 其他风险指标
    downside_deviation: float = Field(..., description="下行偏差")
    
    # 风险等级
    risk_level: str = Field(..., description="风险等级")
    risk_score: float = Field(..., description="风险评分")
    
    analysis_date: datetime = Field(..., description="分析日期") 
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class FundType(str, Enum):
    """基金类型枚举"""
    STOCK = "stock"          # 股票型
    BOND = "bond"            # 债券型
    HYBRID = "hybrid"        # 混合型
    INDEX = "index"          # 指数型
    MONEY = "money"          # 货币型
    QDII = "qdii"           # QDII


class FundBaseInfo(BaseModel):
    """基金基础信息"""
    code: str = Field(..., description="基金代码")
    name: str = Field(..., description="基金名称")
    fund_type: FundType = Field(..., description="基金类型")
    company: str = Field(..., description="基金公司")


class FundInfo(BaseModel):
    """基金详细信息"""
    code: str = Field(..., description="基金代码")
    name: str = Field(..., description="基金名称")
    fund_type: FundType = Field(..., description="基金类型")
    company: str = Field(..., description="基金公司")
    manager: Optional[str] = Field(None, description="基金经理")
    establish_date: Optional[str] = Field(None, description="成立日期")
    total_asset: Optional[float] = Field(None, description="基金规模")
    unit_net_value: Optional[float] = Field(None, description="单位净值")
    accumulated_net_value: Optional[float] = Field(None, description="累计净值")
    net_value_date: Optional[str] = Field(None, description="净值日期")
    day_growth_rate: Optional[float] = Field(None, description="日涨跌幅")
    recent_1week: Optional[float] = Field(None, description="近1周收益率")
    recent_1month: Optional[float] = Field(None, description="近1月收益率")
    recent_3month: Optional[float] = Field(None, description="近3月收益率")
    recent_6month: Optional[float] = Field(None, description="近6月收益率")
    recent_1year: Optional[float] = Field(None, description="近1年收益率")
    recent_2year: Optional[float] = Field(None, description="近2年收益率")
    recent_3year: Optional[float] = Field(None, description="近3年收益率")
    index_code: Optional[str] = Field(None, description="跟踪指数代码")
    index_name: Optional[str] = Field(None, description="跟踪指数名称")
    management_fee: Optional[float] = Field(None, description="管理费率")
    custodian_fee: Optional[float] = Field(None, description="托管费率")
    subscription_fee: Optional[float] = Field(None, description="申购费率")
    redemption_fee: Optional[float] = Field(None, description="赎回费率")


class FundDataPoint(BaseModel):
    """基金净值数据点"""
    date: str = Field(..., description="日期")
    unit_net_value: float = Field(..., description="单位净值")
    accumulated_net_value: float = Field(..., description="累计净值")
    daily_growth_rate: Optional[float] = Field(None, description="日增长率")


class FundHistoryData(BaseModel):
    """基金历史数据"""
    code: str = Field(..., description="基金代码")
    name: str = Field(..., description="基金名称")
    data: List[FundDataPoint] = Field(..., description="历史净值数据")
    statistics: Optional[Dict[str, Any]] = Field(None, description="统计信息")


class FundComparisonItem(BaseModel):
    """基金对比项"""
    code: str = Field(..., description="基金代码")
    name: str = Field(..., description="基金名称")
    fund_type: FundType = Field(..., description="基金类型")
    data: List[FundDataPoint] = Field(..., description="历史数据")
    performance: Dict[str, float] = Field(..., description="表现指标")
    risk_metrics: Dict[str, float] = Field(..., description="风险指标")


class FundComparisonResponse(BaseModel):
    """基金对比响应"""
    success: bool = Field(True, description="请求是否成功")
    data: List[FundComparisonItem] = Field(..., description="对比数据")
    comparison_metrics: Dict[str, Any] = Field(..., description="对比指标")
    message: str = Field(..., description="响应消息")


class FundListResponse(BaseModel):
    """基金列表响应"""
    success: bool = Field(True, description="请求是否成功")
    data: List[FundBaseInfo] = Field(..., description="基金列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    size: int = Field(..., description="每页数量")
    message: str = Field(..., description="响应消息")


class IndexFundsResponse(BaseModel):
    """指数基金响应"""
    success: bool = Field(True, description="请求是否成功")
    data: List[FundInfo] = Field(..., description="指数基金列表")
    index_code: str = Field(..., description="指数代码")
    index_name: str = Field(..., description="指数名称")
    message: str = Field(..., description="响应消息")


class FundRealtimeData(BaseModel):
    """基金实时数据"""
    code: str = Field(..., description="基金代码")
    name: str = Field(..., description="基金名称")
    unit_net_value: float = Field(..., description="单位净值")
    accumulated_net_value: float = Field(..., description="累计净值")
    net_value_date: str = Field(..., description="净值日期")
    day_growth_rate: float = Field(..., description="日涨跌幅")
    last_update: datetime = Field(..., description="最后更新时间")


class FundPerformanceAnalysis(BaseModel):
    """基金业绩分析"""
    code: str = Field(..., description="基金代码")
    name: str = Field(..., description="基金名称")
    return_metrics: Dict[str, float] = Field(..., description="收益指标")
    risk_metrics: Dict[str, float] = Field(..., description="风险指标")
    risk_adjusted_metrics: Dict[str, float] = Field(..., description="风险调整后指标")
    benchmark_comparison: Optional[Dict[str, Any]] = Field(None, description="基准对比")
    rating: Optional[str] = Field(None, description="评级")
    last_update: datetime = Field(..., description="最后更新时间") 
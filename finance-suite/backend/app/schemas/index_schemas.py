from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum


class IndexType(str, Enum):
    """指数类型枚举"""
    EQUITY = "equity"  # 股票指数
    BOND = "bond"      # 债券指数
    COMMODITY = "commodity"  # 商品指数
    CURRENCY = "currency"    # 货币指数
    SECTOR = "sector"        # 行业指数
    GROWTH = "growth"        # 成长指数
    VALUE = "value"          # 价值指数
    SMALL_CAP = "small_cap"  # 小盘指数
    LARGE_CAP = "large_cap"  # 大盘指数


class IndexBaseInfo(BaseModel):
    """指数基础信息"""
    code: str = Field(..., description="指数代码")
    name: str = Field(..., description="指数名称")
    market: str = Field(..., description="市场类型")
    category: str = Field(..., description="指数分类")
    index_type: Optional[IndexType] = Field(None, description="指数类型")


class IndexInfo(BaseModel):
    """指数详细信息"""
    code: str = Field(..., description="指数代码")
    name: str = Field(..., description="指数名称")
    market: str = Field(..., description="市场类型")
    category: str = Field(..., description="指数分类")
    index_type: Optional[IndexType] = Field(None, description="指数类型")
    base_date: Optional[str] = Field(None, description="基准日期")
    base_value: Optional[float] = Field(None, description="基准点数")
    current_value: Optional[float] = Field(None, description="当前点数")
    change_percent: Optional[float] = Field(None, description="涨跌幅")
    change_value: Optional[float] = Field(None, description="涨跌点数")
    volume: Optional[float] = Field(None, description="成交量")
    turnover: Optional[float] = Field(None, description="成交额")
    pe_ratio: Optional[float] = Field(None, description="市盈率")
    pb_ratio: Optional[float] = Field(None, description="市净率")
    dividend_yield: Optional[float] = Field(None, description="股息率")
    constituent_count: Optional[int] = Field(None, description="成分股数量")
    last_update: Optional[datetime] = Field(None, description="最后更新时间")


class IndexDataPoint(BaseModel):
    """指数数据点"""
    date: str = Field(..., description="日期")
    open_value: float = Field(..., description="开盘点数")
    high_value: float = Field(..., description="最高点数")
    low_value: float = Field(..., description="最低点数")
    close_value: float = Field(..., description="收盘点数")
    volume: Optional[float] = Field(None, description="成交量")
    turnover: Optional[float] = Field(None, description="成交额")
    change_value: Optional[float] = Field(None, description="涨跌点数")
    change_percent: Optional[float] = Field(None, description="涨跌幅")


class IndexHistoryData(BaseModel):
    """指数历史数据"""
    code: str = Field(..., description="指数代码")
    name: str = Field(..., description="指数名称")
    data: List[IndexDataPoint] = Field(..., description="历史数据点")
    statistics: Optional[Dict[str, Any]] = Field(None, description="统计信息")


class IndexComparisonItem(BaseModel):
    """指数对比项"""
    code: str = Field(..., description="指数代码")
    name: str = Field(..., description="指数名称")
    index_type: Optional[IndexType] = Field(None, description="指数类型")
    data: List[IndexDataPoint] = Field(..., description="历史数据")
    performance: Dict[str, float] = Field(..., description="表现指标")
    statistics: Optional[Dict[str, Any]] = Field(None, description="统计信息")


class IndexComparisonResponse(BaseModel):
    """指数对比响应"""
    success: bool = Field(True, description="请求是否成功")
    data: List[IndexComparisonItem] = Field(..., description="对比数据")
    comparison_metrics: Dict[str, Any] = Field(..., description="对比指标")
    message: str = Field(..., description="响应消息")


class IndexListResponse(BaseModel):
    """指数列表响应"""
    success: bool = Field(True, description="请求是否成功")
    data: List[IndexBaseInfo] = Field(..., description="指数列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="页码")
    size: int = Field(..., description="每页大小")
    message: str = Field(..., description="响应消息")


class IndexRealtimeData(BaseModel):
    """指数实时数据"""
    code: str = Field(..., description="指数代码")
    name: str = Field(..., description="指数名称")
    current_value: float = Field(..., description="当前点数")
    change_percent: float = Field(..., description="涨跌幅")
    change_value: float = Field(..., description="涨跌点数")
    volume: Optional[float] = Field(None, description="成交量")
    turnover: Optional[float] = Field(None, description="成交额")
    high_value: Optional[float] = Field(None, description="今日最高")
    low_value: Optional[float] = Field(None, description="今日最低")
    open_value: Optional[float] = Field(None, description="今日开盘")
    last_update: datetime = Field(..., description="最后更新时间") 
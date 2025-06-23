"""
指数数据服务
"""
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import random

from app.adapters.akshare_adapter import AKShareAdapter
from app.schemas.index_schemas import (
    IndexInfo, IndexListResponse, IndexBaseInfo, IndexType,
    IndexHistoryData, IndexComparisonResponse, IndexComparisonItem
)

logger = logging.getLogger(__name__)


class IndexService:
    """指数数据服务类"""
    
    def __init__(self):
        self.adapter = AKShareAdapter()

    async def get_index_list(self, index_type: Optional[str] = None,
                           page: int = 1, size: int = 20) -> IndexListResponse:
        """获取指数列表"""
        try:
            # 定义一些常用指数
            indices = [
                IndexBaseInfo(
                    code="000001",
                    name="上证指数",
                    market="SH",
                    category="综合指数",
                    index_type=IndexType.EQUITY
                ),
                IndexBaseInfo(
                    code="000300",
                    name="沪深300",
                    market="SH",
                    category="规模指数",
                    index_type=IndexType.EQUITY
                ),
                IndexBaseInfo(
                    code="000905",
                    name="中证500",
                    market="SH",
                    category="规模指数",
                    index_type=IndexType.EQUITY
                ),
                IndexBaseInfo(
                    code="399001",
                    name="深证成指",
                    market="SZ",
                    category="综合指数",
                    index_type=IndexType.EQUITY
                ),
                IndexBaseInfo(
                    code="399006",
                    name="创业板指",
                    market="SZ",
                    category="规模指数",
                    index_type=IndexType.EQUITY
                ),
            ]
            
            # 分页处理
            start_idx = (page - 1) * size
            end_idx = start_idx + size
            page_indices = indices[start_idx:end_idx]
            
            return IndexListResponse(
                success=True,
                data=page_indices,
                total=len(indices),
                page=page,
                size=size,
                pages=(len(indices) + size - 1) // size
            )
        except Exception as e:
            logger.error(f"获取指数列表失败: {str(e)}")
            return IndexListResponse(
                success=False,
                data=[],
                total=0,
                page=page,
                size=size,
                pages=0,
                message=f"获取指数列表失败: {str(e)}"
            )

    async def get_available_indices(self) -> List[IndexBaseInfo]:
        """获取所有可用指数"""
        try:
            response = await self.get_index_list(size=100)
            return response.data
        except Exception as e:
            logger.error(f"获取可用指数失败: {str(e)}")
            return []

    def _determine_index_type(self, code: str, name: str) -> IndexType:
        """根据指数代码和名称确定指数类型"""
        if any(keyword in name for keyword in ["债券", "债"]):
            return IndexType.BOND
        elif any(keyword in name for keyword in ["商品", "黄金", "原油"]):
            return IndexType.COMMODITY
        else:
            return IndexType.EQUITY

    def _determine_category(self, name: str) -> str:
        """根据指数名称确定分类"""
        if any(keyword in name for keyword in ["300", "500", "50", "1000"]):
            return "规模指数"
        elif any(keyword in name for keyword in ["行业", "医药", "科技", "消费"]):
            return "行业指数"
        elif any(keyword in name for keyword in ["价值", "成长", "红利"]):
            return "策略指数"
        else:
            return "综合指数"

    async def get_index_info(self, index_code: str) -> Optional[IndexInfo]:
        """获取指数基本信息"""
        try:
            # 使用AKShare适配器获取真实数据
            info = await self.adapter.get_index_info(index_code)
            
            if info is None:
                logger.error(f"获取指数信息失败: {index_code} - 适配器返回None")
                return None
            
            logger.info(f"获取指数信息成功: {index_code} - {info}")
            
            # 将适配器返回的数据转换为IndexInfo对象
            return IndexInfo(
                code=info.get("code", index_code),
                name=info.get("name", f"指数 {index_code}"),
                market=info.get("market", "SH" if index_code.startswith("000") else "SZ"),
                category=self._determine_category(info.get("name", "")),
                index_type=self._determine_index_type(index_code, info.get("name", "")),
                current_value=info.get("current_value"),
                change_value=info.get("change_value"),
                change_percent=info.get("change_percent"),
                volume=info.get("volume"),
                turnover=info.get("turnover"),
                amplitude=info.get("amplitude"),
                pe_ratio=info.get("pe_ratio"),
                pb_ratio=info.get("pb_ratio"),
                dividend_yield=info.get("dividend_yield"),
                valuation_percentile=info.get("valuation_percentile"),
                last_update=datetime.now()
            )
        except Exception as e:
            logger.error(f"获取指数信息时出错: {e}")
            return None

    async def get_index_history(self, index_code: str, start_date: str,
                              end_date: str) -> IndexHistoryData:
        """获取指数历史数据"""
        try:
            # 使用AKShare适配器获取真实历史数据
            df = await self.adapter.get_index_history(index_code, start_date, end_date)
            
            if df is None or df.empty:
                # 如果没有数据，返回空的历史数据结构
                return IndexHistoryData(
                    code=index_code,
                    name=f"指数 {index_code}",
                    data=[],
                    start_date=start_date,
                    end_date=end_date,
                    total_days=0,
                    statistics={}
                )
            
            # 转换数据格式
            from app.schemas.index_schemas import IndexDataPoint
            data_points = []
            
            for _, row in df.iterrows():
                data_points.append(IndexDataPoint(
                    date=row["date"],
                    open_value=float(row["open"]),
                    close_value=float(row["close"]),
                    high_value=float(row["high"]),
                    low_value=float(row["low"]),
                    volume=int(row.get("volume", 0)),
                    change_value=0.0,  # 计算后填入
                    change_percent=0.0  # 计算后填入
                ))
            
            # 计算涨跌和涨跌幅
            for i in range(1, len(data_points)):
                prev_close = data_points[i-1].close_value
                curr_close = data_points[i].close_value
                change = curr_close - prev_close
                pct_change = (change / prev_close * 100) if prev_close > 0 else 0
                
                data_points[i].change_value = round(change, 2)
                data_points[i].change_percent = round(pct_change, 2)
            
            # 计算统计数据
            if data_points:
                start_value = data_points[0].close_value
                end_value = data_points[-1].close_value
                total_return = ((end_value - start_value) / start_value * 100) if start_value > 0 else 0
                
                # 计算波动率
                returns = [dp.change_percent for dp in data_points[1:]]
                if returns:
                    import statistics
                    volatility = statistics.stdev(returns) if len(returns) > 1 else 0
                else:
                    volatility = 0
                
                statistics_data = {
                    "total_return": round(total_return, 2),
                    "volatility": round(volatility, 2),
                    "max_value": max(dp.close_value for dp in data_points),
                    "min_value": min(dp.close_value for dp in data_points),
                    "avg_volume": sum(dp.volume for dp in data_points) / len(data_points)
                }
            else:
                statistics_data = {}
            
            return IndexHistoryData(
                code=index_code,
                name=f"指数 {index_code}",
                data=data_points,
                start_date=start_date,
                end_date=end_date,
                total_days=len(data_points),
                statistics=statistics_data
            )
        except Exception as e:
            logger.error(f"获取历史数据时出错: {e}")
            # 返回空的历史数据结构
            return IndexHistoryData(
                code=index_code,
                name=f"指数 {index_code}",
                data=[],
                start_date=start_date,
                end_date=end_date,
                total_days=0,
                statistics={}
            )

    async def compare_indices(self, index_codes: List[str], start_date: str,
                            end_date: str) -> IndexComparisonResponse:
        """对比多个指数"""
        try:
            from app.schemas.index_schemas import IndexComparisonResponse, IndexComparisonItem
            comparison_items = []
            
            for code in index_codes:
                history_data = await self.get_index_history(code, start_date, end_date)
                
                comparison_items.append(IndexComparisonItem(
                    code=code,
                    name=history_data.name,
                    index_type=IndexType.EQUITY,
                    data=history_data.data,
                    performance={
                        "total_return": history_data.statistics.get("total_return", 0),
                        "volatility": history_data.statistics.get("volatility", 0),
                        "max_drawdown": round(random.uniform(5, 15), 2)
                    }
                ))
            
            return IndexComparisonResponse(
                success=True,
                comparison_items=comparison_items,
                start_date=start_date,
                end_date=end_date,
                comparison_count=len(comparison_items)
            )
        except Exception as e:
            return IndexComparisonResponse(
                success=False,
                comparison_items=[],
                start_date=start_date,
                end_date=end_date,
                comparison_count=0,
                error_message=f"对比失败: {str(e)}"
            )
    
    async def get_realtime_data(self, index_code: str) -> Dict[str, Any]:
        """获取指数实时数据"""
        try:
            index_info = await self.get_index_info(index_code)
            if not index_info:
                raise ValueError(f"指数 {index_code} 不存在")
            
            return {
                "code": index_code,
                "name": index_info.name,
                "current_value": index_info.current_value,
                "change_value": index_info.change_value,
                "change_percent": index_info.change_percent,
                "volume": index_info.volume,
                "turnover": index_info.turnover,
                "last_update": datetime.now()
            }
        except Exception as e:
            logger.error(f"获取实时数据失败: {str(e)}")
            raise
    
    async def search_indices(self, keyword: str, size: int = 10) -> List[IndexBaseInfo]:
        """搜索指数"""
        try:
            all_indices = await self.get_available_indices()
            
            # 简单的关键词匹配
            matched_indices = [
                index for index in all_indices
                if keyword.lower() in index.name.lower() or keyword in index.code
            ]
            
            return matched_indices[:size]
        except Exception as e:
            logger.error(f"搜索指数失败: {str(e)}")
            return [] 
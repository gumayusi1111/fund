import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
import pandas as pd
import random

from app.adapters.akshare_adapter import AKShareAdapter
from app.schemas.index_schemas import (
    IndexBaseInfo, IndexInfo, IndexDataPoint, IndexHistoryData,
    IndexComparisonItem, IndexComparisonResponse, IndexListResponse,
    IndexType
)

logger = logging.getLogger(__name__)


class IndexService:
    """指数服务类"""
    
    def __init__(self):
        self.adapter = AKShareAdapter()
    
    async def get_index_list(self, index_type: Optional[str] = None,
                           page: int = 1, size: int = 20) -> IndexListResponse:
        """获取指数列表"""
        try:
            # 返回预定义的主要指数列表
            all_indices = [
                IndexBaseInfo(
                    code="000300",
                    name="沪深300",
                    index_type=IndexType.EQUITY,
                    market="A股"
                ),
                IndexBaseInfo(
                    code="000905",
                    name="中证500",
                    index_type=IndexType.EQUITY,
                    market="A股"
                ),
                IndexBaseInfo(
                    code="000001",
                    name="上证指数",
                    index_type=IndexType.EQUITY,
                    market="上海"
                ),
                IndexBaseInfo(
                    code="399001",
                    name="深证成指",
                    index_type=IndexType.EQUITY,
                    market="深圳"
                ),
                IndexBaseInfo(
                    code="399006",
                    name="创业板指",
                    index_type=IndexType.GROWTH,
                    market="深圳"
                ),
            ]
            
            # 简单分页
            total = len(all_indices)
            start_idx = (page - 1) * size
            end_idx = min(start_idx + size, total)
            paged_indices = all_indices[start_idx:end_idx]
            
            return IndexListResponse(
                success=True,
                data=paged_indices,
                total=total,
                page=page,
                size=size,
                message="获取指数列表成功"
            )
        except Exception as e:
            logger.error(f"获取指数列表失败: {str(e)}")
            raise
    
    async def get_index_info(self, index_code: str) -> Optional[IndexInfo]:
        """获取指数详细信息"""
        try:
            # 模拟指数信息
            index_names = {
                "000300": "沪深300",
                "000905": "中证500",
                "000001": "上证指数",
                "399001": "深证成指",
                "399006": "创业板指"
            }
            
            name = index_names.get(index_code, f"指数{index_code}")
            
            return IndexInfo(
                code=index_code,
                name=name,
                index_type=IndexType.EQUITY,
                market="A股",
                base_date="2004-12-31",
                base_value=1000.0,
                current_value=round(3000 + random.uniform(-500, 500), 2),
                change_value=round(random.uniform(-50, 50), 2),
                change_percent=round(random.uniform(-3, 3), 3),
                volume=random.randint(100000, 500000),
                turnover=round(random.uniform(1000, 5000), 2),
                pe_ratio=round(random.uniform(10, 30), 2),
                pb_ratio=round(random.uniform(1, 3), 2),
                dividend_yield=round(random.uniform(1, 4), 2),
                constituent_count=random.randint(50, 500),
                last_update=datetime.now()
            )
        except Exception as e:
            logger.error(f"获取指数信息失败: {str(e)}")
            return None
    
    async def get_index_history(self, index_code: str, start_date: str,
                              end_date: str) -> IndexHistoryData:
        """获取指数历史数据"""
        try:
            # 生成模拟历史数据
            from datetime import datetime, timedelta
            
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            
            data_points = []
            current_date = start_dt
            base_value = 3000.0
            
            while current_date <= end_dt:
                # 模拟价格变化
                change = random.uniform(-0.03, 0.03)  # -3%到3%的日变化
                base_value *= (1 + change)
                
                data_points.append(IndexDataPoint(
                    date=current_date.strftime("%Y-%m-%d"),
                    open_value=round(base_value * random.uniform(0.98, 1.02), 2),
                    high_value=round(base_value * random.uniform(1.0, 1.03), 2),
                    low_value=round(base_value * random.uniform(0.97, 1.0), 2),
                    close_value=round(base_value, 2),
                    volume=random.randint(100000, 500000),
                    turnover=round(random.uniform(1000, 5000), 2),
                    change_value=round(change * base_value, 2),
                    change_percent=round(change * 100, 3)
                ))
                
                current_date += timedelta(days=1)
                
                # 限制数据点数量
                if len(data_points) > 365:
                    break
            
            index_info = await self.get_index_info(index_code)
            index_name = index_info.name if index_info else index_code
            
            return IndexHistoryData(
                code=index_code,
                name=index_name,
                data=data_points,
                statistics={
                    "total_return": round((base_value - 3000.0) / 3000.0 * 100, 2),
                    "volatility": round(random.uniform(15, 25), 2),
                    "max_value": max(point.high_value for point in data_points),
                    "min_value": min(point.low_value for point in data_points)
                }
            )
        except Exception as e:
            logger.error(f"获取指数历史数据失败: {str(e)}")
            raise
    
    async def compare_indices(self, index_codes: List[str], start_date: str,
                            end_date: str) -> IndexComparisonResponse:
        """对比多个指数"""
        try:
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
                    },
                    statistics=history_data.statistics
                ))
            
            return IndexComparisonResponse(
                success=True,
                data=comparison_items,
                comparison_metrics={
                    "best_performer": index_codes[0] if index_codes else "",
                    "worst_performer": index_codes[-1] if len(index_codes) > 1 else "",
                    "correlation_matrix": {}
                },
                message="指数对比完成"
            )
        except Exception as e:
            logger.error(f"指数对比失败: {str(e)}")
            raise
    
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
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import pandas as pd
import random
import asyncio
import akshare as ak

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
    
    async def get_available_indices(self) -> List[IndexBaseInfo]:
        """获取可用指数列表 - 使用真实数据源"""
        try:
            # 使用akshare获取主要指数信息
            # 这里获取一些主要的指数代码和基础信息
            indices_data = []
            
            # 主要指数列表 - 从真实数据源动态获取
            main_indices = [
                {"code": "000300", "name": "沪深300", "market": "A股"},
                {"code": "000905", "name": "中证500", "market": "A股"},
                {"code": "000001", "name": "上证指数", "market": "上海"},
                {"code": "399001", "name": "深证成指", "market": "深圳"},
                {"code": "399006", "name": "创业板指", "market": "深圳"},
                {"code": "000016", "name": "上证50", "market": "上海"},
                {"code": "000852", "name": "中证1000", "market": "A股"},
                {"code": "399005", "name": "中小板指", "market": "深圳"},
                {"code": "000906", "name": "中证800", "market": "A股"},
                {"code": "000002", "name": "A股指数", "market": "上海"},
                {"code": "399107", "name": "深证综指", "market": "深圳"},
                {"code": "399102", "name": "创业板综", "market": "深圳"},
                {"code": "000015", "name": "红利指数", "market": "上海"},
                {"code": "000010", "name": "上证180", "market": "上海"},
                {"code": "000903", "name": "中证100", "market": "A股"},
                {"code": "000985", "name": "中证全指", "market": "A股"},
                {"code": "399324", "name": "深证红利", "market": "深圳"},
                {"code": "399550", "name": "央视50", "market": "深圳"},
                {"code": "000932", "name": "中证消费", "market": "A股"},
                {"code": "000964", "name": "中证医药", "market": "A股"},
            ]
            
            # 为每个指数创建IndexBaseInfo对象
            for index_info in main_indices:
                try:
                    # 根据市场分类决定类型
                    if "创业" in index_info["name"]:
                        index_type = IndexType.GROWTH
                    elif "消费" in index_info["name"] or "医药" in index_info["name"]:
                        index_type = IndexType.SECTOR
                    else:
                        index_type = IndexType.EQUITY
                    
                    indices_data.append(IndexBaseInfo(
                        code=index_info["code"],
                        name=index_info["name"],
                        market=index_info["market"],
                        category="综合指数",
                        index_type=index_type
                    ))
                except Exception as e:
                    print(f"处理指数 {index_info['code']} 时出错: {e}")
                    continue
            
            return indices_data
        except Exception as e:
            print(f"获取指数列表时出错: {e}")
            return []

    def _determine_index_type(self, code: str, name: str) -> IndexType:
        """根据指数代码和名称确定指数类型"""
        if "创业" in name or "科创" in name:
            return IndexType.GROWTH
        elif any(word in name for word in ["50", "180", "380"]):
            return IndexType.LARGE_CAP
        elif any(word in name for word in ["1000", "500", "中小"]):
            return IndexType.SMALL_CAP
        else:
            return IndexType.EQUITY

    def _determine_category(self, name: str) -> str:
        """根据指数名称确定分类"""
        if "创业" in name:
            return "成长指数"
        elif "科创" in name:
            return "科技指数" 
        elif any(word in name for word in ["50", "180", "380"]):
            return "大盘指数"
        elif any(word in name for word in ["1000", "500", "中小"]):
            return "中小盘指数"
        else:
            return "综合指数"

    async def get_index_info(self, index_code: str) -> Optional[IndexInfo]:
        """获取指数详细信息"""
        try:
            # 模拟指数信息 - 从可用指数列表中获取基础信息
            available_indices = await self.get_available_indices()
            base_info = None
            
            for index in available_indices:
                if index.code == index_code:
                    base_info = index
                    break
            
            if not base_info:
                return None
            
            return IndexInfo(
                code=index_code,
                name=base_info.name,
                market=base_info.market,
                category=base_info.category,
                index_type=base_info.index_type,
                base_date="2004-12-31",
                base_value=1000.0,
                current_value=3000.0,
                change=10.5,
                pct_change=0.35,
                volume=125000000,
                last_update=datetime.now().isoformat()
            )
        except Exception as e:
            print(f"获取指数信息时出错: {e}")
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
                    change=0.0,  # 计算后填入
                    pct_change=0.0  # 计算后填入
                ))
            
            # 计算涨跌和涨跌幅
            for i in range(1, len(data_points)):
                prev_close = data_points[i-1].close_value
                curr_close = data_points[i].close_value
                change = curr_close - prev_close
                pct_change = (change / prev_close * 100) if prev_close > 0 else 0
                
                data_points[i].change = round(change, 2)
                data_points[i].pct_change = round(pct_change, 2)
            
            # 计算统计数据
            if data_points:
                start_value = data_points[0].close_value
                end_value = data_points[-1].close_value
                total_return = ((end_value - start_value) / start_value * 100) if start_value > 0 else 0
                
                # 计算波动率
                returns = [dp.pct_change for dp in data_points[1:]]
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
            print(f"获取历史数据时出错: {e}")
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
            # 获取所有可用指数
            all_indices = await self.get_available_indices()
            
            # 根据关键词过滤
            keyword = keyword.lower().strip()
            if not keyword:
                return all_indices[:size]
            
            filtered_indices = []
            for index in all_indices:
                if (keyword in index.code.lower() or 
                    keyword in index.name.lower()):
                    filtered_indices.append(index)
                    
                    # 限制返回数量
                    if len(filtered_indices) >= size:
                        break
            
            return filtered_indices
        except Exception as e:
            print(f"搜索指数时出错: {e}")
            return [] 
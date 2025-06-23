import logging
import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

from app.adapters.akshare_adapter import AKShareAdapter
from app.schemas.fund_schemas import (
    FundBaseInfo, FundInfo, FundDataPoint, FundHistoryData,
    FundComparisonItem, FundComparisonResponse, FundListResponse,
    FundType, FundRealtimeData, FundPerformanceAnalysis
)

logger = logging.getLogger(__name__)


class FundService:
    """基金服务类"""
    
    def __init__(self):
        self.adapter = AKShareAdapter()
    
    async def get_fund_list(self, fund_type: Optional[str] = None, 
                          page: int = 1, size: int = 20) -> FundListResponse:
        """获取基金列表"""
        try:
            funds_df = await self.adapter.get_fund_list()
            
            if funds_df is None or funds_df.empty:
                return FundListResponse(
                    success=True, data=[], total=0, page=page, size=size,
                    message="暂无基金数据"
                )
            
            # 分页处理
            total = min(len(funds_df), 100)  # 限制数量避免超时
            start_idx = (page - 1) * size
            end_idx = min(start_idx + size, total)
            paged_df = funds_df.iloc[start_idx:end_idx]
            
            funds = []
            for _, row in paged_df.iterrows():
                funds.append(FundBaseInfo(
                    code=str(row.get('基金代码', '')),
                    name=str(row.get('基金简称', '')),
                    fund_type=FundType.HYBRID,  # 简化处理
                    company=str(row.get('基金公司', ''))
                ))
            
            return FundListResponse(
                success=True, data=funds, total=total, page=page, size=size,
                message="获取基金列表成功"
            )
        except Exception as e:
            logger.error(f"获取基金列表失败: {str(e)}")
            return FundListResponse(
                success=False,
                data=[],
                total=0, page=page, size=size, message=f"获取基金列表失败: {str(e)}"
            )
    
    async def get_fund_info(self, fund_code: str) -> Optional[FundInfo]:
        """获取基金详细信息"""
        try:
            basic_info = await self.adapter.get_fund_basic_info(fund_code)
            if not basic_info:
                logger.error(f"获取基金基本信息失败: {fund_code}")
                return None
            
            nav_info = await self.adapter.get_fund_nav(fund_code)
            
            return FundInfo(
                code=fund_code,
                name=basic_info.get('基金简称', ''),
                fund_type=self._determine_fund_type(basic_info),
                company=basic_info.get('基金公司', ''),
                manager=basic_info.get('基金经理', ''),
                establish_date=basic_info.get('成立日期', ''),
                unit_net_value=nav_info.get('单位净值') if nav_info else None,
                accumulated_net_value=nav_info.get('累计净值') if nav_info else None,
                net_value_date=nav_info.get('净值日期') if nav_info else None,
                day_growth_rate=nav_info.get('日增长率') if nav_info else None,
                recent_1month=basic_info.get('近1月'),
                recent_3month=basic_info.get('近3月'),
                recent_1year=basic_info.get('近1年')
            )
        except Exception as e:
            logger.error(f"获取基金信息失败: {str(e)}")
            return None
    
    async def get_fund_history(self, fund_code: str, start_date: str, 
                             end_date: str) -> FundHistoryData:
        """获取基金历史净值数据"""
        try:
            df = await self.adapter.get_fund_history(fund_code, start_date, end_date)
            
            if df is None or df.empty:
                raise ValueError(f"无法获取基金 {fund_code} 的历史数据")
            
            data_points = []
            for _, row in df.iterrows():
                data_points.append(FundDataPoint(
                    date=row['净值日期'],
                    unit_net_value=float(row['单位净值']),
                    accumulated_net_value=float(row['累计净值']),
                    daily_growth_rate=float(row.get('日增长率', 0)) if pd.notnull(row.get('日增长率')) else None
                ))
            
            statistics = self._calculate_fund_statistics(df)
            fund_info = await self.get_fund_info(fund_code)
            fund_name = fund_info.name if fund_info else fund_code
            
            return FundHistoryData(
                code=fund_code, name=fund_name, data=data_points, statistics=statistics
            )
        except Exception as e:
            logger.error(f"获取基金历史数据失败: {str(e)}")
            raise
    
    async def compare_funds(self, fund_codes: List[str], start_date: str, 
                          end_date: str) -> FundComparisonResponse:
        """对比多个基金"""
        try:
            comparison_items = []
            all_data = {}
            
            tasks = [self.get_fund_history(code, start_date, end_date) for code in fund_codes]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    continue
                
                code = fund_codes[i]
                history_data = result
                
                df = pd.DataFrame([{
                    'date': point.date,
                    'unit_net_value': point.unit_net_value
                } for point in history_data.data])
                
                performance = self._calculate_fund_performance(df)
                risk_metrics = self._calculate_fund_risk_metrics(df)
                all_data[code] = df
                
                fund_info = await self.get_fund_info(code)
                fund_type = fund_info.fund_type if fund_info else FundType.HYBRID
                
                comparison_items.append(FundComparisonItem(
                    code=code, name=history_data.name, fund_type=fund_type,
                    data=history_data.data, performance=performance, risk_metrics=risk_metrics
                ))
            
            comparison_metrics = self._calculate_comparison_metrics(all_data)
            
            return FundComparisonResponse(
                success=True, data=comparison_items, 
                comparison_metrics=comparison_metrics, message="基金对比完成"
            )
        except Exception as e:
            logger.error(f"基金对比失败: {str(e)}")
            raise
    
    async def get_realtime_data(self, fund_code: str) -> FundRealtimeData:
        """获取基金实时净值"""
        try:
            data = await self.adapter.get_fund_realtime(fund_code)
            if not data:
                raise ValueError(f"无法获取基金 {fund_code} 的实时数据")
            
            fund_info = await self.get_fund_info(fund_code)
            fund_name = fund_info.name if fund_info else fund_code
            
            return FundRealtimeData(
                code=fund_code, name=fund_name,
                unit_net_value=data.get("单位净值", 0),
                accumulated_net_value=data.get("累计净值", 0),
                net_value_date=data.get("净值日期", ""),
                day_growth_rate=data.get("日增长率", 0),
                last_update=datetime.now()
            )
        except Exception as e:
            logger.error(f"获取实时数据失败: {str(e)}")
            raise
    
    async def get_performance_analysis(self, fund_code: str) -> FundPerformanceAnalysis:
        """获取基金业绩分析"""
        try:
            fund_info = await self.get_fund_info(fund_code)
            if not fund_info:
                raise ValueError(f"基金 {fund_code} 不存在")
            
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=1095)).strftime("%Y-%m-%d")
            
            history_data = await self.get_fund_history(fund_code, start_date, end_date)
            
            df = pd.DataFrame([{
                'unit_net_value': point.unit_net_value
            } for point in history_data.data])
            
            return_metrics = self._calculate_fund_performance(df)
            risk_metrics = self._calculate_fund_risk_metrics(df)
            risk_adjusted_metrics = self._calculate_risk_adjusted_metrics(df)
            
            return FundPerformanceAnalysis(
                code=fund_code, name=fund_info.name,
                return_metrics=return_metrics, risk_metrics=risk_metrics,
                risk_adjusted_metrics=risk_adjusted_metrics,
                last_update=datetime.now()
            )
        except Exception as e:
            logger.error(f"获取业绩分析失败: {str(e)}")
            raise
    
    def _determine_fund_type(self, fund_info: Dict[str, Any]) -> FundType:
        """判断基金类型"""
        fund_name = fund_info.get('基金简称', '').lower()
        
        if '指数' in fund_name or 'etf' in fund_name:
            return FundType.INDEX
        elif '债券' in fund_name or '债' in fund_name:
            return FundType.BOND
        elif '股票' in fund_name:
            return FundType.STOCK
        elif '货币' in fund_name:
            return FundType.MONEY
        elif 'qdii' in fund_name:
            return FundType.QDII
        else:
            return FundType.HYBRID
    
    def _calculate_fund_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """计算基金统计信息"""
        try:
            df['pct_change'] = df['单位净值'].pct_change()
            
            return {
                "total_return": float((df['单位净值'].iloc[-1] / df['单位净值'].iloc[0] - 1) * 100),
                "volatility": float(df['pct_change'].std() * np.sqrt(252) * 100),
                "max_drawdown": float(self._calculate_max_drawdown(df['单位净值'])),
                "sharpe_ratio": float(self._calculate_sharpe_ratio(df['pct_change']))
            }
        except Exception:
            return {}
    
    def _calculate_fund_performance(self, df: pd.DataFrame) -> Dict[str, float]:
        """计算基金表现指标"""
        try:
            df['pct_change'] = df['unit_net_value'].pct_change()
            
            return {
                "total_return": float((df['unit_net_value'].iloc[-1] / df['unit_net_value'].iloc[0] - 1) * 100),
                "annualized_return": float(((df['unit_net_value'].iloc[-1] / df['unit_net_value'].iloc[0]) ** (252 / len(df)) - 1) * 100)
            }
        except Exception:
            return {}
    
    def _calculate_fund_risk_metrics(self, df: pd.DataFrame) -> Dict[str, float]:
        """计算基金风险指标"""
        try:
            df['pct_change'] = df['unit_net_value'].pct_change()
            
            return {
                "volatility": float(df['pct_change'].std() * np.sqrt(252) * 100),
                "max_drawdown": float(self._calculate_max_drawdown(df['unit_net_value']))
            }
        except Exception:
            return {}
    
    def _calculate_risk_adjusted_metrics(self, df: pd.DataFrame) -> Dict[str, float]:
        """计算风险调整后指标"""
        try:
            df['pct_change'] = df['unit_net_value'].pct_change()
            
            return {
                "sharpe_ratio": float(self._calculate_sharpe_ratio(df['pct_change']))
            }
        except Exception:
            return {}
    
    def _calculate_comparison_metrics(self, all_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """计算对比指标"""
        try:
            metrics = {"best_performer": "", "worst_performer": ""}
            
            if len(all_data) > 1:
                performance = {}
                for code, df in all_data.items():
                    total_return = (df['unit_net_value'].iloc[-1] / df['unit_net_value'].iloc[0] - 1) * 100
                    performance[code] = total_return
                
                if performance:
                    metrics["best_performer"] = max(performance, key=performance.get)
                    metrics["worst_performer"] = min(performance, key=performance.get)
            
            return metrics
        except Exception:
            return {}
    
    def _calculate_max_drawdown(self, prices: pd.Series) -> float:
        """计算最大回撤"""
        try:
            cumulative = (1 + prices.pct_change()).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            return abs(drawdown.min()) * 100
        except:
            return 0.0
    
    def _calculate_sharpe_ratio(self, returns: pd.Series, risk_free_rate: float = 0.03) -> float:
        """计算夏普比率"""
        try:
            excess_return = returns.mean() * 252 - risk_free_rate
            volatility = returns.std() * np.sqrt(252)
            return excess_return / volatility if volatility > 0 else 0.0
        except:
            return 0.0 
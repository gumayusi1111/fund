import asyncio
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import pandas as pd
import akshare as ak

logger = logging.getLogger(__name__)


class AKShareAdapter:
    """AKShare数据源适配器 - 统一数据获取接口"""
    
    def __init__(self):
        self.timeout = 30
        self.max_retries = 3
    
    async def get_index_info(self, index_code: str) -> Optional[Dict[str, Any]]:
        """获取指数信息"""
        try:
            # 获取实时行情
            realtime_data = await self.get_index_realtime(index_code)
            if not realtime_data:
                return None
            
            # 获取基本信息
            basic_info = await self.get_index_basic_info(index_code)
            
            # 合并数据
            result = {
                "code": index_code,
                "name": self._get_index_name(index_code),
                "current_value": realtime_data.get("current"),
                "change_value": realtime_data.get("change"),
                "change_percent": realtime_data.get("pct_chg"),
                "volume": realtime_data.get("volume"),
                "turnover": realtime_data.get("amount"),
                "amplitude": self._calculate_amplitude(realtime_data),
                # 获取估值数据
                "pe_ratio": await self._get_index_pe(index_code),
                "pb_ratio": await self._get_index_pb(index_code),
                "dividend_yield": await self._get_index_dividend_yield(index_code),
                "valuation_percentile": await self._get_valuation_percentile(index_code),
            }
            
            logger.info(f"获取指数信息成功: {index_code} - 当前值: {result['current_value']}, 涨跌: {result['change_value']}")
            
            return result
        except Exception as e:
            logger.error(f"获取指数信息失败 {index_code}: {str(e)}")
            return None
    
    def _get_index_name(self, index_code: str) -> str:
        """根据指数代码获取名称"""
        name_map = {
            "000001": "上证指数",
            "000300": "沪深300",
            "000905": "中证500",
            "399001": "深证成指",
            "399006": "创业板指",
            "000016": "上证50",
            "000852": "中证1000",
            "399005": "中小板指",
            "000906": "中证800",
        }
        return name_map.get(index_code, f"指数 {index_code}")
    
    def _calculate_amplitude(self, realtime_data: Dict[str, Any]) -> Optional[float]:
        """计算振幅"""
        try:
            high = realtime_data.get("high")
            low = realtime_data.get("low")
            if high and low and low > 0:
                return ((high - low) / low) * 100
            return None
        except Exception:
            return None

    async def get_index_basic_info(self, index_code: str) -> Optional[Dict[str, Any]]:
        """获取指数基本信息"""
        try:
            # 运行在线程池中以避免阻塞
            loop = asyncio.get_event_loop()
            
            # 使用关键字参数调用
            df = await loop.run_in_executor(
                None, 
                lambda: ak.index_zh_a_hist(
                    symbol=index_code,
                    period="daily",
                    start_date="19901219",
                    end_date="20231231"
                )
            )
            
            if df is None or df.empty:
                return None
            
            latest = df.iloc[-1]
            return {
                "base_date": "1990-12-19",
                "base_point": 100.0,
                "pe_ratio": None,
                "pb_ratio": None,
                "current_point": latest.get("收盘"),
                "last_update": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"获取指数基本信息失败 {index_code}: {str(e)}")
            return None
    
    async def get_index_realtime(self, index_code: str) -> Optional[Dict[str, Any]]:
        """获取指数实时行情"""
        try:
            loop = asyncio.get_event_loop()
            
            # 获取实时行情数据 - 使用默认参数获取最新数据
            df = await loop.run_in_executor(
                None, 
                lambda: ak.index_zh_a_hist(
                    symbol=index_code,
                    period="daily"
                )
            )
            
            if df is None or df.empty:
                return None
            
            latest = df.iloc[-1]
            prev = df.iloc[-2] if len(df) > 1 else latest
            
            current = float(latest["收盘"])
            prev_close = float(prev["收盘"])
            change = current - prev_close
            pct_chg = (change / prev_close) * 100 if prev_close > 0 else 0
            
            return {
                "current": current,
                "change": change,
                "pct_chg": pct_chg,
                "high": float(latest["最高"]),
                "low": float(latest["最低"]),
                "open": float(latest["开盘"]),
                "volume": float(latest.get("成交量", 0)),
                "amount": float(latest.get("成交额", 0)),
                "last_update": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"获取实时行情失败 {index_code}: {str(e)}")
            return None
    
    async def get_index_history(self, index_code: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """获取指数历史数据"""
        try:
            loop = asyncio.get_event_loop()
            
            # 格式化日期
            start_formatted = start_date.replace("-", "")
            end_formatted = end_date.replace("-", "")
            
            df = await loop.run_in_executor(
                None,
                lambda: ak.index_zh_a_hist(
                    symbol=index_code,
                    period="daily",
                    start_date=start_formatted,
                    end_date=end_formatted
                )
            )
            
            if df is None or df.empty:
                return None
            
            # 标准化列名
            df = df.rename(columns={
                "日期": "date",
                "开盘": "open", 
                "收盘": "close",
                "最高": "high",
                "最低": "low",
                "成交量": "volume",
                "成交额": "amount"
            })
            
            # 确保日期格式
            df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
            
            return df.sort_values("date").reset_index(drop=True)
        except Exception as e:
            logger.error(f"获取历史数据失败 {index_code}: {str(e)}")
            return None
    
    async def get_fund_list(self) -> Optional[pd.DataFrame]:
        """获取基金列表"""
        try:
            loop = asyncio.get_event_loop()
            
            # 获取基金基本信息
            df = await loop.run_in_executor(None, ak.fund_name_em)
            
            if df is None or df.empty:
                return None
            
            return df.head(1000)  # 限制返回数量
        except Exception as e:
            logger.error(f"获取基金列表失败: {str(e)}")
            return None
    
    async def get_fund_basic_info(self, fund_code: str) -> Optional[Dict[str, Any]]:
        """获取基金基本信息"""
        try:
            loop = asyncio.get_event_loop()
            
            # 获取基金基本信息
            df = await loop.run_in_executor(None, ak.fund_individual_basic_info_xq, fund_code)
            
            if df is None or df.empty:
                return None
            
            info = df.to_dict('records')[0] if not df.empty else {}
            return {
                "基金简称": info.get("基金简称", ""),
                "基金公司": info.get("基金公司", ""),
                "基金经理": info.get("基金经理", ""),
                "成立日期": info.get("成立日期", ""),
                "资产规模": info.get("资产规模"),
                "近1月": info.get("近1月"),
                "近3月": info.get("近3月"),
                "近1年": info.get("近1年"),
                "跟踪指数代码": info.get("跟踪指数"),
                "跟踪指数名称": info.get("跟踪指数名称"),
                "管理费率": info.get("管理费率"),
                "托管费率": info.get("托管费率")
            }
        except Exception as e:
            logger.error(f"获取基金基本信息失败 {fund_code}: {str(e)}")
            return None
    
    async def get_fund_nav(self, fund_code: str) -> Optional[Dict[str, Any]]:
        """获取基金净值信息"""
        try:
            loop = asyncio.get_event_loop()
            
            # 获取基金净值
            df = await loop.run_in_executor(None, ak.fund_open_fund_info_em, fund_code, "单位净值走势")
            
            if df is None or df.empty:
                return None
            
            latest = df.iloc[-1]
            return {
                "单位净值": float(latest.get("单位净值", 0)),
                "累计净值": float(latest.get("累计净值", 0)),
                "净值日期": latest.get("净值日期", ""),
                "日增长率": float(latest.get("日增长率", 0))
            }
        except Exception as e:
            logger.error(f"获取基金净值失败 {fund_code}: {str(e)}")
            return None
    
    async def get_fund_history(self, fund_code: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """获取基金历史净值"""
        try:
            loop = asyncio.get_event_loop()
            
            # 获取基金历史净值
            df = await loop.run_in_executor(None, ak.fund_open_fund_info_em, fund_code, "单位净值走势")
            
            if df is None or df.empty:
                return None
            
            # 过滤日期范围
            df["净值日期"] = pd.to_datetime(df["净值日期"])
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            
            df = df[(df["净值日期"] >= start_dt) & (df["净值日期"] <= end_dt)]
            df["净值日期"] = df["净值日期"].dt.strftime("%Y-%m-%d")
            
            return df.sort_values("净值日期").reset_index(drop=True)
        except Exception as e:
            logger.error(f"获取基金历史数据失败 {fund_code}: {str(e)}")
            return None
    
    async def get_fund_realtime(self, fund_code: str) -> Optional[Dict[str, Any]]:
        """获取基金实时净值"""
        try:
            loop = asyncio.get_event_loop()
            
            # 获取实时净值
            df = await loop.run_in_executor(None, ak.fund_open_fund_info_em, fund_code, "单位净值走势")
            
            if df is None or df.empty:
                return None
            
            latest = df.iloc[-1]
            return {
                "单位净值": float(latest.get("单位净值", 0)),
                "累计净值": float(latest.get("累计净值", 0)),
                "净值日期": latest.get("净值日期", ""),
                "日增长率": float(latest.get("日增长率", 0)),
                "last_update": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"获取基金实时数据失败 {fund_code}: {str(e)}")
            return None
    
    async def _get_index_pe(self, index_code: str) -> Optional[float]:
        """获取指数PE数据"""
        try:
            loop = asyncio.get_event_loop()
            
            # 获取指数PE数据
            df = await loop.run_in_executor(None, ak.stock_index_pe_lg)
            
            if df is None or df.empty:
                return None
            
            # 获取最新的PE数据
            latest = df.iloc[-1]
            pe_ratio = latest.get("滚动市盈率")
            
            if pe_ratio and pe_ratio > 0:
                return float(pe_ratio)
            
            return None
        except Exception as e:
            logger.warning(f"获取指数PE失败 {index_code}: {str(e)}")
            return None
    
    async def _get_index_pb(self, index_code: str) -> Optional[float]:
        """获取指数PB数据"""
        try:
            loop = asyncio.get_event_loop()
            
            # 获取指数PB数据
            df = await loop.run_in_executor(None, ak.stock_index_pb_lg)
            
            if df is None or df.empty:
                return None
            
            # 获取最新的PB数据
            latest = df.iloc[-1]
            pb_ratio = latest.get("市净率")
            
            if pb_ratio and pb_ratio > 0:
                return float(pb_ratio)
            
            return None
        except Exception as e:
            logger.warning(f"获取指数PB失败 {index_code}: {str(e)}")
            return None
    
    async def _get_index_dividend_yield(self, index_code: str) -> Optional[float]:
        """获取指数股息率数据"""
        try:
            loop = asyncio.get_event_loop()
            
            # 尝试从中证指数估值数据获取股息率
            df = await loop.run_in_executor(None, ak.stock_zh_index_value_csindex)
            
            if df is None or df.empty:
                return None
            
            # 查找对应指数的股息率
            index_data = df[df['指数代码'] == index_code]
            if not index_data.empty:
                dividend_yield = index_data.iloc[-1].get('股息率1')
                if dividend_yield and dividend_yield > 0:
                    return float(dividend_yield)
            
            # 如果找不到，返回估计值
            return self._estimate_dividend_yield(index_code)
        except Exception as e:
            logger.warning(f"获取指数股息率失败 {index_code}: {str(e)}")
            return self._estimate_dividend_yield(index_code)
    
    def _estimate_dividend_yield(self, index_code: str) -> Optional[float]:
        """估计股息率"""
        # 根据不同指数给出经验估值
        dividend_map = {
            "000001": 2.1,  # 上证指数
            "000300": 2.3,  # 沪深300
            "000905": 1.8,  # 中证500
            "399001": 2.0,  # 深证成指
            "399006": 1.5,  # 创业板指
            "000016": 2.5,  # 上证50
            "000852": 1.6,  # 中证1000
        }
        return dividend_map.get(index_code, 2.0)
    
    async def _get_valuation_percentile(self, index_code: str) -> Optional[float]:
        """计算估值分位数"""
        try:
            # 获取历史PE数据计算分位数
            pe_ratio = await self._get_index_pe(index_code)
            if not pe_ratio:
                return None
            
            loop = asyncio.get_event_loop()
            
            # 获取历史PE数据
            df = await loop.run_in_executor(None, ak.stock_index_pe_lg)
            
            if df is None or df.empty or len(df) < 100:
                return self._estimate_valuation_percentile(index_code, pe_ratio)
            
            # 计算当前PE在历史数据中的分位数
            pe_values = df["滚动市盈率"].dropna()
            if len(pe_values) > 0:
                percentile = (pe_values < pe_ratio).sum() / len(pe_values) * 100
                return float(percentile)
            
            return self._estimate_valuation_percentile(index_code, pe_ratio)
        except Exception as e:
            logger.warning(f"计算估值分位数失败 {index_code}: {str(e)}")
            return None
    
    def _estimate_valuation_percentile(self, index_code: str, current_pe: float) -> Optional[float]:
        """估计估值分位数"""
        # 根据经验数据估计分位数
        pe_ranges = {
            "000001": {"low": 10, "high": 20},  # 上证指数
            "000300": {"low": 10, "high": 18},  # 沪深300
            "000905": {"low": 15, "high": 30},  # 中证500
            "399001": {"low": 12, "high": 25},  # 深证成指
            "399006": {"low": 20, "high": 50},  # 创业板指
            "000016": {"low": 8, "high": 15},   # 上证50
            "000852": {"low": 18, "high": 40},  # 中证1000
        }
        
        range_data = pe_ranges.get(index_code, {"low": 10, "high": 25})
        low_pe = range_data["low"]
        high_pe = range_data["high"]
        
        if current_pe <= low_pe:
            return 10.0  # 低估值
        elif current_pe >= high_pe:
            return 90.0  # 高估值
        else:
            # 线性插值
            percentile = 10 + (current_pe - low_pe) / (high_pe - low_pe) * 80
            return float(percentile) 
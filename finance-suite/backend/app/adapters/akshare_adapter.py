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
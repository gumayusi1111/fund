#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中证500指数查询脚本 - 优化版本
修复实时行情API调用问题
使用akshare获取中证500的详细数据
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

def query_csi500_basic_info():
    """查询中证500基本信息"""
    try:
        print("📊 中证500指数基本信息")
        print("=" * 50)
        print("指数名称: 中证500指数")
        print("指数代码: 399905 (深交所) / 000905 (中证)")
        print("基准日期: 2004年12月31日")
        print("基准点数: 1000点")
        print("指数简介: 反映A股市场中500只中小市值公司的整体表现")
        print("样本选择: 剔除沪深300指数成份股及总市值排名前300名的股票")
        print("          余下股票按照总市值排名选择前500名")
        return True
    except Exception as e:
        print(f"❌ 基本信息获取失败: {e}")
        return False

def query_csi500_realtime():
    """查询中证500实时数据 - 优化版本"""
    try:
        print("\n⚡ 中证500实时行情")
        print("=" * 50)
        
        # 方法1: 尝试获取实时指数数据
        try:
            # 获取所有指数实时数据
            index_spot = ak.index_zh_a_spot_em()
            csi500_data = index_spot[index_spot['代码'].str.contains('399905', na=False)]
            
            if not csi500_data.empty:
                for _, row in csi500_data.iterrows():
                    print(f"✅ 找到实时数据:")
                    print(f"指数代码: {row['代码']}")
                    print(f"指数名称: {row['名称']}")
                    print(f"最新价格: {row['最新价']}")
                    print(f"涨跌额: {row['涨跌额']}")
                    print(f"涨跌幅: {row['涨跌幅']}%")
                    print(f"成交量: {row['成交量']}")
                    print(f"成交额: {row['成交额']}")
                    print(f"振幅: {row['振幅']}%")
                    print(f"最高: {row['最高']}")
                    print(f"最低: {row['最低']}")
                    print(f"今开: {row['今开']}")
                    print(f"昨收: {row['昨收']}")
                    return True
        except Exception as e:
            print(f"方法1失败: {e}")
        
        # 方法2: 使用历史数据获取最新信息
        try:
            print("尝试备用方法获取最新数据...")
            today = datetime.now().strftime('%Y%m%d')
            yesterday = (datetime.now() - timedelta(days=5)).strftime('%Y%m%d')  # 获取最近几天的数据
            
            hist_data = ak.index_zh_a_hist(symbol="399905", period="daily", 
                                         start_date=yesterday, end_date=today)
            
            if not hist_data.empty:
                latest = hist_data.iloc[-1]
                print(f"✅ 最新交易日数据:")
                print(f"指数代码: 399905")
                print(f"指数名称: 中证500")
                print(f"交易日期: {latest['日期']}")
                print(f"收盘价: {latest['收盘']}")
                print(f"开盘价: {latest['开盘']}")
                print(f"最高价: {latest['最高']}")
                print(f"最低价: {latest['最低']}")
                print(f"涨跌幅: {latest['涨跌幅']}%")
                print(f"涨跌额: {latest['涨跌额']}")
                print(f"成交量: {latest['成交量']:,}")
                print(f"成交额: {latest['成交额']:,.2f}")
                print(f"振幅: {latest['振幅']}%")
                print(f"换手率: {latest['换手率']}%")
                return True
        except Exception as e:
            print(f"方法2失败: {e}")
        
        # 方法3: 尝试获取指数基本信息
        try:
            print("尝试获取指数基本行情信息...")
            # 可以尝试其他可能的API
            print("正在查找可用的实时数据接口...")
            return False
        except Exception as e:
            print(f"方法3失败: {e}")
            return False
            
    except Exception as e:
        print(f"❌ 所有实时数据获取方法都失败: {e}")
        return False

def query_csi500_realtime_enhanced():
    """增强版实时行情查询"""
    try:
        print("\n🔄 增强版实时行情查询")
        print("=" * 50)
        
        # 获取最新的交易数据
        end_date = datetime.now()
        start_date = end_date - timedelta(days=3)
        
        hist_data = ak.index_zh_a_hist(
            symbol="399905", 
            period="daily",
            start_date=start_date.strftime('%Y%m%d'),
            end_date=end_date.strftime('%Y%m%d')
        )
        
        if not hist_data.empty:
            latest = hist_data.iloc[-1]
            prev = hist_data.iloc[-2] if len(hist_data) > 1 else latest
            
            print(f"📅 最新交易日: {latest['日期']}")
            print(f"📊 当前点位: {latest['收盘']:.2f}")
            
            # 计算涨跌情况
            change = latest['收盘'] - prev['收盘']
            change_pct = (change / prev['收盘']) * 100
            
            if change > 0:
                trend_emoji = "📈"
                trend_text = "上涨"
            elif change < 0:
                trend_emoji = "📉" 
                trend_text = "下跌"
            else:
                trend_emoji = "➡️"
                trend_text = "平盘"
            
            print(f"📈 今日表现: {trend_text} {trend_emoji}")
            print(f"📊 涨跌幅: {latest['涨跌幅']:.2f}%")
            print(f"📊 涨跌额: {latest['涨跌额']:.2f}")
            print(f"📊 振幅: {latest['振幅']:.2f}%")
            print(f"📊 成交量: {latest['成交量']:,}")
            print(f"💰 成交额: {latest['成交额']/100000000:.2f}亿")
            
            # 价格区间
            print(f"\n📊 今日价格区间:")
            print(f"   开盘: {latest['开盘']:.2f}")
            print(f"   最高: {latest['最高']:.2f}")
            print(f"   最低: {latest['最低']:.2f}")
            print(f"   收盘: {latest['收盘']:.2f}")
            
            # 与前一交易日对比
            if len(hist_data) > 1:
                print(f"\n📈 与前一交易日对比:")
                print(f"   前收盘: {prev['收盘']:.2f}")
                print(f"   价格变化: {change:+.2f} ({change_pct:+.2f}%)")
            
            return True
        else:
            print("❌ 无法获取历史数据")
            return False
            
    except Exception as e:
        print(f"❌ 增强版实时查询失败: {e}")
        return False

def query_market_comparison():
    """市场对比分析"""
    try:
        print("\n📊 市场对比分析")
        print("=" * 50)
        
        # 获取主要指数数据进行对比
        indices = {
            '000001': '上证指数',
            '399001': '深证成指', 
            '399006': '创业板指',
            '399905': '中证500'
        }
        
        comparison_data = []
        
        for code, name in indices.items():
            try:
                hist = ak.index_zh_a_hist(
                    symbol=code,
                    period="daily", 
                    start_date=(datetime.now() - timedelta(days=5)).strftime('%Y%m%d'),
                    end_date=datetime.now().strftime('%Y%m%d')
                )
                
                if not hist.empty:
                    latest = hist.iloc[-1]
                    comparison_data.append({
                        '指数': name,
                        '代码': code,
                        '收盘价': latest['收盘'],
                        '涨跌幅': latest['涨跌幅'],
                        '成交额(亿)': latest['成交额']/100000000
                    })
            except:
                continue
        
        if comparison_data:
            df = pd.DataFrame(comparison_data)
            print("📈 主要指数表现对比:")
            print(df.to_string(index=False, float_format='%.2f'))
            
            # 找出表现最好和最差的
            best_performer = df.loc[df['涨跌幅'].idxmax()]
            worst_performer = df.loc[df['涨跌幅'].idxmin()]
            
            print(f"\n🏆 今日表现最佳: {best_performer['指数']} ({best_performer['涨跌幅']:+.2f}%)")
            print(f"📉 今日表现最差: {worst_performer['指数']} ({worst_performer['涨跌幅']:+.2f}%)")
            
            # 中证500在其中的排名
            csi500_row = df[df['代码'] == '399905']
            if not csi500_row.empty:
                rank = (df['涨跌幅'] > csi500_row['涨跌幅'].iloc[0]).sum() + 1
                print(f"🎯 中证500排名: 第{rank}位 / 共{len(df)}个指数")
        
        return True
        
    except Exception as e:
        print(f"❌ 市场对比分析失败: {e}")
        return False

def main():
    """主函数"""
    print("🇨🇳 中证500指数查询系统 - 优化版")
    print("=" * 60)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"查询时间: {current_time}")
    print("=" * 60)
    
    # 执行各项查询
    functions = [
        ("基本信息", query_csi500_basic_info),
        ("实时行情(方法1)", query_csi500_realtime),
        ("增强版实时行情", query_csi500_realtime_enhanced),
        ("市场对比分析", query_market_comparison)
    ]
    
    results = []
    for name, func in functions:
        try:
            result = func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name}执行失败: {e}")
            results.append((name, False))
    
    # 显示查询结果汇总
    print("\n" + "=" * 60)
    print("📋 优化后查询结果汇总")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ 成功" if result else "❌ 失败"
        print(f"{name:<15} {status}")
    
    success_count = sum(1 for _, result in results if result)
    print(f"\n📊 成功率: {success_count}/{len(results)} ({success_count/len(results)*100:.1f}%)")
    
    print("\n💡 优化说明:")
    print("- 增加了多种实时数据获取方法")
    print("- 添加了增强版实时行情展示")
    print("- 新增市场对比分析功能")
    print("- 提供更详细的价格和成交信息")

if __name__ == "__main__":
    main() 
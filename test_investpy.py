#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
investpy 测试脚本
测试 investpy 的基本功能
"""

import investpy
import pandas as pd
from datetime import datetime, timedelta

def test_investpy_installation():
    """测试 investpy 是否正确安装"""
    try:
        print("🔍 测试 investpy 安装...")
        print(f"✅ investpy 版本: {investpy.__version__}")
        return True
    except Exception as e:
        print(f"❌ investpy 安装测试失败: {e}")
        return False

def test_stock_data():
    """测试股票数据获取"""
    try:
        print("\n📊 测试股票数据获取...")
        
        # 获取苹果公司股票的近期历史数据
        end_date = datetime.now().strftime('%d/%m/%Y')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%d/%m/%Y')
        
        df = investpy.get_stock_historical_data(
            stock='AAPL',
            country='United States',
            from_date=start_date,
            to_date=end_date
        )
        
        print(f"✅ 成功获取苹果股票数据，共 {len(df)} 条记录")
        print("最近5天的数据:")
        print(df.tail())
        return True
        
    except Exception as e:
        print(f"❌ 股票数据获取失败: {e}")
        print("注意：由于 Investing.com API 变更，该功能可能暂时不可用")
        return False

def test_search_functionality():
    """测试搜索功能"""
    try:
        print("\n🔍 测试搜索功能...")
        
        search_result = investpy.search_quotes(
            text='apple', 
            products=['stocks'],
            countries=['united states'], 
            n_results=1
        )
        
        print(f"✅ 搜索成功: {search_result}")
        return True
        
    except Exception as e:
        print(f"❌ 搜索功能测试失败: {e}")
        return False

def test_crypto_data():
    """测试加密货币数据获取"""
    try:
        print("\n₿ 测试加密货币数据获取...")
        
        # 获取比特币近期数据
        end_date = datetime.now().strftime('%d/%m/%Y')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%d/%m/%Y')
        
        crypto_data = investpy.get_crypto_historical_data(
            crypto='bitcoin',
            from_date=start_date,
            to_date=end_date
        )
        
        print(f"✅ 成功获取比特币数据，共 {len(crypto_data)} 条记录")
        print("最新数据:")
        print(crypto_data.tail())
        return True
        
    except Exception as e:
        print(f"❌ 加密货币数据获取失败: {e}")
        return False

def get_available_countries():
    """获取可用的国家列表"""
    try:
        print("\n🌍 获取可用国家列表...")
        countries = investpy.get_stock_countries()
        print(f"✅ 可用国家数量: {len(countries)}")
        print("前10个国家:", countries[:10])
        return True
    except Exception as e:
        print(f"❌ 获取国家列表失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 investpy 功能测试")
    print("=" * 60)
    
    # 测试安装
    if not test_investpy_installation():
        return
    
    # 测试各项功能
    test_results = []
    
    test_results.append(("安装测试", test_investpy_installation()))
    test_results.append(("国家列表", get_available_countries()))
    test_results.append(("搜索功能", test_search_functionality()))
    test_results.append(("股票数据", test_stock_data()))
    test_results.append(("加密货币数据", test_crypto_data()))
    
    # 显示测试结果
    print("\n" + "=" * 60)
    print("📋 测试结果汇总")
    print("=" * 60)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name:<15} {status}")
    
    print("\n📝 注意事项:")
    print("- 如果某些功能失败，可能是由于 Investing.com API 变更")
    print("- 建议考虑使用 investiny 作为替代方案")
    print("- 数据获取可能需要稳定的网络连接")

if __name__ == "__main__":
    main() 
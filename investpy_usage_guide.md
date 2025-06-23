# investpy 使用指南

## 项目简介

investpy 是一个用于从 Investing.com 提取金融数据的 Python 包，可以获取：
- 39,952 只股票数据
- 82,221 只基金数据  
- 11,403 只ETF数据
- 2,029 种货币对数据
- 7,797 个指数数据
- 688 种债券数据
- 66 种商品数据
- 250 个证书数据
- 4,697 种加密货币数据

⚠️ **注意**: 目前 investpy 由于 Investing.com API 变更暂时无法正常工作，作者推荐使用 investiny 作为临时替代方案。

## 安装方法

```bash
pip install investpy
```

## 主要功能

### 1. 股票历史数据获取

```python
import investpy

# 获取苹果公司股票历史数据
df = investpy.get_stock_historical_data(stock='AAPL',
                                        country='United States',
                                        from_date='01/01/2010',
                                        to_date='01/01/2020')
print(df.head())
```

输出示例：
```
             Open   High    Low  Close     Volume Currency
Date                                                      
2010-01-04  30.49  30.64  30.34  30.57  123432176      USD
2010-01-05  30.66  30.80  30.46  30.63  150476160      USD
2010-01-06  30.63  30.75  30.11  30.14  138039728      USD
2010-01-07  30.25  30.29  29.86  30.08  119282440      USD
2010-01-08  30.04  30.29  29.87  30.28  111969192      USD
```

### 2. 搜索功能

```python
import investpy

# 搜索苹果公司股票
search_result = investpy.search_quotes(text='apple', 
                                       products=['stocks'],
                                       countries=['united states'], 
                                       n_results=1)
print(search_result)
```

返回结果：
```json
{
    "id_": 6408, 
    "name": "Apple Inc", 
    "symbol": "AAPL", 
    "country": "united states", 
    "tag": "/equities/apple-computer-inc", 
    "pair_type": "stocks", 
    "exchange": "NASDAQ"
}
```

### 3. 通过搜索结果获取数据

```python
# 获取最新数据
recent_data = search_result.retrieve_recent_data()

# 获取历史数据
historical_data = search_result.retrieve_historical_data(from_date='01/01/2019', 
                                                         to_date='01/01/2020')

# 获取基本信息
information = search_result.retrieve_information()

# 获取默认货币
default_currency = search_result.retrieve_currency()

# 获取技术指标
technical_indicators = search_result.retrieve_technical_indicators(interval='daily')
```

### 4. 加密货币数据

```python
import investpy

# 获取比特币历史数据
data = investpy.get_crypto_historical_data(crypto='bitcoin',
                                           from_date='01/01/2014',
                                           to_date='01/01/2019')

print(data.head())
```

输出示例：
```
             Open    High    Low   Close  Volume Currency
Date                                                     
2014-01-01  805.9   829.9  771.0   815.9   10757      USD
2014-01-02  815.9   886.2  810.5   856.9   12812      USD
2014-01-03  856.9   888.2  839.4   884.3    9709      USD
2014-01-04  884.3   932.2  848.3   924.7   14239      USD
2014-01-05  924.7  1029.9  911.4  1014.7   21374      USD
```

## 其他主要功能

### 基金数据
```python
# 获取基金数据
fund_data = investpy.get_fund_historical_data(fund='Fund Name',
                                              country='Country',
                                              from_date='01/01/2019',
                                              to_date='01/01/2020')
```

### ETF数据
```python
# 获取ETF数据
etf_data = investpy.get_etf_historical_data(etf='ETF Name',
                                            country='Country',
                                            from_date='01/01/2019',
                                            to_date='01/01/2020')
```

### 指数数据
```python
# 获取指数数据
index_data = investpy.get_index_historical_data(index='S&P 500',
                                                country='United States',
                                                from_date='01/01/2019',
                                                to_date='01/01/2020')
```

### 货币对数据
```python
# 获取货币对数据
currency_data = investpy.get_currency_cross_historical_data(currency_cross='EUR/USD',
                                                            from_date='01/01/2019',
                                                            to_date='01/01/2020')
```

### 商品数据
```python
# 获取商品数据
commodity_data = investpy.get_commodity_historical_data(commodity='Gold',
                                                        from_date='01/01/2019',
                                                        to_date='01/01/2020')
```

## 数据获取参数说明

- `from_date` 和 `to_date`: 日期格式为 'dd/mm/yyyy'
- `country`: 国家名称（英文）
- `interval`: 数据间隔，可选：
  - 'Daily' (默认)
  - 'Weekly'
  - 'Monthly'
- `order`: 数据排序，可选：
  - 'ascending' (升序)
  - 'descending' (降序，默认)

## 注意事项

1. **当前状态**: 由于 Investing.com API 变更，investpy 暂时无法正常工作
2. **替代方案**: 建议使用 investiny 包作为临时替代
3. **数据来源**: 所有数据来自 Investing.com
4. **使用限制**: 仅用于研究目的
5. **免责声明**: 该包与 Investing.com 无关联

## 相关项目

- **investiny**: investpy 的更新版本
- **pyrtfolio**: 股票投资组合生成工具
- **trendet**: 股票时间序列趋势检测
- **pypme**: PME (公开市场等价物) 计算工具

## 文档和支持

- 官方文档: [investpy.readthedocs.io](https://investpy.readthedocs.io/)
- GitHub仓库: [https://github.com/alvarobartt/investpy](https://github.com/alvarobartt/investpy)
- GitHub讨论: 用于Q&A和技术支持

## 作者信息

- 作者: Álvaro Bartolomé del Canto
- LinkedIn: [alvarobartt](https://linkedin.com/in/alvarobartt)
- Twitter: [@alvarobartt](https://twitter.com/alvarobartt)
- GitHub: [alvarobartt](https://github.com/alvarobartt) 
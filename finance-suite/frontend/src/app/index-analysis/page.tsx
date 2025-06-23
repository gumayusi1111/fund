'use client';

import { useEffect } from 'react';
import { useIndexAnalysis } from './hooks/useIndexAnalysis';
import IndexCodeInput from './components/IndexCodeInput';
import TimeRangeSelector from './components/TimeRangeSelector';
import SimpleChart from './components/SimpleChart';

export default function IndexAnalysisPage() {
  const {
    loading,
    error,
    indexInfo,
    historyData,
    indexCode,
    selectedTimeRange,
    hasData,
    isValidCode,
    setIndexCode,
    setTimeRange,
    searchIndex,
    clearError
  } = useIndexAnalysis();

  // 页面加载时设置默认指数
  useEffect(() => {
    setIndexCode('000300'); // 默认沪深300
  }, [setIndexCode]);

  // 处理搜索
  const handleSearch = async () => {
    if (!isValidCode) return;
    
    try {
      await searchIndex(indexCode, selectedTimeRange);
    } catch (error) {
      console.error('搜索失败:', error);
    }
  };

  // 处理时间范围变化
  const handleTimeRangeChange = async (range: string) => {
    setTimeRange(range);
    
    // 如果已经有数据，自动重新查询
    if (indexCode && hasData) {
      try {
        await searchIndex(indexCode, range);
      } catch (error) {
        console.error('更新时间范围失败:', error);
      }
    }
  };

  // 计算年初至今涨跌幅
  const getYearToDateReturn = () => {
    if (!historyData?.data || historyData.data.length === 0) return null;
    
    // 找到年初的数据
    const currentYear = new Date().getFullYear();
    const yearStartData = historyData.data.find(d => {
      const date = new Date(d.date);
      return date.getFullYear() === currentYear && date.getMonth() === 0;
    });
    
    if (yearStartData) {
      const lastData = historyData.data[historyData.data.length - 1];
      const ytdReturn = ((lastData.close_value - yearStartData.close_value) / yearStartData.close_value) * 100;
      return ytdReturn || null;
    }
    
    return null;
  };

  // 计算52周高低
  const get52WeekHighLow = () => {
    if (!historyData?.data || historyData.data.length === 0) return { high: null, low: null };
    
    const oneYearAgo = new Date();
    oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);
    
    const yearData = historyData.data.filter(d => new Date(d.date) >= oneYearAgo);
    
    if (yearData.length > 0) {
      const high = Math.max(...yearData.map(d => d.high_value));
      const low = Math.min(...yearData.map(d => d.low_value));
      return { high, low };
    }
    
    return { high: null, low: null };
  };

  // 计算振幅
  const getAmplitude = () => {
    if (!historyData?.data || historyData.data.length === 0) return null;
    const lastData = historyData.data[historyData.data.length - 1];
    return ((lastData.high_value - lastData.low_value) / lastData.low_value) * 100;
  };

  return (
    <div className="p-6 max-w-full mx-auto">
      {/* 页面标题 */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">指数分析</h1>
        <p className="text-gray-600 mt-1">查看指数历史数据和走势图</p>
      </div>

      {/* 工具栏 */}
      <div className="bg-white border border-gray-200 rounded-lg p-4 mb-6">
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex-1 min-w-64">
            <IndexCodeInput
              value={indexCode}
              onChange={setIndexCode}
              onSearch={handleSearch}
              loading={loading}
              error={error}
            />
          </div>
          
          <div className="min-w-48">
            <TimeRangeSelector
              selectedRange={selectedTimeRange}
              onChange={handleTimeRangeChange}
              disabled={loading}
            />
          </div>
          
          <button
            onClick={handleSearch}
            disabled={!isValidCode || loading}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? '查询中...' : '查询'}
          </button>
        </div>
      </div>

      {/* 错误提示 */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="w-4 h-4 text-red-500 mr-2">⚠️</div>
              <span className="text-red-800">{error}</span>
            </div>
            <button
              onClick={clearError}
              className="text-red-600 hover:text-red-800"
            >
              ✕
            </button>
          </div>
        </div>
      )}

      {/* 图表区域 - 全宽 */}
      <div className="bg-white border border-gray-200 rounded-lg mb-6 overflow-hidden">
        {historyData && historyData.data && historyData.data.length > 0 ? (
          <div className="p-6 overflow-x-auto">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">
                {historyData.name} ({historyData.code}) 价格走势
              </h2>
              <div className="text-sm text-gray-500">
                {historyData.data[0].date} - {historyData.data[historyData.data.length - 1].date}
              </div>
            </div>
            <SimpleChart
              data={historyData}
              loading={loading}
              height={450}
            />
          </div>
        ) : (
          <div className="p-12 text-center">
            {loading ? (
              <div>
                <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                <p className="text-gray-600">正在加载数据...</p>
              </div>
            ) : (
              <div>
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">📊</span>
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">暂无数据</h3>
                <p className="text-gray-500 mb-4">请输入指数代码并点击查询按钮</p>
                <button
                  onClick={handleSearch}
                  disabled={!isValidCode || loading}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
                >
                  开始查询
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* 数据展示区域 */}
      {indexInfo && historyData && historyData.data && historyData.data.length > 0 && (
        <>
          {/* 基础行情数据 */}
          <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold mb-4">基础行情数据</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {/* 最新点位 */}
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <p className="text-sm text-gray-500">最新点位</p>
                  <span className="text-xs text-yellow-600">⭐⭐⭐⭐</span>
                </div>
                <p className="text-2xl font-bold text-gray-900">
                  {indexInfo.current_value?.toFixed(2) || '--'}
                </p>
                <p className="text-xs text-gray-400">当前指数价格</p>
              </div>

              {/* 涨跌幅 */}
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <p className="text-sm text-gray-500">涨跌幅</p>
                  <span className="text-xs text-yellow-600">⭐⭐⭐⭐</span>
                </div>
                <p className={`text-2xl font-bold ${(indexInfo.change_percent ?? 0) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {(indexInfo.change_percent ?? 0) >= 0 ? '+' : ''}{indexInfo.change_percent?.toFixed(2) || 0}%
                </p>
                <p className="text-xs text-gray-400">今天赚还是亏</p>
              </div>

              {/* 涨跌额 */}
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <p className="text-sm text-gray-500">涨跌额</p>
                  <span className="text-xs text-yellow-600">⭐⭐⭐</span>
                </div>
                <p className={`text-2xl font-bold ${(indexInfo.change_value ?? 0) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {(indexInfo.change_value ?? 0) >= 0 ? '+' : ''}{indexInfo.change_value?.toFixed(2) || 0}
                </p>
                <p className="text-xs text-gray-400">涨跌了多少点</p>
              </div>

              {/* 成交量 */}
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <p className="text-sm text-gray-500">成交量</p>
                  <span className="text-xs text-yellow-600">⭐⭐</span>
                </div>
                <p className="text-xl font-bold text-gray-900">
                  {indexInfo.volume ? (indexInfo.volume / 100000000).toFixed(2) + '亿' : '--'}
                </p>
                <p className="text-xs text-gray-400">今天多少人交易</p>
              </div>

              {/* 成交额 */}
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <p className="text-sm text-gray-500">成交额</p>
                  <span className="text-xs text-yellow-600">⭐⭐⭐</span>
                </div>
                <p className="text-xl font-bold text-gray-900">
                  {indexInfo.turnover ? (indexInfo.turnover / 100000000).toFixed(2) + '亿' : '--'}
                </p>
                <p className="text-xs text-gray-400">资金活跃度</p>
              </div>

              {/* 振幅 */}
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <p className="text-sm text-gray-500">振幅</p>
                  <span className="text-xs text-yellow-600">⭐⭐</span>
                </div>
                <p className="text-xl font-bold text-gray-900">
                  {getAmplitude()?.toFixed(2) || '--'}%
                </p>
                <p className="text-xs text-gray-400">市场激烈程度</p>
              </div>

              {/* 52周高低 */}
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <p className="text-sm text-gray-500">52周高/低</p>
                  <span className="text-xs text-yellow-600">⭐⭐</span>
                </div>
                <p className="text-lg font-bold text-gray-900">
                  {get52WeekHighLow().high?.toFixed(0) || '--'} / {get52WeekHighLow().low?.toFixed(0) || '--'}
                </p>
                <p className="text-xs text-gray-400">一年内最高最低</p>
              </div>

              {/* 年初至今涨跌幅 */}
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <p className="text-sm text-gray-500">年初至今</p>
                  <span className="text-xs text-yellow-600">⭐⭐⭐</span>
                </div>
                <p className={`text-xl font-bold ${(getYearToDateReturn() ?? 0) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {(() => {
                    const ytd = getYearToDateReturn();
                    return ytd !== null ? 
                      `${ytd >= 0 ? '+' : ''}${ytd.toFixed(2)}%` : 
                      '--';
                  })()}
                </p>
                <p className="text-xs text-gray-400">今年表现如何</p>
              </div>
            </div>
          </div>

          {/* 估值数据 */}
          <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold mb-4">估值数据</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              {/* 市盈率 */}
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <p className="text-sm text-gray-500">市盈率(PE)</p>
                  <span className="text-xs text-yellow-600">⭐⭐⭐⭐</span>
                </div>
                <p className="text-xl font-bold text-gray-900">
                  {indexInfo.pe_ratio?.toFixed(2) || '--'}
                </p>
                <p className="text-xs text-gray-400">估值贵不贵</p>
              </div>

              {/* 市净率 */}
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <p className="text-sm text-gray-500">市净率(PB)</p>
                  <span className="text-xs text-yellow-600">⭐⭐⭐</span>
                </div>
                <p className="text-xl font-bold text-gray-900">
                  {indexInfo.pb_ratio?.toFixed(2) || '--'}
                </p>
                <p className="text-xs text-gray-400">资产估值参考</p>
              </div>

              {/* 股息率 */}
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <p className="text-sm text-gray-500">股息率</p>
                  <span className="text-xs text-yellow-600">⭐⭐⭐</span>
                </div>
                <p className="text-xl font-bold text-gray-900">
                  {indexInfo.dividend_yield ? indexInfo.dividend_yield.toFixed(2) + '%' : '--'}
                </p>
                <p className="text-xs text-gray-400">能不能吃利息</p>
              </div>

              {/* 估值分位数 */}
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <p className="text-sm text-gray-500">估值分位数</p>
                  <span className="text-xs text-yellow-600">⭐⭐⭐⭐</span>
                </div>
                <p className="text-xl font-bold text-gray-900">--</p>
                <p className="text-xs text-gray-400">历史估值位置</p>
              </div>
            </div>
          </div>

          {/* 统计数据 */}
          {historyData.statistics && (
            <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
              <h3 className="text-lg font-semibold mb-4">统计数据</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                {historyData.statistics.total_return !== undefined && (
                  <div>
                    <p className="text-sm text-gray-500">总收益率</p>
                    <p className={`text-xl font-bold ${historyData.statistics.total_return >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {historyData.statistics.total_return >= 0 ? '+' : ''}{historyData.statistics.total_return.toFixed(2)}%
                    </p>
                  </div>
                )}
                {historyData.statistics.volatility !== undefined && (
                  <div>
                    <p className="text-sm text-gray-500">波动率</p>
                    <p className="text-xl font-bold">{historyData.statistics.volatility.toFixed(2)}%</p>
                  </div>
                )}
                {historyData.statistics.max_value !== undefined && (
                  <div>
                    <p className="text-sm text-gray-500">最高点</p>
                    <p className="text-xl font-bold">{historyData.statistics.max_value.toFixed(2)}</p>
                  </div>
                )}
                {historyData.statistics.min_value !== undefined && (
                  <div>
                    <p className="text-sm text-gray-500">最低点</p>
                    <p className="text-xl font-bold">{historyData.statistics.min_value.toFixed(2)}</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* 最新交易数据 */}
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4">最新交易数据</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 text-sm font-medium text-gray-700">日期</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-700">开盘</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-700">最高</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-700">最低</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-700">收盘</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-700">涨跌幅</th>
                    <th className="text-right py-3 px-4 text-sm font-medium text-gray-700">成交量</th>
                  </tr>
                </thead>
                <tbody>
                  {historyData.data.slice(-10).reverse().map((point, index) => (
                    <tr key={index} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3 px-4 text-sm">{point.date}</td>
                      <td className="py-3 px-4 text-sm text-right">{point.open_value.toFixed(2)}</td>
                      <td className="py-3 px-4 text-sm text-right">{point.high_value.toFixed(2)}</td>
                      <td className="py-3 px-4 text-sm text-right">{point.low_value.toFixed(2)}</td>
                      <td className="py-3 px-4 text-sm text-right font-medium">{point.close_value.toFixed(2)}</td>
                      <td className={`py-3 px-4 text-sm text-right font-medium ${(point.change_percent ?? 0) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {(point.change_percent ?? 0) >= 0 ? '+' : ''}{(point.change_percent ?? 0).toFixed(2)}%
                      </td>
                      <td className="py-3 px-4 text-sm text-right">
                        {point.volume ? (point.volume / 100000000).toFixed(2) + '亿' : '--'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
} 
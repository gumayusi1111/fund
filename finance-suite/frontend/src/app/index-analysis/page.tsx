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

  return (
    <div className="p-6 max-w-7xl mx-auto">
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

      {/* 指数信息卡片 */}
      {indexInfo && (
        <div className="bg-white border border-gray-200 rounded-lg p-4 mb-6">
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
            <div>
              <p className="text-sm text-gray-500">指数代码</p>
              <p className="font-semibold">{indexInfo.code}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">指数名称</p>
              <p className="font-semibold">{indexInfo.name}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">所属市场</p>
              <p>{indexInfo.market}</p>
            </div>
            {indexInfo.current_value && (
              <div>
                <p className="text-sm text-gray-500">当前点位</p>
                <p className="font-semibold">{indexInfo.current_value.toFixed(2)}</p>
              </div>
            )}
            {indexInfo.change_value !== undefined && (
              <div>
                <p className="text-sm text-gray-500">涨跌点数</p>
                <p className={`font-semibold ${indexInfo.change_value >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {indexInfo.change_value >= 0 ? '+' : ''}{indexInfo.change_value.toFixed(2)}
                </p>
              </div>
            )}
            {indexInfo.change_percent !== undefined && (
              <div>
                <p className="text-sm text-gray-500">涨跌幅</p>
                <p className={`font-semibold ${indexInfo.change_percent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {indexInfo.change_percent >= 0 ? '+' : ''}{indexInfo.change_percent.toFixed(2)}%
                </p>
              </div>
            )}
          </div>
        </div>
      )}

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

      {/* 图表区域 */}
      <div className="bg-white border border-gray-200 rounded-lg">
        {historyData && historyData.data && historyData.data.length > 0 ? (
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">价格走势</h2>
              <div className="text-sm text-gray-500">
                共 {historyData.data.length} 个数据点
              </div>
            </div>
            <SimpleChart
              data={historyData}
              loading={loading}
              height={400}
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

      {/* 数据统计 */}
      {historyData && historyData.statistics && (
        <div className="mt-6 bg-white border border-gray-200 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-3">统计数据</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {historyData.statistics.total_return !== undefined && (
              <div>
                <p className="text-sm text-gray-500">总收益率</p>
                <p className={`font-semibold ${historyData.statistics.total_return >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {historyData.statistics.total_return.toFixed(2)}%
                </p>
              </div>
            )}
            {historyData.statistics.volatility !== undefined && (
              <div>
                <p className="text-sm text-gray-500">波动率</p>
                <p className="font-semibold">{historyData.statistics.volatility.toFixed(2)}%</p>
              </div>
            )}
            {historyData.statistics.max_value !== undefined && (
              <div>
                <p className="text-sm text-gray-500">最高点</p>
                <p className="font-semibold">{historyData.statistics.max_value.toFixed(2)}</p>
              </div>
            )}
            {historyData.statistics.min_value !== undefined && (
              <div>
                <p className="text-sm text-gray-500">最低点</p>
                <p className="font-semibold">{historyData.statistics.min_value.toFixed(2)}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
} 
'use client';

import { useMemo } from 'react';
import { IndexHistoryData } from '../types';
import { formatChartDate } from '../utils/dateUtils';

interface SimpleChartProps {
  data: IndexHistoryData;
  loading?: boolean;
  height?: number;
}

export default function SimpleChart({
  data,
  loading = false,
  height = 400
}: SimpleChartProps) {
  // 转换数据格式用于图表显示
  const chartData = useMemo(() => {
    if (!data?.data || data.data.length === 0) {
      return [];
    }

    return data.data.map((point) => ({
      date: formatChartDate(point.date),
      value: point.close_value,
      fullDate: point.date,
      open: point.open_value,
      high: point.high_value,
      low: point.low_value,
      close: point.close_value,
      volume: point.volume,
      changePercent: point.change_percent
    }));
  }, [data]);

  // 计算统计信息
  const statistics = useMemo(() => {
    if (chartData.length === 0) return null;

    const values = chartData.map(d => d.value);
    const minValue = Math.min(...values);
    const maxValue = Math.max(...values);
    const firstValue = values[0];
    const lastValue = values[values.length - 1];
    const totalReturn = ((lastValue - firstValue) / firstValue) * 100;

    return {
      minValue,
      maxValue,
      totalReturn,
      dataPoints: chartData.length
    };
  }, [chartData]);

  if (loading) {
    return (
      <div className="w-full flex items-center justify-center bg-gray-50 rounded-lg" style={{ height }}>
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-2" />
          <p className="text-gray-600">加载图表数据中...</p>
        </div>
      </div>
    );
  }

  if (!data || chartData.length === 0) {
    return (
      <div className="w-full flex items-center justify-center bg-gray-50 rounded-lg" style={{ height }}>
        <div className="text-center">
          <svg className="w-12 h-12 text-gray-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <p className="text-gray-600">暂无图表数据</p>
          <p className="text-sm text-gray-500 mt-1">请输入指数代码并查询</p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full">
      {/* 图表标题 */}
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900">
          {data.name} ({data.code}) 走势图
        </h3>
        <p className="text-sm text-gray-600">
          数据点数: {chartData.length} | 时间范围: {chartData[0]?.fullDate} 至 {chartData[chartData.length - 1]?.fullDate}
        </p>
      </div>

      {/* 简单的SVG图表 */}
      <div className="w-full bg-white rounded-lg border border-gray-200 p-4">
        <div className="w-full overflow-x-auto">
          <svg width="100%" height={height} className="min-w-full">
            {/* 背景网格 */}
            <defs>
              <pattern id="grid" width="50" height="40" patternUnits="userSpaceOnUse">
                <path d="M 50 0 L 0 0 0 40" fill="none" stroke="#e5e7eb" strokeWidth="1"/>
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" />
            
            {/* 绘制价格线 */}
            {statistics && (
              <g>
                {/* 计算坐标 */}
                {(() => {
                  const padding = 40;
                  const chartWidth = 800; // 固定宽度
                  const chartHeight = height - padding * 2;
                  const xStep = (chartWidth - padding * 2) / (chartData.length - 1);
                  const yScale = chartHeight / (statistics.maxValue - statistics.minValue);
                  
                  const points = chartData.map((point, index) => ({
                    x: padding + index * xStep,
                    y: padding + (statistics.maxValue - point.value) * yScale
                  }));

                  const pathD = points.reduce((path, point, index) => {
                    return path + (index === 0 ? `M ${point.x} ${point.y}` : ` L ${point.x} ${point.y}`);
                  }, '');

                  return (
                    <>
                      {/* 价格线 */}
                      <path
                        d={pathD}
                        fill="none"
                        stroke="#3B82F6"
                        strokeWidth="2"
                        className="drop-shadow-sm"
                      />
                      
                                             {/* 数据点 */}
                       {points.map((point, index) => (
                         <circle
                           key={index}
                           cx={point.x}
                           cy={point.y}
                           r="3"
                           fill="#3B82F6"
                           className="hover:r-5 transition-all duration-200 cursor-pointer"
                         >
                           <title>{`${chartData[index].fullDate}: ${chartData[index].value.toFixed(2)}`}</title>
                         </circle>
                       ))}
                      
                      {/* Y轴标签 */}
                      <text x="10" y={padding} fill="#6b7280" fontSize="12">
                        {statistics.maxValue.toFixed(0)}
                      </text>
                      <text x="10" y={height - padding} fill="#6b7280" fontSize="12">
                        {statistics.minValue.toFixed(0)}
                      </text>
                      
                      {/* X轴标签 */}
                      <text x={padding} y={height - 10} fill="#6b7280" fontSize="12">
                        {chartData[0]?.date}
                      </text>
                      <text x={chartWidth - padding} y={height - 10} fill="#6b7280" fontSize="12" textAnchor="end">
                        {chartData[chartData.length - 1]?.date}
                      </text>
                    </>
                  );
                })()}
              </g>
            )}
          </svg>
        </div>
      </div>

      {/* 统计信息 */}
      {statistics && (
        <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-gray-50 p-3 rounded-lg">
            <p className="text-xs text-gray-600">总收益率</p>
            <p className={`text-lg font-semibold ${statistics.totalReturn >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {statistics.totalReturn.toFixed(2)}%
            </p>
          </div>
          <div className="bg-gray-50 p-3 rounded-lg">
            <p className="text-xs text-gray-600">数据点数</p>
            <p className="text-lg font-semibold text-gray-900">{statistics.dataPoints}</p>
          </div>
          <div className="bg-gray-50 p-3 rounded-lg">
            <p className="text-xs text-gray-600">最高点</p>
            <p className="text-lg font-semibold text-gray-900">{statistics.maxValue.toFixed(2)}</p>
          </div>
          <div className="bg-gray-50 p-3 rounded-lg">
            <p className="text-xs text-gray-600">最低点</p>
            <p className="text-lg font-semibold text-gray-900">{statistics.minValue.toFixed(2)}</p>
          </div>
        </div>
      )}

      {/* 图表说明 */}
      <div className="mt-4 text-xs text-gray-500">
        <p>💡 提示：这是一个简化的图表组件。将鼠标悬停在数据点上可查看详细信息。</p>
      </div>
    </div>
  );
} 
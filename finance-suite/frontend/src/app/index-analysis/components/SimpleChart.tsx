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
  height = 500
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

  // 计算统计信息和图表参数
  const chartInfo = useMemo(() => {
    if (chartData.length === 0) return null;

    const values = chartData.map(d => d.value);
    const minValue = Math.min(...values);
    const maxValue = Math.max(...values);
    const firstValue = values[0];
    const lastValue = values[values.length - 1];
    const totalReturn = ((lastValue - firstValue) / firstValue) * 100;

    // 计算Y轴刻度
    const range = maxValue - minValue;
    const padding = range * 0.1;
    const yMin = minValue - padding;
    const yMax = maxValue + padding;
    
    // 生成Y轴刻度值
    const yTicks = [];
    const tickCount = 6;
    const tickStep = (yMax - yMin) / (tickCount - 1);
    for (let i = 0; i < tickCount; i++) {
      yTicks.push(yMin + tickStep * i);
    }

    return {
      minValue,
      maxValue,
      yMin,
      yMax,
      yTicks,
      totalReturn,
      dataPoints: chartData.length,
      isPositive: lastValue >= firstValue
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

  if (!chartInfo) {
    return null;
  }

  // 图表尺寸参数
  const margins = { top: 20, right: 80, bottom: 60, left: 80 };
  const chartWidth = 1000;
  const chartHeight = height - margins.top - margins.bottom;

  // 计算坐标点
  const points = chartData.map((point, index) => {
    const x = margins.left + (index / (chartData.length - 1)) * (chartWidth - margins.left - margins.right);
    const y = margins.top + ((chartInfo.yMax - point.value) / (chartInfo.yMax - chartInfo.yMin)) * chartHeight;
    return { x, y, data: point };
  });

  // 创建路径
  const linePath = points.reduce((path, point, index) => {
    return path + (index === 0 ? `M ${point.x} ${point.y}` : ` L ${point.x} ${point.y}`);
  }, '');

  // 创建渐变区域路径
  const areaPath = linePath + ` L ${points[points.length - 1].x} ${height - margins.bottom} L ${margins.left} ${height - margins.bottom} Z`;

  // 计算X轴标签 - 显示5-7个时间点
  const xLabelCount = Math.min(7, Math.max(5, Math.floor(chartData.length / 10)));
  const xLabelStep = Math.floor(chartData.length / (xLabelCount - 1));
  const xLabels = [];
  for (let i = 0; i < xLabelCount - 1; i++) {
    const index = i * xLabelStep;
    xLabels.push({ x: points[index].x, label: chartData[index].date });
  }
  // 确保最后一个标签
  xLabels.push({ 
    x: points[points.length - 1].x, 
    label: chartData[chartData.length - 1].date 
  });

  return (
    <div className="w-full">
      {/* 图表容器 */}
      <div className="w-full bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div className="w-full overflow-x-auto">
          <svg width={chartWidth} height={height} className="min-w-full">
            {/* 定义渐变 */}
            <defs>
              <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stopColor={chartInfo.isPositive ? "#10B981" : "#EF4444"} stopOpacity="0.2" />
                <stop offset="100%" stopColor={chartInfo.isPositive ? "#10B981" : "#EF4444"} stopOpacity="0.02" />
              </linearGradient>
              <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur in="SourceAlpha" stdDeviation="2"/>
                <feOffset dx="0" dy="1" result="offsetblur"/>
                <feComponentTransfer>
                  <feFuncA type="linear" slope="0.1"/>
                </feComponentTransfer>
                <feMerge>
                  <feMergeNode/>
                  <feMergeNode in="SourceGraphic"/>
                </feMerge>
              </filter>
            </defs>

            {/* 背景网格 */}
            <g>
              {/* 水平网格线 */}
              {chartInfo.yTicks.map((tick, index) => {
                const y = margins.top + ((chartInfo.yMax - tick) / (chartInfo.yMax - chartInfo.yMin)) * chartHeight;
                return (
                  <g key={index}>
                    <line
                      x1={margins.left}
                      y1={y}
                      x2={chartWidth - margins.right}
                      y2={y}
                      stroke="#E5E7EB"
                      strokeWidth="1"
                      strokeDasharray={index === 0 || index === chartInfo.yTicks.length - 1 ? "0" : "3,3"}
                    />
                    <text
                      x={margins.left - 10}
                      y={y + 5}
                      fill="#6B7280"
                      fontSize="12"
                      textAnchor="end"
                    >
                      {tick.toFixed(0)}
                    </text>
                  </g>
                );
              })}

              {/* 垂直网格线 */}
              {xLabels.map((label, index) => (
                <line
                  key={index}
                  x1={label.x}
                  y1={margins.top}
                  x2={label.x}
                  y2={height - margins.bottom}
                  stroke="#E5E7EB"
                  strokeWidth="1"
                  strokeDasharray="3,3"
                />
              ))}
            </g>

            {/* 渐变区域 */}
            <path
              d={areaPath}
              fill="url(#areaGradient)"
            />

            {/* 价格线 */}
            <path
              d={linePath}
              fill="none"
              stroke={chartInfo.isPositive ? "#10B981" : "#EF4444"}
              strokeWidth="2.5"
              filter="url(#shadow)"
            />

            {/* 数据点 */}
            {points.map((point, index) => (
              <g key={index}>
                <circle
                  cx={point.x}
                  cy={point.y}
                  r="0"
                  fill={chartInfo.isPositive ? "#10B981" : "#EF4444"}
                  className="chart-dot"
                >
                  <animate
                    attributeName="r"
                    values="0;3;0"
                    dur="0.3s"
                    begin="mouseover"
                    fill="freeze"
                  />
                </circle>
                {/* 鼠标悬停区域 */}
                <rect
                  x={point.x - 20}
                  y={margins.top}
                  width="40"
                  height={chartHeight}
                  fill="transparent"
                  className="cursor-pointer"
                >
                  <title>
                    {`日期: ${point.data.fullDate}\n`}
                    {`收盘: ${point.data.value.toFixed(2)}\n`}
                    {`开盘: ${point.data.open.toFixed(2)}\n`}
                    {`最高: ${point.data.high.toFixed(2)}\n`}
                    {`最低: ${point.data.low.toFixed(2)}\n`}
                    {`涨跌幅: ${point.data.changePercent?.toFixed(2) || 0}%`}
                  </title>
                </rect>
              </g>
            ))}

            {/* X轴标签 */}
            {xLabels.map((label, index) => (
              <text
                key={index}
                x={label.x}
                y={height - margins.bottom + 20}
                fill="#6B7280"
                fontSize="12"
                textAnchor="middle"
              >
                {label.label}
              </text>
            ))}

            {/* Y轴标题 */}
            <text
              x={20}
              y={margins.top + chartHeight / 2}
              fill="#6B7280"
              fontSize="14"
              textAnchor="middle"
              transform={`rotate(-90 20 ${margins.top + chartHeight / 2})`}
            >
              指数点位
            </text>

            {/* X轴标题 */}
            <text
              x={chartWidth / 2}
              y={height - 10}
              fill="#6B7280"
              fontSize="14"
              textAnchor="middle"
            >
              日期
            </text>

            {/* 当前值标注 */}
            <g>
              <rect
                x={chartWidth - margins.right + 10}
                y={points[points.length - 1].y - 10}
                width="60"
                height="20"
                fill={chartInfo.isPositive ? "#10B981" : "#EF4444"}
                rx="4"
              />
              <text
                x={chartWidth - margins.right + 40}
                y={points[points.length - 1].y + 3}
                fill="white"
                fontSize="12"
                textAnchor="middle"
                fontWeight="bold"
              >
                {chartData[chartData.length - 1].value.toFixed(2)}
              </text>
            </g>
          </svg>
        </div>
      </div>

      <style jsx>{`
        .chart-dot {
          transition: all 0.3s ease;
        }
        .chart-dot:hover {
          r: 5;
        }
      `}</style>
    </div>
  );
} 
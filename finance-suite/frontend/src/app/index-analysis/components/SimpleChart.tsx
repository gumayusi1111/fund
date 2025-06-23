'use client';

import { useState, useRef } from 'react';
import { IndexHistoryData } from '../types';

export interface SimpleChartProps {
  data: IndexHistoryData;
  loading: boolean;
  height?: number;
  showTooltip?: boolean;
}

interface HorizontalLine {
  id: string;
  y: number;
  value: number;
  color: string;
  label: string;
}

export default function SimpleChart({ data, loading, height = 400, showTooltip = true }: SimpleChartProps) {
  const [horizontalLines, setHorizontalLines] = useState<HorizontalLine[]>([]);
  const [isDragging, setIsDragging] = useState<string | null>(null);
  const svgRef = useRef<SVGSVGElement>(null);

  if (loading) {
    return (
      <div className="flex items-center justify-center" style={{ height }}>
        <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!data || !data.data || data.data.length === 0) {
    return (
      <div className="flex items-center justify-center" style={{ height }}>
        <p className="text-gray-500">暂无数据</p>
      </div>
    );
  }

  // 计算数据范围
  const values = data.data.map(d => d.close_value);
  const minValue = Math.min(...values);
  const maxValue = Math.max(...values);
  const valueRange = maxValue - minValue;
  const padding = valueRange * 0.1;

  // 调整后的范围
  const adjustedMin = minValue - padding;
  const adjustedMax = maxValue + padding;
  const adjustedRange = adjustedMax - adjustedMin;

  // SVG 尺寸
  const svgWidth = 1200;
  const svgHeight = height;
  const marginTop = 40;
  const marginBottom = 60;
  const marginLeft = 80;
  const marginRight = 80;
  const chartWidth = svgWidth - marginLeft - marginRight;
  const chartHeight = svgHeight - marginTop - marginBottom;

  // 计算点的位置
  const points = data.data.map((d, i) => ({
    x: (i / (data.data.length - 1)) * chartWidth + marginLeft,
    y: marginTop + chartHeight - ((d.close_value - adjustedMin) / adjustedRange) * chartHeight,
    data: d
  }));

  // 创建路径
  const path = points
    .map((p, i) => (i === 0 ? `M ${p.x},${p.y}` : `L ${p.x},${p.y}`))
    .join(' ');

  // 创建区域路径
  const areaPath = `${path} L ${points[points.length - 1].x},${marginTop + chartHeight} L ${points[0].x},${marginTop + chartHeight} Z`;

  // 选择要显示的时间标签（5-7个）
  const timeLabels = [];
  const labelCount = Math.min(7, Math.max(5, Math.floor(data.data.length / 10)));
  const step = Math.floor(data.data.length / (labelCount - 1));
  
  for (let i = 0; i < labelCount - 1; i++) {
    const index = i * step;
    timeLabels.push({
      x: points[index].x,
      label: data.data[index].date
    });
  }
  
  // 确保包含最后一个点
  timeLabels.push({
    x: points[points.length - 1].x,
    label: data.data[data.data.length - 1].date
  });

  // Y轴标签（5个）
  const yLabels = [];
  for (let i = 0; i <= 4; i++) {
    const value = adjustedMin + (adjustedRange * i) / 4;
    yLabels.push({
      y: marginTop + chartHeight - (chartHeight * i) / 4,
      label: value.toFixed(0)
    });
  }

  // 当前值（最后一个点）
  const currentPoint = points[points.length - 1];
  const currentValue = data.data[data.data.length - 1];

  // 将Y坐标转换为价格值
  const yToValue = (y: number): number => {
    const relativeY = (y - marginTop) / chartHeight;
    return adjustedMax - (relativeY * adjustedRange);
  };



  // 添加水平线
  const addHorizontalLine = (e: React.MouseEvent<SVGSVGElement>) => {
    if (e.ctrlKey || e.metaKey) { // Ctrl+Click 或 Cmd+Click 添加线
      const svg = e.currentTarget;
      const rect = svg.getBoundingClientRect();
      const y = e.clientY - rect.top;
      
      if (y >= marginTop && y <= marginTop + chartHeight) {
        const value = yToValue(y);
        const newLine: HorizontalLine = {
          id: Date.now().toString(),
          y: y,
          value: value,
          color: '#ef4444',
          label: `参考线 ${value.toFixed(2)}`
        };
        setHorizontalLines(prev => [...prev, newLine]);
      }
    }
  };

  // 开始拖拽
  const startDrag = (lineId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setIsDragging(lineId);
  };

  // 拖拽过程中
  const handleDrag = (e: React.MouseEvent<SVGSVGElement>) => {
    if (isDragging) {
      const svg = e.currentTarget;
      const rect = svg.getBoundingClientRect();
      const y = e.clientY - rect.top;
      
      if (y >= marginTop && y <= marginTop + chartHeight) {
        const value = yToValue(y);
        setHorizontalLines(prev => 
          prev.map(line => 
            line.id === isDragging 
              ? { ...line, y: y, value: value, label: `参考线 ${value.toFixed(2)}` }
              : line
          )
        );
      }
    }
  };

  // 结束拖拽
  const endDrag = () => {
    setIsDragging(null);
  };

  // 删除水平线
  const removeHorizontalLine = (lineId: string) => {
    setHorizontalLines(prev => prev.filter(line => line.id !== lineId));
  };

  // 处理鼠标事件
  const handleMouseMove = (e: React.MouseEvent<SVGSVGElement>) => {
    if (isDragging) {
      handleDrag(e);
      return;
    }

    if (!showTooltip) return;
    
    const svg = e.currentTarget;
    const rect = svg.getBoundingClientRect();
    
    // 计算鼠标在SVG坐标系中的位置
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;
    
    // 考虑SVG的viewBox缩放比例
    const scaleX = svgWidth / rect.width;
    const scaleY = svgHeight / rect.height;
    
    const svgX = mouseX * scaleX;
    const svgY = mouseY * scaleY;
    
    // 只在图表区域内显示tooltip
    if (svgX < marginLeft || svgX > marginLeft + chartWidth || 
        svgY < marginTop || svgY > marginTop + chartHeight) {
      // 隐藏tooltip
      const tooltip = svg.querySelector('.chart-tooltip') as SVGGElement;
      const hoverCircle = svg.querySelector('.hover-circle') as SVGCircleElement;
      const hoverLine = svg.querySelector('.hover-line') as SVGLineElement;
      
      if (tooltip) tooltip.style.display = 'none';
      if (hoverCircle) hoverCircle.style.display = 'none';
      if (hoverLine) hoverLine.style.display = 'none';
      return;
    }
    
    // 找到最近的数据点 - 只考虑X轴距离
    let closestPoint = points[0];
    let closestDistance = Math.abs(points[0].x - svgX);
    
    for (const point of points) {
      const distance = Math.abs(point.x - svgX);
      if (distance < closestDistance) {
        closestDistance = distance;
        closestPoint = point;
      }
    }
    
    // 显示tooltip
    const tooltip = svg.querySelector('.chart-tooltip') as SVGGElement;
    const tooltipBg = tooltip?.querySelector('rect');
    const tooltipText = tooltip?.querySelector('text');
    const hoverCircle = svg.querySelector('.hover-circle') as SVGCircleElement;
    const hoverLine = svg.querySelector('.hover-line') as SVGLineElement;
    
    if (tooltip && tooltipBg && tooltipText && hoverCircle && hoverLine && closestDistance < 20) {
      // 显示悬停元素
      hoverCircle.style.display = 'block';
      hoverLine.style.display = 'block';
      tooltip.style.display = 'block';
      
      // 设置悬停元素位置
      hoverCircle.setAttribute('cx', closestPoint.x.toString());
      hoverCircle.setAttribute('cy', closestPoint.y.toString());
      hoverLine.setAttribute('x1', closestPoint.x.toString());
      hoverLine.setAttribute('x2', closestPoint.x.toString());
      hoverLine.setAttribute('y1', (marginTop).toString());
      hoverLine.setAttribute('y2', (marginTop + chartHeight).toString());
      
      // 设置tooltip内容
      const lines = [
        `日期: ${closestPoint.data.date}`,
        `收盘: ${closestPoint.data.close_value.toFixed(2)}`,
        `开盘: ${closestPoint.data.open_value.toFixed(2)}`,
        `最高: ${closestPoint.data.high_value.toFixed(2)}`,
        `最低: ${closestPoint.data.low_value.toFixed(2)}`,
        `涨幅: ${(closestPoint.data.change_percent ?? 0) >= 0 ? '+' : ''}${(closestPoint.data.change_percent ?? 0).toFixed(2)}%`,
        `成交量: ${closestPoint.data.volume ? (closestPoint.data.volume / 100000000).toFixed(2) + '亿' : '--'}`
      ];
      
      // 清空现有内容
      while (tooltipText.firstChild) {
        tooltipText.removeChild(tooltipText.firstChild);
      }
      
      // 添加新的文本行
      lines.forEach((line, i) => {
        const tspan = document.createElementNS('http://www.w3.org/2000/svg', 'tspan');
        tspan.textContent = line;
        tspan.setAttribute('x', '10');
        tspan.setAttribute('y', (20 + i * 18).toString());
        if (i === 0) {
          tspan.style.fontWeight = 'bold';
        }
        if (i === 5 && closestPoint.data.change_percent !== null && closestPoint.data.change_percent !== undefined) {
          tspan.style.fill = closestPoint.data.change_percent >= 0 ? '#10b981' : '#ef4444';
        }
        tooltipText.appendChild(tspan);
      });
      
      // 设置tooltip背景大小
      tooltipBg.setAttribute('width', '180');
      tooltipBg.setAttribute('height', (lines.length * 18 + 10).toString());
      
      // 计算tooltip位置
      let tooltipX = closestPoint.x + 10;
      let tooltipY = closestPoint.y - 60;
      
      // 调整位置避免超出边界
      if (tooltipX + 180 > svgWidth - marginRight) {
        tooltipX = closestPoint.x - 190;
      }
      if (tooltipY < marginTop) {
        tooltipY = closestPoint.y + 10;
      }
      
      tooltip.setAttribute('transform', `translate(${tooltipX}, ${tooltipY})`);
    }
  };
  
  const handleMouseLeave = (e: React.MouseEvent<SVGSVGElement>) => {
    if (isDragging) return;
    
    if (!showTooltip) return;
    
    const svg = e.currentTarget;
    const tooltip = svg.querySelector('.chart-tooltip') as SVGGElement;
    const hoverCircle = svg.querySelector('.hover-circle') as SVGCircleElement;
    const hoverLine = svg.querySelector('.hover-line') as SVGLineElement;
    
    if (tooltip) tooltip.style.display = 'none';
    if (hoverCircle) hoverCircle.style.display = 'none';
    if (hoverLine) hoverLine.style.display = 'none';
  };

  return (
    <div className="w-full" style={{ height }}>
      {/* 操作提示 */}
      <div className="mb-2 text-xs text-gray-500 flex items-center gap-4">
        <span>💡 按住 Ctrl/Cmd + 点击图表添加参考线</span>
        <span>拖拽参考线可移动位置</span>
        <span>双击参考线删除</span>
      </div>
      
      <svg 
        ref={svgRef}
        viewBox={`0 0 ${svgWidth} ${svgHeight}`} 
        className="w-full h-full cursor-crosshair"
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        onMouseUp={endDrag}
        onClick={addHorizontalLine}
      >
        {/* 定义渐变 */}
        <defs>
          <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.3" />
            <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.05" />
          </linearGradient>
          <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur in="SourceAlpha" stdDeviation="3"/>
            <feOffset dx="0" dy="2" result="offsetblur"/>
            <feFlood floodColor="#000000" floodOpacity="0.1"/>
            <feComposite in2="offsetblur" operator="in"/>
            <feMerge>
              <feMergeNode/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>

        {/* 背景 */}
        <rect width={svgWidth} height={svgHeight} fill="white" />

        {/* Y轴网格线和标签 */}
        {yLabels.map((label, i) => (
          <g key={i}>
            <line
              x1={marginLeft}
              y1={label.y}
              x2={marginLeft + chartWidth}
              y2={label.y}
              stroke="#e5e7eb"
              strokeWidth="1"
              strokeDasharray={i === 0 ? "0" : "3 3"}
            />
            <text
              x={marginLeft - 10}
              y={label.y}
              textAnchor="end"
              alignmentBaseline="middle"
              className="text-sm fill-gray-600"
            >
              {label.label}
            </text>
          </g>
        ))}

        {/* X轴基准线 */}
        <line
          x1={marginLeft}
          y1={marginTop + chartHeight}
          x2={marginLeft + chartWidth}
          y2={marginTop + chartHeight}
          stroke="#e5e7eb"
          strokeWidth="2"
        />

        {/* X轴时间标签 */}
        {timeLabels.map((label, i) => (
          <text
            key={i}
            x={label.x}
            y={marginTop + chartHeight + 20}
            textAnchor="middle"
            className="text-sm fill-gray-600"
          >
            {label.label}
          </text>
        ))}

        {/* 区域填充 */}
        <path
          d={areaPath}
          fill="url(#areaGradient)"
          opacity="0.8"
        />

        {/* 价格线 */}
        <path
          d={path}
          fill="none"
          stroke="#3b82f6"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
          filter="url(#shadow)"
        />

        {/* 水平参考线 */}
        {horizontalLines.map((line) => (
          <g key={line.id}>
            {/* 参考线 */}
            <line
              x1={marginLeft}
              y1={line.y}
              x2={marginLeft + chartWidth}
              y2={line.y}
              stroke={line.color}
              strokeWidth="2"
              strokeDasharray="5 5"
              className="cursor-move"
              onMouseDown={(e) => startDrag(line.id, e)}
              onDoubleClick={() => removeHorizontalLine(line.id)}
            />
            
            {/* 拖拽手柄 */}
            <circle
              cx={marginLeft + chartWidth - 20}
              cy={line.y}
              r="6"
              fill={line.color}
              stroke="white"
              strokeWidth="2"
              className="cursor-move"
              onMouseDown={(e) => startDrag(line.id, e)}
              onDoubleClick={() => removeHorizontalLine(line.id)}
            />
            
            {/* 价格标签 */}
            <rect
              x={marginLeft + chartWidth + 5}
              y={line.y - 10}
              width="80"
              height="20"
              rx="3"
              fill={line.color}
              opacity="0.9"
            />
            <text
              x={marginLeft + chartWidth + 45}
              y={line.y + 4}
              textAnchor="middle"
              className="text-xs font-bold fill-white"
            >
              {line.value.toFixed(2)}
            </text>
          </g>
        ))}

        {/* 数据点 */}
        {points.map((point, i) => (
          <circle
            key={i}
            cx={point.x}
            cy={point.y}
            r="4"
            fill="white"
            stroke="#3b82f6"
            strokeWidth="2"
            className="opacity-0 hover:opacity-100 transition-opacity"
          />
        ))}

        {/* 当前值标注 */}
        <g transform={`translate(${currentPoint.x}, ${currentPoint.y})`}>
          <circle r="6" fill="#3b82f6" />
          <circle r="4" fill="white" />
          
          {/* 价格标签背景 */}
          <rect
            x="10"
            y="-15"
            width="100"
            height="30"
            rx="15"
            fill="#3b82f6"
            filter="url(#shadow)"
          />
          
          {/* 价格标签文字 */}
          <text
            x="60"
            y="5"
            textAnchor="middle"
            className="text-sm font-bold fill-white"
          >
            {currentValue.close_value.toFixed(2)}
          </text>
        </g>

        {/* 悬停线 */}
        <line
          className="hover-line"
          stroke="#94a3b8"
          strokeWidth="1"
          strokeDasharray="3 3"
          style={{ display: 'none' }}
        />

        {/* 悬停圆点 */}
        <circle
          className="hover-circle"
          r="5"
          fill="#3b82f6"
          stroke="white"
          strokeWidth="2"
          style={{ display: 'none' }}
        />

        {/* Tooltip */}
        <g className="chart-tooltip" style={{ display: 'none' }}>
          <rect
            rx="4"
            fill="rgba(0, 0, 0, 0.9)"
            stroke="none"
          />
          <text fill="white" fontSize="14">
          </text>
        </g>
      </svg>
    </div>
  );
} 
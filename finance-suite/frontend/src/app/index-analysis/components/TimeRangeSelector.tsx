'use client';

import { TIME_RANGES, TimeRange } from '../types';

interface TimeRangeSelectorProps {
  selectedRange: string;
  onChange: (range: string) => void;
  disabled?: boolean;
}

export default function TimeRangeSelector({
  selectedRange,
  onChange,
  disabled = false
}: TimeRangeSelectorProps) {
  const handleRangeClick = (range: TimeRange) => {
    if (!disabled) {
      onChange(range.value);
    }
  };

  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-700 mb-3">
        时间范围
      </label>
      
      <div className="grid grid-cols-3 md:grid-cols-6 gap-2">
        {TIME_RANGES.map((range) => (
          <button
            key={range.value}
            onClick={() => handleRangeClick(range)}
            disabled={disabled}
            className={`
              px-4 py-2 text-sm font-medium rounded-lg border transition-all duration-200
              ${selectedRange === range.value 
                ? 'bg-blue-600 text-white border-blue-600 shadow-md' 
                : 'bg-white text-gray-700 border-gray-300 hover:bg-blue-50 hover:border-blue-300'
              }
              ${disabled 
                ? 'opacity-50 cursor-not-allowed' 
                : 'cursor-pointer'
              }
              focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
            `}
          >
            {range.label}
          </button>
        ))}
      </div>

      {/* 当前选择的时间范围信息 */}
      <div className="mt-3 text-xs text-gray-500">
        {selectedRange && (
          <div className="flex items-center">
            <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            已选择：{TIME_RANGES.find(r => r.value === selectedRange)?.label || '未知'}
          </div>
        )}
      </div>

      {/* 自定义时间范围提示 */}
      <div className="mt-2 p-3 bg-blue-50 rounded-lg">
        <p className="text-xs text-blue-700">
          💡 提示：选择不同的时间范围来查看指数在不同时期的表现趋势
        </p>
      </div>
    </div>
  );
} 
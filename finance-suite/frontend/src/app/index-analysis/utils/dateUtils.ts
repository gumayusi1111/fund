// 日期处理工具函数

import { format, subMonths, subDays, startOfDay, endOfDay } from 'date-fns';

/**
 * 根据时间范围字符串计算开始和结束日期
 */
export function formatDateRange(timeRange: string): { startDate: string; endDate: string } {
  const now = new Date();
  const endDate = format(endOfDay(now), 'yyyy-MM-dd');
  let startDate: string;

  switch (timeRange) {
    case '1m':
      startDate = format(startOfDay(subMonths(now, 1)), 'yyyy-MM-dd');
      break;
    case '3m':
      startDate = format(startOfDay(subMonths(now, 3)), 'yyyy-MM-dd');
      break;
    case '6m':
      startDate = format(startOfDay(subMonths(now, 6)), 'yyyy-MM-dd');
      break;
    case '1y':
      startDate = format(startOfDay(subMonths(now, 12)), 'yyyy-MM-dd');
      break;
    case '2y':
      startDate = format(startOfDay(subMonths(now, 24)), 'yyyy-MM-dd');
      break;
    case '3y':
      startDate = format(startOfDay(subMonths(now, 36)), 'yyyy-MM-dd');
      break;
    case '7d':
      startDate = format(startOfDay(subDays(now, 7)), 'yyyy-MM-dd');
      break;
    case '30d':
      startDate = format(startOfDay(subDays(now, 30)), 'yyyy-MM-dd');
      break;
    default:
      // 默认3个月
      startDate = format(startOfDay(subMonths(now, 3)), 'yyyy-MM-dd');
  }

  return { startDate, endDate };
}

/**
 * 格式化日期用于显示
 */
export function formatDisplayDate(dateString: string): string {
  try {
    const date = new Date(dateString);
    return format(date, 'yyyy年MM月dd日');
  } catch {
    return dateString;
  }
}

/**
 * 格式化日期用于图表显示
 */
export function formatChartDate(dateString: string): string {
  try {
    const date = new Date(dateString);
    return format(date, 'MM/dd');
  } catch {
    return dateString;
  }
}

/**
 * 验证日期字符串格式
 */
export function isValidDate(dateString: string): boolean {
  try {
    const date = new Date(dateString);
    return date instanceof Date && !isNaN(date.getTime());
  } catch {
    return false;
  }
}

/**
 * 计算两个日期之间的天数差
 */
export function getDaysDifference(startDate: string, endDate: string): number {
  try {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const diffTime = Math.abs(end.getTime() - start.getTime());
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  } catch {
    return 0;
  }
}

/**
 * 根据时间范围获取合适的数据点间隔
 */
export function getDataPointInterval(timeRange: string): number {
  switch (timeRange) {
    case '7d':
    case '1m':
      return 1; // 每天
    case '3m':
      return 3; // 每3天
    case '6m':
      return 7; // 每周
    case '1y':
      return 14; // 每两周
    case '2y':
    case '3y':
      return 30; // 每月
    default:
      return 1;
  }
} 
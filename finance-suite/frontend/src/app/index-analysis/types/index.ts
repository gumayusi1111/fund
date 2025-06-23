// 指数分析相关类型定义

export interface IndexInfo {
  code: string;
  name: string;
  market: string;
  category: string;
  index_type?: string;
  base_date?: string;
  base_value?: number;
  current_value: number | null;
  change_value: number | null;
  change_percent: number | null;
  volume: number | null;           // 成交量
  turnover: number | null;         // 成交额
  amplitude?: number | null;       // 振幅
  pe_ratio?: number | null;        // 市盈率
  pb_ratio?: number | null;        // 市净率
  dividend_yield?: number | null;  // 股息率
  valuation_percentile?: number | null; // 估值分位数
  constituent_count?: number;
  last_update?: string;
}

export interface IndexDataPoint {
  date: string;
  open_value: number;
  high_value: number;
  low_value: number;
  close_value: number;
  volume?: number;
  turnover?: number;
  change_value?: number;
  change_percent?: number;
}

export interface IndexHistoryPoint {
  date: string;
  open_value: number;
  high_value: number;
  low_value: number;
  close_value: number;
  volume: number | null;
  turnover: number | null;
  change_value?: number | null;
  change_percent?: number | null;
}

export interface IndexStatistics {
  total_return?: number;
  volatility?: number;
  max_value?: number;
  min_value?: number;
  avg_volume?: number;
}

export interface IndexHistoryData {
  code: string;
  name: string;
  data: IndexHistoryPoint[];
  statistics?: IndexStatistics;
}

export interface TimeRange {
  label: string;
  value: string;
  months: number;
}

export interface IndexQueryParams {
  indexCode: string;
  timeRange: string;
  startDate?: string;
  endDate?: string;
}

export interface ChartData {
  date: string;
  value: number;
  change?: number;
  fullDate?: string;
  open?: number;
  high?: number;
  low?: number;
  close?: number;
  volume?: number;
  changePercent?: number;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
}

export interface IndexAnalysisState {
  loading: boolean;
  error: string | null;
  indexInfo: IndexInfo | null;
  historyData: IndexHistoryData | null;
  selectedTimeRange: string;
  indexCode: string;
}

// 常量定义
export const TIME_RANGES: TimeRange[] = [
  { label: '1个月', value: '1m', months: 1 },
  { label: '3个月', value: '3m', months: 3 },
  { label: '6个月', value: '6m', months: 6 },
  { label: '1年', value: '1y', months: 12 },
  { label: '2年', value: '2y', months: 24 },
  { label: '3年', value: '3y', months: 36 },
];

export const DEFAULT_INDEX_CODES = [
  { code: '000300', name: '沪深300' },
  { code: '000905', name: '中证500' },
  { code: '000001', name: '上证指数' },
  { code: '399001', name: '深证成指' },
  { code: '399006', name: '创业板指' },
];

// 错误类型
export class IndexAnalysisError extends Error {
  constructor(message: string, public code?: string) {
    super(message);
    this.name = 'IndexAnalysisError';
  }
} 
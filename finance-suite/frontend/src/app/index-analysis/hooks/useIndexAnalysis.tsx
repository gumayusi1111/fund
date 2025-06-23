'use client';

import { useState, useCallback } from 'react';
import { IndexAnalysisState, IndexQueryParams } from '../types';
import indexAPI from '../services/indexAPI';

const initialState: IndexAnalysisState = {
  loading: false,
  error: null,
  indexInfo: null,
  historyData: null,
  selectedTimeRange: '3m',
  indexCode: ''
};

export function useIndexAnalysis() {
  const [state, setState] = useState<IndexAnalysisState>(initialState);

  // 设置指数代码
  const setIndexCode = useCallback((code: string) => {
    setState(prev => ({ ...prev, indexCode: code, error: null }));
  }, []);

  // 设置时间范围
  const setTimeRange = useCallback((range: string) => {
    setState(prev => ({ ...prev, selectedTimeRange: range }));
  }, []);

  // 清除错误
  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  // 重置状态
  const reset = useCallback(() => {
    setState(initialState);
  }, []);

  // 获取指数信息
  const fetchIndexInfo = useCallback(async (indexCode: string) => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      
      const indexInfo = await indexAPI.getIndexInfo(indexCode);
      
      setState(prev => ({ 
        ...prev, 
        indexInfo,
        loading: false 
      }));
      
      return indexInfo;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : '获取指数信息失败';
      setState(prev => ({ 
        ...prev, 
        error: errorMessage,
        loading: false,
        indexInfo: null 
      }));
      throw error;
    }
  }, []);

  // 获取历史数据
  const fetchHistoryData = useCallback(async (params: IndexQueryParams) => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      
      const historyData = await indexAPI.getIndexHistory(params);
      
      setState(prev => ({ 
        ...prev, 
        historyData,
        loading: false 
      }));
      
      return historyData;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : '获取历史数据失败';
      setState(prev => ({ 
        ...prev, 
        error: errorMessage,
        loading: false,
        historyData: null 
      }));
      throw error;
    }
  }, []);

  // 搜索指数
  const searchIndex = useCallback(async (indexCode: string, timeRange: string) => {
    if (!indexCode.trim()) {
      setState(prev => ({ ...prev, error: '请输入指数代码' }));
      return;
    }

    try {
      setState(prev => ({ ...prev, loading: true, error: null }));

      // 并行获取指数信息和历史数据
      const [indexInfo, historyData] = await Promise.all([
        indexAPI.getIndexInfo(indexCode),
        indexAPI.getIndexHistory({ indexCode, timeRange })
      ]);

      setState(prev => ({ 
        ...prev, 
        indexInfo,
        historyData,
        indexCode,
        selectedTimeRange: timeRange,
        loading: false,
        error: null
      }));

      return { indexInfo, historyData };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : '查询失败';
      setState(prev => ({ 
        ...prev, 
        error: errorMessage,
        loading: false 
      }));
      throw error;
    }
  }, []);

  // 验证指数代码
  const validateIndex = useCallback(async (indexCode: string): Promise<boolean> => {
    try {
      return await indexAPI.validateIndexCode(indexCode);
    } catch {
      return false;
    }
  }, []);

  return {
    // 状态
    ...state,
    
    // 操作
    setIndexCode,
    setTimeRange,
    clearError,
    reset,
    fetchIndexInfo,
    fetchHistoryData,
    searchIndex,
    validateIndex,
    
    // 计算属性
    hasData: Boolean(state.indexInfo && state.historyData),
    isValidCode: Boolean(state.indexCode.trim())
  };
} 
// 指数分析API服务

import { 
  IndexInfo, 
  IndexHistoryData, 
  ApiResponse, 
  IndexQueryParams,
  IndexAnalysisError 
} from '../types';
import { formatDateRange } from '../utils/dateUtils';

class IndexAPIService {
  private baseURL: string;

  constructor() {
    this.baseURL = process.env.NEXT_PUBLIC_API_URL || '/api';
  }

  /**
   * 获取指数基本信息
   */
  async getIndexInfo(indexCode: string): Promise<IndexInfo> {
    try {
      const response = await fetch(`${this.baseURL}/v1/indices/${indexCode}/info`);
      
      if (!response.ok) {
        throw new IndexAnalysisError(
          `获取指数信息失败: ${response.statusText}`,
          response.status.toString()
        );
      }

      const result: ApiResponse<IndexInfo> = await response.json();
      
      if (!result.success) {
        throw new IndexAnalysisError(result.message);
      }

      return result.data;
    } catch (error) {
      if (error instanceof IndexAnalysisError) {
        throw error;
      }
      throw new IndexAnalysisError('网络错误，请检查连接后重试');
    }
  }

  /**
   * 获取指数历史数据
   */
  async getIndexHistory(params: IndexQueryParams): Promise<IndexHistoryData> {
    try {
      const { startDate, endDate } = formatDateRange(params.timeRange);
      
      const queryParams = new URLSearchParams({
        start_date: params.startDate || startDate,
        end_date: params.endDate || endDate,
      });

      const response = await fetch(
        `${this.baseURL}/v1/indices/${params.indexCode}/history?${queryParams}`
      );

      if (!response.ok) {
        throw new IndexAnalysisError(
          `获取历史数据失败: ${response.statusText}`,
          response.status.toString()
        );
      }

      const result: ApiResponse<IndexHistoryData> = await response.json();
      
      if (!result.success) {
        throw new IndexAnalysisError(result.message);
      }

      return result.data;
    } catch (error) {
      if (error instanceof IndexAnalysisError) {
        throw error;
      }
      throw new IndexAnalysisError('获取历史数据失败，请重试');
    }
  }

  /**
   * 获取指数列表
   */
  async getIndexList(): Promise<Array<{ code: string; name: string }>> {
    try {
      const response = await fetch(`${this.baseURL}/v1/indices/list?size=50`);
      
      if (!response.ok) {
        throw new IndexAnalysisError(
          `获取指数列表失败: ${response.statusText}`,
          response.status.toString()
        );
      }

      const result: ApiResponse<Array<{ code: string; name: string }>> = 
        await response.json();
      
      if (!result.success) {
        throw new IndexAnalysisError(result.message);
      }

      return result.data || [];
    } catch (error) {
      if (error instanceof IndexAnalysisError) {
        throw error;
      }
      throw new IndexAnalysisError('获取指数列表失败');
    }
  }

  /**
   * 搜索指数
   */
  async searchIndices(keyword: string): Promise<Array<{ code: string; name: string }>> {
    try {
      if (!keyword.trim()) {
        return [];
      }

      const queryParams = new URLSearchParams({
        keyword: keyword.trim(),
        size: '10'
      });

      const response = await fetch(`${this.baseURL}/v1/indices/search?${queryParams}`);
      
      if (!response.ok) {
        throw new IndexAnalysisError(
          `搜索指数失败: ${response.statusText}`,
          response.status.toString()
        );
      }

      const result: ApiResponse<Array<{ code: string; name: string }>> = 
        await response.json();
      
      if (!result.success) {
        throw new IndexAnalysisError(result.message);
      }

      return result.data || [];
    } catch (error) {
      if (error instanceof IndexAnalysisError) {
        throw error;
      }
      throw new IndexAnalysisError('搜索指数失败');
    }
  }

  /**
   * 验证指数代码是否有效
   */
  async validateIndexCode(indexCode: string): Promise<boolean> {
    try {
      await this.getIndexInfo(indexCode);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * 批量获取指数信息
   */
  async getMultipleIndicesInfo(indexCodes: string[]): Promise<IndexInfo[]> {
    try {
      const promises = indexCodes.map(code => this.getIndexInfo(code));
      const results = await Promise.allSettled(promises);
      
      return results
        .filter((result): result is PromiseFulfilledResult<IndexInfo> => 
          result.status === 'fulfilled'
        )
        .map(result => result.value);
    } catch {
      throw new IndexAnalysisError('批量获取指数信息失败');
    }
  }
}

// 创建单例实例
const indexAPI = new IndexAPIService();

export default indexAPI;
export { IndexAPIService }; 
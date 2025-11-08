/**
 * API service for making HTTP requests
 */

import type { ApiResponse, HelloResponse, HealthResponse, StatusResponse } from '@/types';

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = '') {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });

      const data = await response.json();

      return {
        data,
        status: response.status,
      };
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      return {
        error: error instanceof Error ? error.message : 'Unknown error',
        status: 500,
      };
    }
  }

  async getHello(): Promise<ApiResponse<HelloResponse>> {
    return this.request<HelloResponse>('/api/hello');
  }

  async getHealth(): Promise<ApiResponse<HealthResponse>> {
    return this.request<HealthResponse>('/health');
  }

  async getStatus(): Promise<ApiResponse<StatusResponse>> {
    return this.request<StatusResponse>('/api/status');
  }
}

export const apiService = new ApiService();
export default apiService;

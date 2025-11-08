/**
 * API response types
 */

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  message?: string;
  status: number;
}

export interface HelloResponse {
  message: string;
  author: string;
  version: string;
  timestamp: string;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  service: string;
}

export interface StatusResponse {
  status: string;
  environment: string;
  debug: boolean;
  timestamp: string;
}

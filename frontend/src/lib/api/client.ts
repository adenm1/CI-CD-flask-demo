import { browser } from '$app/environment';
import { mockRequest } from './mock';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const USE_MOCK_API = import.meta.env.VITE_USE_MOCK_API === 'true';

export type RequestOptions = {
  method?: string;
  data?: unknown;
  token?: string | null;
  headers?: Record<string, string>;
};

function getStoredToken(): string | null {
  if (!browser) return null;
  return localStorage.getItem('ci_dashboard_token');
}

function withBase(path: string) {
  if (path.startsWith('http')) return path;
  if (!path.startsWith('/')) return `${API_BASE_URL}/${path}`;
  return `${API_BASE_URL}${path}`;
}

export async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const token = options.token ?? getStoredToken();
  if (USE_MOCK_API) {
    return mockRequest<T>(path, { ...options, token });
  }

  const headers = new Headers({
    'Content-Type': 'application/json',
    ...options.headers
  });

  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const response = await fetch(withBase(path), {
    method: options.method || 'GET',
    headers,
    body: options.data ? JSON.stringify(options.data) : undefined
  });

  if (!response.ok) {
    const errorPayload = await response.json().catch(() => ({}));
    const message = errorPayload.message || errorPayload.error || response.statusText;
    throw new Error(message || 'Request failed');
  }

  if (response.status === 204) {
    return {} as T;
  }

  return response.json() as Promise<T>;
}

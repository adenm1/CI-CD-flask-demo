import { request } from './client';
import type { AdminProfile } from '$lib/stores/auth';

export type AuthResponse = {
  token: string;
  admin: AdminProfile;
};

export type LoginPayload = {
  username: string;
  password: string;
  totpCode?: string;
};

export type RegisterPayload = LoginPayload & {
  inviteCode?: string;
  reason?: string;
};

const USE_MOCK_API = import.meta.env.VITE_USE_MOCK_API === 'true';

export function login(payload: LoginPayload) {
  return request<AuthResponse>('/api/auth/login', {
    method: 'POST',
    data: {
      username: payload.username,
      password: payload.password,
      totp_code: payload.totpCode
    }
  });
}

export async function register(payload: RegisterPayload) {
  return request<AuthResponse>('/api/auth/register', {
    method: 'POST',
    data: payload
  });
}

export function requestAccess(payload: RegisterPayload) {
  return request<{ message: string; request: { id: number } }>('/api/auth/register/request', {
    method: 'POST',
    data: payload
  });
}

import { request } from './client';
import type { AdminProfile } from '$lib/stores/auth';

export type AuthResponse = {
  token: string;
  admin: AdminProfile;
};

export type LoginPayload = {
  username: string;
  password: string;
};

export type RegisterPayload = LoginPayload & {
  inviteCode?: string;
};

const REGISTRATION_ENABLED = import.meta.env.VITE_ENABLE_REGISTER === 'true';
const USE_MOCK_API = import.meta.env.VITE_USE_MOCK_API === 'true';

export function login(payload: LoginPayload) {
  return request<AuthResponse>('/api/auth/login', {
    method: 'POST',
    data: payload
  });
}

export async function register(payload: RegisterPayload) {
  return request<AuthResponse>('/api/auth/register', {
    method: 'POST',
    data: payload
  });
}

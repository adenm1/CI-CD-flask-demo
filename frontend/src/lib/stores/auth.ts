import { browser } from '$app/environment';
import { writable, derived } from 'svelte/store';

export type AdminProfile = {
  id: number;
  username: string;
  role?: string;
};

export type AuthState = {
  token: string | null;
  admin: AdminProfile | null;
  loading: boolean;
  error: string | null;
};

const STORAGE_TOKEN_KEY = 'ci_dashboard_token';
const STORAGE_ADMIN_KEY = 'ci_dashboard_admin';

function deserializeAdmin(value: string | null): AdminProfile | null {
  if (!value) return null;
  try {
    return JSON.parse(value) as AdminProfile;
  } catch {
    return null;
  }
}

function createAuthStore() {
  const { subscribe, update, set } = writable<AuthState>({
    token: null,
    admin: null,
    loading: false,
    error: null
  });

  return {
    subscribe,
    initialize() {
      if (!browser) return;
      const token = localStorage.getItem(STORAGE_TOKEN_KEY);
      const admin = deserializeAdmin(localStorage.getItem(STORAGE_ADMIN_KEY));
      set({ token, admin, loading: false, error: null });
    },
    setLoading(loading: boolean) {
      update((state) => ({ ...state, loading }));
    },
    setError(error: string | null) {
      update((state) => ({ ...state, error }));
    },
    login(token: string, admin: AdminProfile) {
      if (browser) {
        localStorage.setItem(STORAGE_TOKEN_KEY, token);
        localStorage.setItem(STORAGE_ADMIN_KEY, JSON.stringify(admin));
      }
      set({ token, admin, loading: false, error: null });
    },
    logout() {
      if (browser) {
        localStorage.removeItem(STORAGE_TOKEN_KEY);
        localStorage.removeItem(STORAGE_ADMIN_KEY);
      }
      set({ token: null, admin: null, loading: false, error: null });
    }
  };
}

export const authStore = createAuthStore();
export const isAuthenticatedStore = derived(authStore, ($auth) => Boolean($auth.token));

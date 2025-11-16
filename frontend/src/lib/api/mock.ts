import type { RequestOptions } from './client';

const mockAdmin = {
  id: 1,
  username: 'demo-admin',
  role: 'owner'
};

let sessions = [
  {
    id: 101,
    title: 'Production Deploy',
    description: 'Blue/green deploy to prod',
    status: 'completed',
    difficulty: 'advanced',
    started_at: new Date(Date.now() - 3600 * 1000 * 5).toISOString(),
    completed_at: new Date(Date.now() - 3600 * 1000 * 4.5).toISOString(),
    created_at: new Date(Date.now() - 3600 * 1000 * 7).toISOString(),
    updated_at: new Date(Date.now() - 3600 * 1000 * 4.5).toISOString()
  },
  {
    id: 102,
    title: 'Staging Deploy',
    description: 'Regression suite + smoke tests',
    status: 'in_progress',
    difficulty: 'intermediate',
    started_at: new Date(Date.now() - 3600 * 1000 * 1.5).toISOString(),
    completed_at: null,
    created_at: new Date(Date.now() - 3600 * 1000 * 2).toISOString(),
    updated_at: new Date(Date.now() - 3600 * 1000 * 1).toISOString()
  },
  {
    id: 103,
    title: 'QA Deploy',
    description: 'Feature branches aggregated',
    status: 'planned',
    difficulty: 'beginner',
    started_at: null,
    completed_at: null,
    created_at: new Date(Date.now() - 3600 * 1000 * 1).toISOString(),
    updated_at: new Date().toISOString()
  }
];

const logs = [
  {
    id: 1,
    level: 'info',
    message: 'Deployed api@main build #451 to production',
    timestamp: new Date().toISOString()
  },
  {
    id: 2,
    level: 'warning',
    message: 'Queued staging deployment waiting on approvals',
    timestamp: new Date(Date.now() - 1000 * 60 * 5).toISOString()
  }
];

function delay(ms = 200) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function mockRequest<T>(path: string, options: RequestOptions): Promise<T> {
  await delay();
  const normalized = path.startsWith('/') ? path : `/${path}`;

  if (normalized.startsWith('/api/auth/login') && options.method === 'POST') {
    return {
      token: 'mock-token',
      admin: mockAdmin
    } as T;
  }

  if (normalized.startsWith('/api/auth/register') && options.method === 'POST') {
    return {
      token: 'mock-token',
      admin: { ...mockAdmin, username: options.data && (options.data as any).username }
    } as T;
  }

  if (normalized.startsWith('/api/status')) {
    const completed = sessions.filter((s) => s.status === 'completed').length;
    const inProgress = sessions.filter((s) => s.status === 'in_progress').length;
    const queued = sessions.filter((s) => s.status !== 'completed').length;
    return {
      status: 'operational',
      successful_deployments: completed,
      failed_deployments: Math.max(0, queued - inProgress),
      active_pipelines: sessions.length,
      avg_build_time: 12.4,
      logs
    } as T;
  }

  if (normalized.startsWith('/api/sessions')) {
    return {
      data: sessions
    } as T;
  }

  if (normalized.startsWith('/api/deployments/history')) {
    const now = Date.now();
    const points = Array.from({ length: 7 }).map((_, index) => ({
      date: new Date(now - (6 - index) * 24 * 60 * 60 * 1000).toISOString(),
      successful: Math.floor(Math.random() * 5) + 1,
      failed: Math.floor(Math.random() * 2)
    }));
    return { data: points } as T;
  }

  return {} as T;
}

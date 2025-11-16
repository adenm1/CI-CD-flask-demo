import { request } from './client';
import type { Pipeline } from './pipelines';

export type DeploymentStats = {
  successful: number;
  failed: number;
  active: number;
  avgBuildTime: number;
};

export type DeploymentHistoryPoint = {
  date: string;
  successful: number;
  failed: number;
};

export type DeploymentLog = {
  id: number;
  message: string;
  level: 'info' | 'warning' | 'error';
  timestamp: string;
};

function deriveStatsFromPipelines(pipelines: Pipeline[] = []): DeploymentStats {
  const successful = pipelines.filter((p) => p.status === 'success').length;
  const active = pipelines.filter((p) => p.status !== 'success').length;
  const failed = Math.max(0, pipelines.length - successful - active);
  const avg = pipelines
    .map((p) => p.durationMinutes || 0)
    .filter(Boolean);
  const avgBuildTime = avg.length ? Number((avg.reduce((a, b) => a + b, 0) / avg.length).toFixed(1)) : 0;
  return { successful, failed, active, avgBuildTime };
}

export async function fetchDeploymentStats(pipelines?: Pipeline[]): Promise<DeploymentStats> {
  try {
    const response = await request<DeploymentStats>('/api/pipelines/stats');
    return response;
  } catch (error) {
    console.error('Failed to fetch deployment stats:', error);
    return deriveStatsFromPipelines(pipelines || []);
  }
}

export async function fetchDeploymentHistory(pipelines?: Pipeline[]): Promise<DeploymentHistoryPoint[]> {
  try {
    const response = await request<{ history: DeploymentHistoryPoint[] }>('/api/pipelines/history');
    if (Array.isArray(response.history)) {
      return response.history;
    }
  } catch (error) {
    console.error('Failed to fetch deployment history:', error);
  }

  // Fallback to empty data
  const days = Array.from({ length: 7 }).map((_, index) => {
    const date = new Date();
    date.setDate(date.getDate() - (6 - index));
    return {
      date: date.toISOString().split('T')[0],
      successful: 0,
      failed: 0
    };
  });
  return days;
}

export async function fetchDeploymentLogs(pipelines?: Pipeline[]): Promise<DeploymentLog[]> {
  try {
    const response = await request<{ logs: DeploymentLog[] }>('/api/pipelines/logs');
    if (Array.isArray(response.logs)) {
      return response.logs;
    }
  } catch (error) {
    console.error('Failed to fetch deployment logs:', error);
  }

  // Return empty array as fallback
  return [];
}

import { writable } from 'svelte/store';
import { fetchPipelines } from '$lib/api/pipelines';
import { fetchDeploymentHistory, fetchDeploymentLogs, fetchDeploymentStats, type DeploymentHistoryPoint, type DeploymentLog, type DeploymentStats } from '$lib/api/deployments';
import type { Pipeline } from '$lib/api/pipelines';
import { ApiError } from '$lib/api/client';
import { authStore } from '$lib/stores/auth';

export type PipelineStoreState = {
  pipelines: Pipeline[];
  metrics: DeploymentStats;
  history: DeploymentHistoryPoint[];
  logs: DeploymentLog[];
  lastUpdated: string | null;
  loading: boolean;
  error: string | null;
};

const REFRESH_INTERVAL = Number(import.meta.env.VITE_DASHBOARD_REFRESH_MS || 10000);

function createPipelineStore() {
  const { subscribe, set, update } = writable<PipelineStoreState>({
    pipelines: [],
    metrics: { successful: 0, failed: 0, active: 0, avgBuildTime: 0 },
    history: [],
    logs: [],
    lastUpdated: null,
    loading: false,
    error: null
  });

  let timer: ReturnType<typeof setInterval> | null = null;

  async function refresh() {
    update((state) => ({ ...state, loading: true, error: null }));
    try {
      const { pipelines } = await fetchPipelines();
      const [metrics, history, logs] = await Promise.all([
        fetchDeploymentStats(pipelines),
        fetchDeploymentHistory(pipelines),
        fetchDeploymentLogs(pipelines)
      ]);
      set({
        pipelines,
        metrics,
        history,
        logs,
        lastUpdated: new Date().toISOString(),
        loading: false,
        error: null
      });
    } catch (error) {
      let message = error instanceof Error ? error.message : 'Failed to fetch dashboard data';
      if (error instanceof ApiError && (error.status === 401 || error.status === 403)) {
        authStore.logout();
        stop();
        message = 'Session expired. Please sign in again.';
      }

      update((state) => ({
        ...state,
        loading: false,
        error: message
      }));
    }
  }

  function start() {
    if (timer) return;
    refresh();
    timer = setInterval(refresh, REFRESH_INTERVAL);
  }

  function stop() {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
  }

  return { subscribe, refresh, start, stop };
}

export const pipelinesStore = createPipelineStore();

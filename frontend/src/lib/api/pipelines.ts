import { request } from './client';

export type Pipeline = {
  id: number;
  name: string;
  description?: string;
  status: 'queued' | 'running' | 'success' | 'failed';
  owner: string;
  lastRun: string | null;
  durationMinutes: number | null;
};

export type PipelineMetrics = {
  successful: number;
  failed: number;
  active: number;
};

type BackendPipeline = {
  id: number;
  name: string;
  description?: string;
  status: string;
  owner: string;
  completedAt?: string | null;
  startedAt?: string;
  durationMinutes?: number | null;
};

function transformPipeline(record: BackendPipeline): Pipeline {
  return {
    id: record.id,
    name: record.name,
    description: record.description,
    status: (record.status as Pipeline['status']) || 'queued',
    owner: record.owner,
    lastRun: record.completedAt || record.startedAt || null,
    durationMinutes: record.durationMinutes || null
  };
}

export async function fetchPipelines(): Promise<{ pipelines: Pipeline[]; metrics: PipelineMetrics }> {
  try {
    const response = await request<{ pipelines: BackendPipeline[] }>('/api/pipelines');
    const pipelines = response.pipelines.map(transformPipeline);

    const successful = pipelines.filter((p) => p.status === 'success').length;
    const failed = pipelines.filter((p) => p.status === 'failed').length;
    const running = pipelines.filter((p) => p.status === 'running').length;

    return {
      pipelines,
      metrics: {
        successful,
        failed,
        active: running
      }
    };
  } catch (error) {
    console.error('Failed to fetch pipelines:', error);
    throw error;
  }
}

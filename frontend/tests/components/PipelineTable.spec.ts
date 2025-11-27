import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/svelte';
import PipelineTable from '$components/PipelineTable.svelte';
import type { Pipeline } from '$lib/api/pipelines';

describe('PipelineTable', () => {
  const pipelines: Pipeline[] = [
    {
      id: 1,
      name: 'Prod deploy',
      description: 'Blue/green release',
      status: 'success',
      owner: 'OPS',
      lastRun: new Date().toISOString(),
      durationMinutes: 18
    }
  ];

  it('renders pipeline rows', () => {
    render(PipelineTable, { pipelines });
    expect(screen.getByText('Prod deploy')).toBeInTheDocument();
    expect(screen.getByText('success')).toBeInTheDocument();
  });
});

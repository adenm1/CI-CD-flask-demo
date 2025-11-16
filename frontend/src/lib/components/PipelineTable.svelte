<script lang="ts">
  import type { Pipeline } from '$lib/api/pipelines';
  import { formatDate, formatDuration, formatRelativeTime } from '$lib/utils/format';

  export let pipelines: Pipeline[] = [];

  const statusClasses: Record<Pipeline['status'], string> = {
    queued: 'bg-tablegrey text-body/70',
    running: 'bg-secondary/10 text-secondary',
    success: 'bg-success/10 text-success'
  };
</script>

<div class="overflow-hidden rounded-apple-xl border border-white/40 bg-card/80 shadow-soft backdrop-blur-sm">
  <div class="flex items-center justify-between border-b border-tablegrey/40 px-6 py-5 bg-gradient-to-r from-card to-background/20">
    <div>
      <p class="text-xs font-medium uppercase tracking-[0.15em] text-body/50">Active Deployments</p>
      <p class="mt-1 text-lg font-bold text-heading">Pipelines</p>
    </div>
    <button class="group flex items-center gap-2 rounded-apple-lg border border-tablegrey/60 bg-white/70 px-4 py-2.5 text-sm font-medium text-body/70 transition hover:border-primary hover:bg-primary/5 hover:text-primary">
      <svg class="h-4 w-4 transition group-hover:scale-110" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
      </svg>
      Export
    </button>
  </div>
  <div class="max-h-[420px] overflow-y-auto">
    <table class="min-w-full divide-y divide-tablegrey/40 text-sm">
      <thead class="sticky top-0 bg-background/80 backdrop-blur-sm text-xs uppercase tracking-[0.1em] text-body/60">
        <tr>
          <th class="px-6 py-4 text-left font-semibold">Pipeline</th>
          <th class="px-6 py-4 text-left font-semibold">Status</th>
          <th class="px-6 py-4 text-left font-semibold">Owner</th>
          <th class="px-6 py-4 text-left font-semibold">Last Run</th>
          <th class="px-6 py-4 text-left font-semibold">Duration</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-tablegrey/30 bg-white/40">
        {#if pipelines.length === 0}
          <tr>
            <td class="px-6 py-12 text-center" colspan="5">
              <div class="flex flex-col items-center gap-3">
                <div class="flex h-16 w-16 items-center justify-center rounded-apple-lg bg-tablegrey/30">
                  <svg class="h-8 w-8 text-body/40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <p class="text-body/60">No pipelines yet</p>
              </div>
            </td>
          </tr>
        {:else}
          {#each pipelines as pipeline}
            <tr class="group transition hover:bg-primary/5">
              <td class="whitespace-nowrap px-6 py-4 text-heading">
                <p class="font-semibold group-hover:text-primary transition">{pipeline.name}</p>
                <p class="text-xs text-body/60">{pipeline.description ?? 'Continuous deployment'}</p>
              </td>
              <td class="px-6 py-4">
                <span class={`inline-flex items-center gap-1.5 rounded-apple-md px-3 py-1.5 text-xs font-semibold ${statusClasses[pipeline.status]}`}>
                  {#if pipeline.status === 'running'}
                    <span class="h-1.5 w-1.5 rounded-full bg-secondary animate-pulse"></span>
                  {:else if pipeline.status === 'success'}
                    <span class="h-1.5 w-1.5 rounded-full bg-success"></span>
                  {:else}
                    <span class="h-1.5 w-1.5 rounded-full bg-body/40"></span>
                  {/if}
                  {pipeline.status}
                </span>
              </td>
              <td class="px-6 py-4 text-body/70 font-medium">{pipeline.owner}</td>
              <td class="px-6 py-4 text-body/70">
                <p class="font-medium">{formatDate(pipeline.lastRun)}</p>
                <p class="text-xs text-body/50">{formatRelativeTime(pipeline.lastRun)}</p>
              </td>
              <td class="px-6 py-4 font-semibold text-body/70">{formatDuration(pipeline.durationMinutes)}</td>
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  </div>
</div>

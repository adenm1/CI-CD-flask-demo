<script lang="ts">
  import type { DeploymentLog } from '$lib/api/deployments';
  import { formatRelativeTime } from '$lib/utils/format';

  let { logs = [] }: { logs?: DeploymentLog[] } = $props();
  let open = $state(true);
</script>

<div class="overflow-hidden rounded-apple-xl border border-white/40 bg-card/80 shadow-soft backdrop-blur-sm">
  <button
    class="group flex w-full items-center justify-between border-b border-tablegrey/40 px-6 py-5 text-left transition bg-gradient-to-r from-card to-background/20 hover:from-card hover:to-background/30"
    onclick={() => (open = !open)}
  >
    <div>
      <p class="text-xs font-medium uppercase tracking-[0.15em] text-body/50">Real-time Events</p>
      <p class="mt-1 text-lg font-bold text-heading">Log Stream</p>
    </div>
    <div class="flex items-center gap-2 rounded-apple-lg bg-white/60 px-3 py-2 text-sm font-medium text-body/60 transition group-hover:bg-white/80">
      <span>{open ? 'Collapse' : 'Expand'}</span>
      <svg class={`h-4 w-4 transition-transform duration-300 ${open ? 'rotate-180' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </div>
  </button>
  {#if open}
    <div class="max-h-80 overflow-y-auto divide-y divide-tablegrey/30">
      {#if logs.length === 0}
        <div class="flex flex-col items-center gap-3 px-6 py-12">
          <div class="flex h-16 w-16 items-center justify-center rounded-apple-lg bg-tablegrey/30">
            <svg class="h-8 w-8 text-body/40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <p class="text-sm text-body/60">No recent log entries</p>
        </div>
      {:else}
        {#each logs as log}
          <div class="group flex items-start gap-4 px-6 py-4 transition hover:bg-primary/5">
            <div class={`mt-1 flex h-7 w-20 shrink-0 items-center justify-center rounded-apple-md text-xs font-bold uppercase tracking-wider ${log.level === 'error' ? 'bg-error/10 text-error' : log.level === 'warning' ? 'bg-accent/10 text-accent' : 'bg-success/10 text-success'}`}>
              {log.level}
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-heading break-words">{log.message}</p>
              <div class="mt-1 flex items-center gap-2">
                <svg class="h-3 w-3 text-body/40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p class="text-xs text-body/60">{formatRelativeTime(log.timestamp)}</p>
              </div>
            </div>
          </div>
        {/each}
      {/if}
    </div>
  {/if}
</div>

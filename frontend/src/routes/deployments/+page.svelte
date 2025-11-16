<script lang="ts">
  import DeploymentChart from '$components/DeploymentChart.svelte';
  import LogDrawer from '$components/LogDrawer.svelte';
  import { pipelinesStore } from '$lib/stores/pipelines';
  import { formatDate, formatDuration, formatRelativeTime } from '$lib/utils/format';

  const store = pipelinesStore;

  $: history = $store.history;
  $: logs = $store.logs;
  const timestamp = (value?: string | null) => (value ? new Date(value).getTime() : 0);
  $: recentDeployments = $store.pipelines
    .slice()
    .sort((a, b) => timestamp(b.lastRun) - timestamp(a.lastRun))
    .slice(0, 6);
</script>

<section class="space-y-8">
  <header>
    <p class="text-sm uppercase tracking-[0.4em] text-body/50">Deployments</p>
    <h2 class="text-3xl font-semibold text-heading">Release insights</h2>
    <p class="text-body/60">Track healthy deploys, regressions, and execution timelines.</p>
  </header>

  <div class="grid gap-6 lg:grid-cols-3">
    <div class="lg:col-span-2">
      <DeploymentChart data={history} />
    </div>
    <LogDrawer {logs} />
  </div>

  <div class="card overflow-hidden">
    <div class="border-b border-tablegrey/60 px-6 py-4">
      <p class="text-lg font-semibold text-heading">Recent deployments</p>
    </div>
    <div class="divide-y divide-tablegrey/50">
      {#if recentDeployments.length === 0}
        <p class="px-6 py-6 text-body/60">No deployments tracked yet.</p>
      {:else}
        {#each recentDeployments as deployment}
          <div class="flex flex-wrap items-center gap-4 px-6 py-4 text-sm text-body/70">
            <div class="flex-1">
              <p class="font-semibold text-heading">{deployment.name}</p>
              <p class="text-xs text-body/50">{formatRelativeTime(deployment.lastRun)}</p>
            </div>
            <span class={`rounded-full px-3 py-1 text-xs font-semibold ${deployment.status === 'success' ? 'bg-success/10 text-success' : deployment.status === 'running' ? 'bg-secondary/10 text-secondary' : 'bg-tablegrey text-body/70'}`}>
              {deployment.status}
            </span>
            <div>
              <p class="font-medium text-heading">{formatDate(deployment.lastRun)}</p>
              <p class="text-xs text-body/50">Duration {formatDuration(deployment.durationMinutes)}</p>
            </div>
          </div>
        {/each}
      {/if}
    </div>
  </div>
</section>

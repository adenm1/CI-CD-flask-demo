<script lang="ts">
  import Card from '$components/Card.svelte';
  import PipelineTable from '$components/PipelineTable.svelte';
  import DeploymentChart from '$components/DeploymentChart.svelte';
  import LogDrawer from '$components/LogDrawer.svelte';
  import { pipelinesStore } from '$lib/stores/pipelines';
  import { formatRelativeTime } from '$lib/utils/format';

  const store = pipelinesStore;
  let storeError = $derived($store.error);

  let metrics = $derived($store.metrics);
  let history = $derived($store.history);
  let logs = $derived($store.logs);
  let lastUpdated = $derived($store.lastUpdated);
  let pipelines = $derived($store.pipelines);

  function retryFetch() {
    store.refresh();
  }
  type CardConfig = {
    title: string;
    value: string | number;
    accent: 'primary' | 'secondary' | 'success' | 'error' | 'accent';
    trendLabel: string;
    trendValue: string;
    trendPositive: boolean;
    icon: string;
  };
  let cards = $derived([
    { title: 'Successful deployments', value: metrics.successful, accent: 'primary' as const, trendLabel: 'vs last refresh', trendValue: '+4%', trendPositive: true, icon: '🚀' },
    { title: 'Failed deployments', value: metrics.failed, accent: 'error' as const, trendLabel: 'vs last refresh', trendValue: '-1%', trendPositive: false, icon: '⚠️' },
    { title: 'Active pipelines', value: metrics.active, accent: 'secondary' as const, trendLabel: 'currently running', trendValue: `${metrics.active} pipelines`, trendPositive: true, icon: '🛠️' },
    { title: 'Avg build time', value: `${metrics.avgBuildTime} min`, accent: 'accent' as const, trendLabel: 'rolling average', trendValue: '~12m', trendPositive: true, icon: '⏱️' }
  ]);
</script>

<div class="space-y-10">
  <!-- Hero Section -->
  <section class="relative overflow-hidden rounded-apple-2xl border border-white/40 bg-gradient-to-br from-primary/5 via-card/95 to-secondary/5 p-6 sm:p-8 shadow-soft backdrop-blur-sm">
    <div class="relative z-10">
      <div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p class="text-xs font-medium uppercase tracking-[0.2em] text-primary">Dashboard</p>
          <h1 class="mt-2 text-3xl sm:text-4xl font-bold tracking-tight text-heading">Live Deployment Overview</h1>
          <p class="mt-2 text-base sm:text-lg text-body/70">Unified telemetry for pipelines, deploys, and release health.</p>
        </div>
        <div class="flex items-center gap-2 rounded-apple-lg bg-background/80 px-4 py-2 backdrop-blur-sm w-full sm:w-auto justify-between sm:justify-center">
          <svg class="h-4 w-4 text-success animate-pulse" fill="currentColor" viewBox="0 0 20 20">
            <circle cx="10" cy="10" r="5"/>
          </svg>
          <p class="text-sm font-medium text-body/80">Updated {lastUpdated ? formatRelativeTime(lastUpdated) : '—'}</p>
        </div>
      </div>
    </div>

    <!-- Decorative gradient blobs -->
    <div class="absolute -right-20 -top-20 h-64 w-64 rounded-full bg-primary/10 blur-3xl"></div>
    <div class="absolute -bottom-20 -left-20 h-64 w-64 rounded-full bg-secondary/10 blur-3xl"></div>
  </section>

  {#if storeError}
    <div class="rounded-apple-lg border border-error/40 bg-error/5 p-4 text-sm text-error flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div class="flex items-center gap-2">
        <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
        </svg>
        <span>{storeError}</span>
      </div>
      <button class="rounded-apple-lg border border-error/40 px-4 py-2 text-error hover:bg-error/10 transition" onclick={retryFetch}>
        Retry
      </button>
    </div>
  {/if}

  <!-- Metrics Cards -->
  <section>
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-heading">Key Metrics</h2>
      <p class="mt-1 text-sm text-body/60">Real-time deployment statistics and trends</p>
    </div>
    <div class="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
      {#each cards as card}
        <Card {...card}>
          {#snippet icon()}
            <span class="text-xl">{card.icon}</span>
          {/snippet}
        </Card>
      {/each}
    </div>
  </section>

  <!-- Data Visualization Section -->
  <section class="grid gap-6 lg:grid-cols-3">
    <!-- Left Column: Pipelines & Logs -->
    <div class="space-y-6 lg:col-span-2">
      <PipelineTable {pipelines} />
      <LogDrawer {logs} />
    </div>

    <!-- Right Column: Chart -->
    <div class="lg:col-span-1">
      <DeploymentChart data={history} />
    </div>
  </section>
</div>

<script lang="ts">
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import type { DeploymentHistoryPoint } from '$lib/api/deployments';

  let { data = [] }: { data: DeploymentHistoryPoint[] } = $props();

  let ApexChart: any = $state(undefined);
  let mounted = $state(false);

  onMount(async () => {
    if (browser) {
      const module = await import('svelte-apexcharts');
      ApexChart = module.default;
      mounted = true;
    }
  });

  let categories = $derived(data.map((point) =>
    new Date(point.date).toLocaleDateString('en', { weekday: 'short' })
  ));

  const baseOptions = {
    chart: {
      type: 'area',
      toolbar: { show: false },
      foreColor: '#374151'
    },
    dataLabels: { enabled: false },
    stroke: { curve: 'smooth', width: 3 },
    colors: ['#1CB5A3', '#E63946'],
    grid: { strokeDashArray: 4 }
  };

  let series = $derived([
    { name: 'Successful', data: data.map((point) => point.successful) },
    { name: 'Failed', data: data.map((point) => point.failed) }
  ]);
</script>

<div class="overflow-hidden rounded-apple-xl border border-white/40 bg-card/80 p-6 shadow-soft backdrop-blur-sm">
  <div class="flex items-center justify-between">
    <div>
      <p class="text-xs font-medium uppercase tracking-[0.15em] text-body/50">Performance Metrics</p>
      <p class="mt-1 text-lg font-bold text-heading">Deployment History</p>
    </div>
    <div class="flex items-center gap-2 rounded-apple-lg bg-gradient-to-r from-primary/5 to-secondary/5 px-3 py-2 backdrop-blur-sm">
      <svg class="h-4 w-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
      <p class="text-sm font-medium text-body/70">7-day window</p>
    </div>
  </div>
  <div class="mt-6">
    {#if mounted && ApexChart}
      <ApexChart
        options={{
          ...baseOptions,
          xaxis: { categories }
        }}
        {series}
        type="area"
        height="280"
      />
    {:else}
      <div class="h-[280px] flex flex-col items-center justify-center gap-3">
        <div class="h-12 w-12 animate-spin rounded-full border-4 border-tablegrey/30 border-t-primary"></div>
        <p class="text-sm text-body/60">Loading chart...</p>
      </div>
    {/if}
  </div>
</div>

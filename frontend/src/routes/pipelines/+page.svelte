<script lang="ts">
  import PipelineTable from '$components/PipelineTable.svelte';
  import { pipelinesStore } from '$lib/stores/pipelines';

  const store = pipelinesStore;
  let storeError = $derived($store.error);
  const filters = ['all', 'queued', 'running', 'success'] as const;
  type Filter = (typeof filters)[number];
  let statusFilter: Filter = $state('all');

  let pipelines = $derived($store.pipelines);
  let filtered = $derived(statusFilter === 'all' ? pipelines : pipelines.filter((p) => p.status === statusFilter));

  function retryFetch() {
    store.refresh();
  }
</script>

<section class="space-y-8">
  <header class="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
    <div>
      <p class="text-sm uppercase tracking-[0.4em] text-body/50">Pipelines</p>
      <h2 class="text-3xl font-semibold text-heading">Orchestrated workflows</h2>
      <p class="text-body/60">All deployment pipelines, with live orchestration signal.</p>
    </div>
    <div class="flex flex-wrap items-center gap-2">
      {#each filters as option}
        <button
          class={`rounded-2xl px-4 py-2 text-sm font-medium ${statusFilter === option ? 'bg-primary text-white' : 'bg-tablegrey/40 text-body/70'}`}
          onclick={() => (statusFilter = option)}
        >
          {option}
        </button>
      {/each}
    </div>
  </header>

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

  <PipelineTable pipelines={filtered} />
</section>

<script lang="ts">
  import PipelineTable from '$components/PipelineTable.svelte';
  import { pipelinesStore } from '$lib/stores/pipelines';

  const store = pipelinesStore;
  const filters = ['all', 'queued', 'running', 'success'] as const;
  type Filter = (typeof filters)[number];
  let statusFilter: Filter = 'all';

  $: pipelines = $store.pipelines;
  $: filtered = statusFilter === 'all' ? pipelines : pipelines.filter((p) => p.status === statusFilter);
</script>

<section class="space-y-8">
  <header class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
    <div>
      <p class="text-sm uppercase tracking-[0.4em] text-body/50">Pipelines</p>
      <h2 class="text-3xl font-semibold text-heading">Orchestrated workflows</h2>
      <p class="text-body/60">All deployment pipelines, with live orchestration signal.</p>
    </div>
    <div class="flex items-center gap-3">
      {#each filters as option}
        <button
          class={`rounded-2xl px-4 py-2 text-sm font-medium ${statusFilter === option ? 'bg-primary text-white' : 'bg-tablegrey/40 text-body/70'}`}
          on:click={() => (statusFilter = option)}
        >
          {option}
        </button>
      {/each}
    </div>
  </header>

  <PipelineTable pipelines={filtered} />
</section>

<script lang="ts">
  import { authStore } from '$lib/stores/auth';
  import { page } from '$app/stores';

  const auth = authStore;
  const titles: Record<string, string> = {
    '/': 'Mission Control',
    '/pipelines': 'Pipelines',
    '/deployments': 'Deployments',
    '/settings': 'Settings'
  };
  let headerTitle = $derived(titles[$page.url.pathname] ?? 'Mission Control');
</script>

<header class="sticky top-0 z-10 border-b border-white/30 bg-background/80 backdrop-blur-lg">
  <div class="flex flex-col gap-4 px-6 py-4 lg:flex-row lg:items-center lg:justify-between">
    <div>
      <p class="text-xs uppercase tracking-[0.3em] text-body/50">CI/CD CONTROL</p>
      <h1 class="text-2xl font-semibold text-heading">{headerTitle}</h1>
    </div>
    <div class="flex flex-1 flex-col gap-3 lg:flex-row lg:items-center lg:justify-end">
      <div class="relative w-full max-w-sm">
        <input
          class="w-full rounded-2xl border border-transparent bg-tablegrey/40 px-4 py-2 pl-10 text-sm text-body placeholder:text-body/50 focus:border-primary focus:bg-white focus:outline-none"
          placeholder="Search pipelines, deployments..."
          type="search"
        />
        <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-body/40">⌘K</span>
      </div>
      <div class="flex items-center gap-3">
        <button class="rounded-2xl bg-secondary px-4 py-2 text-sm font-medium text-white transition hover:bg-secondary-hover">
          New pipeline
        </button>
        <div class="flex items-center gap-2 rounded-2xl border border-tablegrey/80 px-4 py-2">
          <div class="grid h-10 w-10 place-items-center rounded-2xl bg-primary/10 text-sm font-semibold text-primary">
            {($auth.admin?.username || 'A').slice(0, 2).toUpperCase()}
          </div>
          <div>
            <p class="text-sm font-semibold text-heading">{$auth.admin?.username ?? 'admin'}</p>
            <p class="text-xs text-body/50">{$auth.admin?.role ?? 'owner'}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</header>

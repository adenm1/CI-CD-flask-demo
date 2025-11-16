<script lang="ts">
  import { page } from '$app/stores';
  import { authStore } from '$lib/stores/auth';

  const navItems = [
    { label: 'Dashboard', href: '/', icon: '🏠' },
    { label: 'Pipelines', href: '/pipelines', icon: '🛠️' },
    { label: 'Deployments', href: '/deployments', icon: '🚀' },
    { label: 'Settings', href: '/settings', icon: '⚙️' }
  ];

  const auth = authStore;
</script>

<aside class="hidden w-72 shrink-0 bg-card/80 shadow-soft backdrop-blur-lg lg:flex lg:flex-col">
  <div class="px-8 pt-10 pb-6 border-b border-white/20">
    <div class="text-2xl font-semibold text-heading">SiYing Liu's Project</div>
    <p class="mt-2 text-sm text-body/60">Unified control center</p>
  </div>
  <nav class="flex-1 space-y-2 px-4 py-6">
    {#each navItems as item}
      {#if $page.url.pathname === item.href}
        <a
          href={item.href}
          data-sveltekit-preload-data
          class="flex items-center gap-3 rounded-2xl bg-primary text-white px-4 py-3 font-medium shadow-soft transition hover:bg-primary-hover"
          aria-current="page"
          >
          <span>{item.icon}</span>
          {item.label}
        </a>
      {:else}
        <a
          href={item.href}
          data-sveltekit-preload-data
          class="flex items-center gap-3 rounded-2xl px-4 py-3 text-body/80 transition hover:bg-tablegrey/40"
          >
          <span>{item.icon}</span>
          {item.label}
        </a>
      {/if}
    {/each}
  </nav>
  <div class="border-t border-white/20 px-6 py-6">
    <p class="text-sm text-body/60">Signed in as</p>
    <p class="mt-1 font-medium text-heading">{$auth.admin?.username ?? '—'}</p>
    <button
      class="mt-4 w-full rounded-2xl border border-tablegrey/80 px-4 py-2 text-sm font-medium text-body/80 transition hover:bg-tablegrey/50"
      on:click={() => auth.logout()}
    >
      Log out
    </button>
  </div>
</aside>

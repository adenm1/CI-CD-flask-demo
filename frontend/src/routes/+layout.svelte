<script lang="ts">
  import '../app.css';
  import Sidebar from '$components/Sidebar.svelte';
  import Header from '$components/Header.svelte';
  import { authStore } from '$lib/stores/auth';
  import { pipelinesStore } from '$lib/stores/pipelines';
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';
  import type { PageData } from './$types';

  export let data: PageData;

  const auth = authStore;

  onMount(() => {
    auth.initialize();
  });

  $: isAuthRoute = $page.url.pathname.startsWith('/login');
  $: isAuthenticated = Boolean($auth.token);
  $: if (isAuthenticated) {
    pipelinesStore.start();
  } else {
    pipelinesStore.stop();
  }
  $: if (browser && !isAuthenticated && !isAuthRoute) {
    goto('/login');
  }
</script>

<svelte:head>
  <title>CI/CD Control Center</title>
  <meta name="theme-color" content="#1CB5A3" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
</svelte:head>

{#if !isAuthRoute && isAuthenticated}
  <div class="flex min-h-screen bg-background text-body">
    <Sidebar />
    <div class="flex flex-1 flex-col bg-background">
      <Header />
      <main class="flex-1 p-6 lg:p-10">
        <slot />
      </main>
    </div>
  </div>
{:else}
  <main class="min-h-screen bg-background flex items-center justify-center p-6">
    <slot />
  </main>
{/if}

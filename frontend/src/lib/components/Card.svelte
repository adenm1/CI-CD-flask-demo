<script lang="ts">
  let {
    title,
    value,
    subtitle = '',
    accent = 'primary' as 'primary' | 'secondary' | 'success' | 'error' | 'accent',
    trendLabel = null as string | null,
    trendValue = null as string | null,
    trendPositive = true,
    icon
  }: {
    title: string;
    value: string | number;
    subtitle?: string;
    accent?: 'primary' | 'secondary' | 'success' | 'error' | 'accent';
    trendLabel?: string | null;
    trendValue?: string | null;
    trendPositive?: boolean;
    icon?: import('svelte').Snippet;
  } = $props();

  const accentClass = {
    primary: 'bg-primary',
    secondary: 'bg-secondary',
    success: 'bg-success',
    error: 'bg-error',
    accent: 'bg-accent'
  };
</script>

<div class="group relative overflow-hidden rounded-apple-xl border border-white/40 bg-gradient-to-br from-card/95 to-card/80 p-6 shadow-soft backdrop-blur-sm transition-all duration-300 hover:shadow-xl hover:scale-[1.02]">
  <!-- Gradient overlay on hover -->
  <div class="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100"></div>

  <div class="relative z-10">
    <div class="flex items-start justify-between">
      <div class="flex-1">
        <p class="text-xs font-medium uppercase tracking-[0.15em] text-body/50">{title}</p>
        <p class="mt-3 text-4xl font-bold tracking-tight text-heading">{value}</p>
        {#if subtitle}
          <p class="mt-2 text-sm text-body/60">{subtitle}</p>
        {/if}
      </div>
      <div class={`flex h-14 w-14 items-center justify-center rounded-apple-lg ${accentClass[accent]}/10 text-2xl transition-transform duration-300 group-hover:scale-110`}>
        {#if icon}{@render icon()}{/if}
      </div>
    </div>

    {#if trendLabel && trendValue}
      <div class="mt-5 flex items-center gap-2 rounded-apple-md bg-background/50 px-3 py-2 text-sm backdrop-blur-sm">
        <span class={`inline-flex items-center gap-1 font-semibold ${trendPositive ? 'text-success' : 'text-error'}`}>
          {#if trendPositive}
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          {:else}
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
            </svg>
          {/if}
          {trendValue}
        </span>
        <span class="text-body/60">{trendLabel}</span>
      </div>
    {/if}
  </div>
</div>

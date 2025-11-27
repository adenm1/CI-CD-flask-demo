<script lang="ts">
  import { authStore } from '$lib/stores/auth';
  import { browser } from '$app/environment';

  const auth = authStore;
  let telemetry = $state(true);
  let notifications = $state(true);
  let refresh = $state(10);

  function copyToken() {
    if (!browser || !$auth.token) return;
    navigator.clipboard.writeText($auth.token);
  }
</script>

<section class="space-y-8">
  <header>
    <p class="text-sm uppercase tracking-[0.4em] text-body/50">Settings</p>
    <h2 class="text-3xl font-semibold text-heading">Control center preferences</h2>
    <p class="text-body/60">Configure security, notifications, and telemetry.</p>
  </header>

  <div class="grid gap-6 lg:grid-cols-2">
    <!-- Access Token Card -->
    <div class="card space-y-6 p-6">
      <div>
        <h3 class="text-xl font-semibold text-heading">Access token</h3>
        <p class="text-sm text-body/60">Keep this token secret; it authenticates API calls.</p>
      </div>
      <div class="rounded-apple-lg border border-tablegrey/60 bg-background/50 p-4 text-sm font-mono break-all">
        {$auth.token ?? '—'}
      </div>
      <button class="rounded-apple-lg bg-secondary px-4 py-2 text-sm font-medium text-white hover:bg-secondary-hover transition" onclick={copyToken}>
        Copy token
      </button>
    </div>

    <!-- Notifications Card -->
    <form class="card space-y-6 p-6">
      <div>
        <h3 class="text-xl font-semibold text-heading">Notifications</h3>
        <p class="text-sm text-body/60">Stay informed when pipelines fail or succeed.</p>
      </div>
      <label class="flex items-center justify-between text-sm font-medium text-heading">
        Pipeline summaries
        <input type="checkbox" bind:checked={notifications} class="rounded border-tablegrey/80 text-primary focus:ring-primary" />
      </label>
      <label class="flex items-center justify-between text-sm font-medium text-heading">
        Telemetry sharing
        <input type="checkbox" bind:checked={telemetry} class="rounded border-tablegrey/80 text-primary focus:ring-primary" />
      </label>
      <label class="block text-sm font-medium text-heading">
        Auto refresh (seconds)
        <input
          type="number"
          min="5"
          max="60"
          step="5"
          bind:value={refresh}
          class="mt-2 w-full rounded-apple-lg border border-tablegrey/80 px-4 py-2 focus:border-primary focus:outline-none"
        />
      </label>
      <button type="button" class="rounded-apple-lg bg-primary px-4 py-2 text-sm font-semibold text-white hover:bg-primary-hover transition">
        Save preferences
      </button>
    </form>
  </div>

  <div class="mt-6">
    <div class="card space-y-4 p-6 max-w-2xl">
      <div>
        <h3 class="text-xl font-semibold text-heading">Credential management</h3>
        <p class="text-sm text-body/60">Rotate passwords and enroll MFA through the backend security workflow; this dashboard never stores passwords in the browser.</p>
      </div>
      <ul class="list-disc space-y-2 pl-6 text-sm text-body/70">
        <li>Use the approved admin tooling to reset credentials instead of the UI.</li>
        <li>Call the <code>/api/auth/totp/enroll</code> endpoint to add TOTP once you are signed in.</li>
        <li>Keep your access logs updated when credentials change.</li>
      </ul>
    </div>
  </div>

</section>

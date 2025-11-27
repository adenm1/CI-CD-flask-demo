<script lang="ts">
  import { goto } from '$app/navigation';
  import { login, requestAccess } from '$lib/api/auth';
  import { authStore } from '$lib/stores/auth';

  const registrationEnabled = import.meta.env.VITE_ENABLE_REGISTER === 'true';
  const forgotPasswordEnabled = false; // Forgot password disabled until a real flow exists
  const auth = authStore;
  let username = $state('');
  let password = $state('');
  let totpCode = $state('');
  let showPassword = $state(false);
  let error = $state<string | null>(null);
  let loading = $state(false);
  let showRegisterModal = $state(false);

  // Register form state
  let registerUsername = $state('');
  let registerPassword = $state('');
  let registerShowPassword = $state(false);
  let registerError = $state<string | null>(null);
  let registerReason = $state('');
  let registerSuccess = $state<string | null>(null);
  let registerLoading = $state(false);

  function closeRegisterOverlay() {
    showRegisterModal = false;
  }

  function handleBackdropKey(event: KeyboardEvent, close: () => void) {
    if (event.key === 'Escape' || event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      close();
    }
  }

  async function handleLogin() {
    loading = true;
    error = null;
    try {
      const response = await login({ username, password, totpCode: totpCode || undefined });
      auth.login(response.token, response.admin);
      goto('/');
    } catch (err) {
      error = err instanceof Error ? err.message : 'Unable to authenticate';
    } finally {
      loading = false;
    }
  }

  async function handleRegister() {
    registerLoading = true;
    registerError = null;
    registerSuccess = null;
    try {
      const response = await requestAccess({ username: registerUsername, password: registerPassword, reason: registerReason });
      registerSuccess = response.message ?? 'Request submitted for approval.';
      registerUsername = '';
      registerPassword = '';
      registerReason = '';
      showRegisterModal = false;
    } catch (err) {
      registerError = err instanceof Error ? err.message : 'Unable to register';
    } finally {
      registerLoading = false;
    }
  }
</script>

<div class="max-w-xl w-full space-y-8">
  <!-- Sign up link above card -->
  {#if registrationEnabled}
    <div class="text-center text-sm text-body/70">
      Don't have an account?
      <button class="font-semibold text-primary hover:text-primary-hover transition" onclick={() => (showRegisterModal = true)}>
        Request access
      </button>
    </div>
  {/if}

  <!-- Login Card -->
  <div class="rounded-apple-2xl border border-white/40 bg-card/80 p-10 shadow-soft backdrop-blur">
    <p class="text-sm uppercase tracking-[0.4em] text-body/50">SiYing Liu's Project</p>
    <h2 class="mt-3 text-3xl font-semibold text-heading">Welcome back</h2>
    <p class="text-body/60">Sign in to access your dashboard.</p>

    <form class="mt-8 space-y-4" onsubmit={(e) => { e.preventDefault(); handleLogin(e); }}>
      <label class="block text-sm font-medium text-heading">
        Username
        <input
          class="mt-2 w-full rounded-apple-lg border border-tablegrey/80 bg-white/70 px-4 py-3 text-body placeholder:text-body/40 focus:border-primary focus:outline-none"
          placeholder="username"
          bind:value={username}
          required
        />
      </label>

      <label class="block text-sm font-medium text-heading">
        Password
        <div class="relative mt-2">
          {#if showPassword}
            <input
              class="w-full rounded-apple-lg border border-tablegrey/80 bg-white/70 px-4 py-3 pr-12 text-body placeholder:text-body/40 focus:border-primary focus:outline-none"
              placeholder="••••••••"
              bind:value={password}
              type="text"
              required
            />
          {:else}
            <input
              class="w-full rounded-apple-lg border border-tablegrey/80 bg-white/70 px-4 py-3 pr-12 text-body placeholder:text-body/40 focus:border-primary focus:outline-none"
              placeholder="••••••••"
              bind:value={password}
              type="password"
              required
            />
          {/if}
          <button
            type="button"
            class="absolute right-3 top-1/2 -translate-y-1/2 text-body/60 hover:text-body transition"
            onmousedown={() => (showPassword = true)}
            onmouseup={() => (showPassword = false)}
            onmouseleave={() => (showPassword = false)}
            ontouchstart={() => (showPassword = true)}
            ontouchend={() => (showPassword = false)}
            aria-label="Show password while pressing"
          >
            {#if showPassword}
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
              </svg>
            {:else}
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            {/if}
          </button>
        </div>
      </label>

      <label class="block text-sm font-medium text-heading">
        One-time code (TOTP, optional)
        <input
          class="mt-2 w-full rounded-apple-lg border border-tablegrey/80 bg-white/70 px-4 py-3 text-body placeholder:text-body/40 focus:border-primary focus:outline-none"
          placeholder="123456"
          bind:value={totpCode}
          inputmode="numeric"
          pattern="[0-9]*"
        />
      </label>


      {#if error}
        <p class="rounded-apple-lg bg-error/10 px-4 py-3 text-sm text-error">{error}</p>
      {/if}

      <button
        class="w-full rounded-apple-lg px-4 py-3 text-sm font-semibold text-white transition bg-primary hover:bg-primary-hover"
        type="submit"
        disabled={loading}
      >
        {loading ? 'Processing…' : 'Sign in'}
      </button>

      {#if registerSuccess}
        <p class="rounded-apple-lg bg-success/10 px-4 py-3 text-sm text-success">{registerSuccess}</p>
      {/if}

      <!-- Forgot Password Link -->
      <div class="text-center text-xs text-body/60">
        Forgot password? Contact an existing admin to reset. Self-service is not available yet.
      </div>
    </form>
  </div>
</div>

<!-- Registration Modal (Floating) -->
{#if showRegisterModal}
  <!-- Backdrop -->
  <div
    class="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 transition-opacity"
    role="button"
    tabindex="0"
    aria-label="Close registration modal"
    onclick={closeRegisterOverlay}
    onkeydown={(event) => handleBackdropKey(event, closeRegisterOverlay)}
  ></div>

  <!-- Modal -->
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <div class="max-w-md w-full rounded-apple-2xl border border-white/40 bg-card shadow-soft p-8 relative animate-in fade-in zoom-in duration-200">
      <!-- Close button -->
      <button
        class="absolute top-4 right-4 text-body/60 hover:text-body transition"
        onclick={closeRegisterOverlay}
        type="button"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <p class="text-sm uppercase tracking-[0.4em] text-body/50">SiYing Liu's Project</p>
      <h2 class="mt-3 text-2xl font-semibold text-heading">Request access</h2>
      <p class="text-body/60">Submit your details for admin approval.</p>

      <form class="mt-6 space-y-4" onsubmit={(e) => { e.preventDefault(); handleRegister(e); }}>
        <label class="block text-sm font-medium text-heading">
          Username
          <input
            class="mt-2 w-full rounded-apple-lg border border-tablegrey/80 bg-white/70 px-4 py-3 text-body placeholder:text-body/40 focus:border-secondary focus:outline-none"
            placeholder="username"
            bind:value={registerUsername}
            required
          />
        </label>

        <label class="block text-sm font-medium text-heading">
          Password
          <div class="relative mt-2">
            {#if registerShowPassword}
              <input
                class="w-full rounded-apple-lg border border-tablegrey/80 bg-white/70 px-4 py-3 pr-12 text-body placeholder:text-body/40 focus:border-secondary focus:outline-none"
                placeholder="••••••••"
                bind:value={registerPassword}
                type="text"
                required
              />
            {:else}
              <input
                class="w-full rounded-apple-lg border border-tablegrey/80 bg-white/70 px-4 py-3 pr-12 text-body placeholder:text-body/40 focus:border-secondary focus:outline-none"
                placeholder="••••••••"
                bind:value={registerPassword}
                type="password"
                required
              />
            {/if}
            <button
              type="button"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-body/60 hover:text-body transition"
              onmousedown={() => (registerShowPassword = true)}
              onmouseup={() => (registerShowPassword = false)}
              onmouseleave={() => (registerShowPassword = false)}
              ontouchstart={() => (registerShowPassword = true)}
              ontouchend={() => (registerShowPassword = false)}
              aria-label="Show password while pressing"
            >
              {#if registerShowPassword}
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                </svg>
              {:else}
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              {/if}
            </button>
          </div>
        </label>

        <label class="block text-sm font-medium text-heading">
          Reason (optional)
          <textarea
            class="mt-2 w-full rounded-apple-lg border border-tablegrey/80 bg-white/70 px-4 py-3 text-body placeholder:text-body/40 focus:border-secondary focus:outline-none"
            placeholder="What do you need access for?"
            rows="3"
            bind:value={registerReason}
          ></textarea>
        </label>

        {#if registerError}
          <p class="rounded-apple-lg bg-error/10 px-4 py-3 text-sm text-error">{registerError}</p>
        {/if}

        <button
          class="w-full rounded-apple-lg px-4 py-3 text-sm font-semibold text-white transition bg-secondary hover:bg-secondary-hover"
          type="submit"
          disabled={registerLoading}
        >
          {registerLoading ? 'Sending…' : 'Send request'}
        </button>
      </form>
    </div>
  </div>
{/if}

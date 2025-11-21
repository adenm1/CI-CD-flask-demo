<script lang="ts">
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';
  import { login, register } from '$lib/api/auth';
  import { authStore } from '$lib/stores/auth';

  const auth = authStore;
  let username = '';
  let password = '';
  let showPassword = false;
  let error: string | null = null;
  let loading = false;
  let showRegisterModal = false;

  // Register form state
  let registerUsername = '';
  let registerPassword = '';
  let registerShowPassword = false;
  let registerError: string | null = null;
  let registerLoading = false;

  // Forgot password
  let showForgotPassword = false;
  const STORAGE_PASSWORD_KEY = 'ci_dashboard_password';

  function closeForgotPassword() {
    showForgotPassword = false;
  }

  function closeRegisterOverlay() {
    showRegisterModal = false;
  }

  function handleBackdropKey(event: KeyboardEvent, close: () => void) {
    if (event.key === 'Escape' || event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      close();
    }
  }

  function handleForgotPassword() {
    if (!browser) return;

    // Reset password to default
    localStorage.removeItem(STORAGE_PASSWORD_KEY);

    alert('Password has been reset to default: change-me-now\n\nYou can now login with:\nUsername: admin\nPassword: change-me-now');

    closeForgotPassword();
  }

  async function handleLogin() {
    loading = true;
    error = null;
    try {
      const response = await login({ username, password });
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
    try {
      const response = await register({ username: registerUsername, password: registerPassword });
      auth.login(response.token, response.admin);
      goto('/');
    } catch (err) {
      registerError = err instanceof Error ? err.message : 'Unable to register';
    } finally {
      registerLoading = false;
    }
  }
</script>

<div class="max-w-xl w-full space-y-8">
  <!-- Sign up link above card -->
  <div class="text-center text-sm text-body/70">
    Don't have an account?
    <button class="font-semibold text-primary hover:text-primary-hover transition" on:click={() => (showRegisterModal = true)}>
      Sign up
    </button>
  </div>

  <!-- Login Card -->
  <div class="rounded-apple-2xl border border-white/40 bg-card/80 p-10 shadow-soft backdrop-blur">
    <p class="text-sm uppercase tracking-[0.4em] text-body/50">SiYing Liu's Project</p>
    <h2 class="mt-3 text-3xl font-semibold text-heading">Welcome back</h2>
    <p class="text-body/60">Sign in to access your dashboard.</p>

    <form class="mt-8 space-y-4" on:submit|preventDefault={handleLogin}>
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
            on:mousedown={() => (showPassword = true)}
            on:mouseup={() => (showPassword = false)}
            on:mouseleave={() => (showPassword = false)}
            on:touchstart={() => (showPassword = true)}
            on:touchend={() => (showPassword = false)}
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

      <!-- Forgot Password Link -->
      <div class="text-center">
        <button
          type="button"
          class="text-sm text-body/60 hover:text-primary transition underline"
          on:click={() => (showForgotPassword = true)}
        >
          Forgot password?
        </button>
      </div>
    </form>
  </div>
</div>

<!-- Forgot Password Modal -->
{#if showForgotPassword}
  <!-- Backdrop -->
  <div
    class="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 transition-opacity"
    role="button"
    tabindex="0"
    aria-label="Close reset password modal"
    on:click={closeForgotPassword}
    on:keydown={(event) => handleBackdropKey(event, closeForgotPassword)}
  ></div>

  <!-- Modal -->
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <div class="max-w-md w-full rounded-apple-2xl border border-white/40 bg-card shadow-soft p-8 relative animate-in fade-in zoom-in duration-200">
      <!-- Close button -->
      <button
        class="absolute top-4 right-4 text-body/60 hover:text-body transition"
        on:click={closeForgotPassword}
        type="button"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <div class="text-center">
        <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-apple-lg bg-primary/10 mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8 text-primary">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
          </svg>
        </div>

        <h2 class="mt-3 text-2xl font-semibold text-heading">Reset Password</h2>
        <p class="mt-2 text-body/60">Reset your password to the default value.</p>

        <div class="mt-6 rounded-apple-lg bg-background/50 p-4 text-left">
          <p class="text-sm font-medium text-heading mb-2">Default credentials:</p>
          <div class="space-y-1 font-mono text-sm text-body/70">
            <p><span class="text-body/50">Username:</span> admin</p>
            <p><span class="text-body/50">Password:</span> change-me-now</p>
          </div>
        </div>

        <div class="mt-6 flex gap-3">
          <button
            class="flex-1 rounded-apple-lg px-4 py-3 text-sm font-semibold text-body/70 transition bg-background/50 hover:bg-background/80"
            on:click={closeForgotPassword}
          >
            Cancel
          </button>
          <button
            class="flex-1 rounded-apple-lg px-4 py-3 text-sm font-semibold text-white transition bg-primary hover:bg-primary-hover"
            on:click={handleForgotPassword}
          >
            Reset Password
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}

<!-- Registration Modal (Floating) -->
{#if showRegisterModal}
  <!-- Backdrop -->
  <div
    class="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 transition-opacity"
    role="button"
    tabindex="0"
    aria-label="Close registration modal"
    on:click={closeRegisterOverlay}
    on:keydown={(event) => handleBackdropKey(event, closeRegisterOverlay)}
  ></div>

  <!-- Modal -->
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <div class="max-w-md w-full rounded-apple-2xl border border-white/40 bg-card shadow-soft p-8 relative animate-in fade-in zoom-in duration-200">
      <!-- Close button -->
      <button
        class="absolute top-4 right-4 text-body/60 hover:text-body transition"
        on:click={closeRegisterOverlay}
        type="button"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <p class="text-sm uppercase tracking-[0.4em] text-body/50">SiYing Liu's Project</p>
      <h2 class="mt-3 text-2xl font-semibold text-heading">Create an account</h2>
      <p class="text-body/60">Join us to get started.</p>

      <form class="mt-6 space-y-4" on:submit|preventDefault={handleRegister}>
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
              on:mousedown={() => (registerShowPassword = true)}
              on:mouseup={() => (registerShowPassword = false)}
              on:mouseleave={() => (registerShowPassword = false)}
              on:touchstart={() => (registerShowPassword = true)}
              on:touchend={() => (registerShowPassword = false)}
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

        {#if registerError}
          <p class="rounded-apple-lg bg-error/10 px-4 py-3 text-sm text-error">{registerError}</p>
        {/if}

        <button
          class="w-full rounded-apple-lg px-4 py-3 text-sm font-semibold text-white transition bg-secondary hover:bg-secondary-hover"
          type="submit"
          disabled={registerLoading}
        >
          {registerLoading ? 'Processing…' : 'Sign up'}
        </button>
      </form>
    </div>
  </div>
{/if}

# Svelte 5 Migration Guide

**Date**: 2025-11-27
**From**: Svelte 4.2.12
**To**: Svelte 5.17.0

---

## What Changed

### Package Updates
```json
{
  "dependencies": {
    "svelte": "^5.17.0"  // was ^4.2.12
  },
  "devDependencies": {
    "@sveltejs/kit": "^2.15.3",  // was ^2.5.7
    "@sveltejs/vite-plugin-svelte": "^5.0.3",  // was ^3.1.1
    "@sveltejs/adapter-auto": "^3.3.1",  // was ^3.1.1
    "svelte-check": "^4.0.0",  // was ^3.6.4
    "vite": "^6.0.0",  // was ^5.2.8
    "vitest": "^2.0.0"  // was ^1.4.0
  }
}
```

---

## Svelte 5 Runes System

Svelte 5 introduces **runes** - a new way to declare reactivity that's more explicit and powerful.

### Migration Pattern

#### Before (Svelte 4)
```svelte
<script>
  let count = 0;
  let doubled = 0;

  $: doubled = count * 2;

  function increment() {
    count += 1;
  }
</script>
```

#### After (Svelte 5)
```svelte
<script>
  let count = $state(0);
  let doubled = $derived(count * 2);

  function increment() {
    count += 1;
  }
</script>
```

---

## Key Runes

### `$state()` - Reactive State
Replaces: `let` for reactive variables

```svelte
<script>
  let count = $state(0);
  let user = $state({ name: 'Alice', age: 30 });
</script>
```

### `$derived()` - Computed Values
Replaces: `$:` reactive statements

```svelte
<script>
  let count = $state(0);
  let doubled = $derived(count * 2);
  let isEven = $derived(count % 2 === 0);
</script>
```

### `$effect()` - Side Effects
Replaces: `$:` for side effects, `onMount`, etc.

```svelte
<script>
  let count = $state(0);

  $effect(() => {
    console.log(`Count is now ${count}`);

    // Cleanup function
    return () => {
      console.log('Cleaning up');
    };
  });
</script>
```

### `$props()` - Component Props
Replaces: `export let`

```svelte
<script>
  let { title, count = 0, onClick } = $props();
</script>

<h1>{title}</h1>
<button onclick={onClick}>{count}</button>
```

---

## Store Usage (Unchanged)

Svelte stores work the same way in Svelte 5:

```svelte
<script>
  import { pipelinesStore } from '$lib/stores/pipelines';

  // Still use $ prefix for store auto-subscription
  $: pipelines = $pipelinesStore.pipelines;
  // Or
  const store = pipelinesStore;
  $: pipelines = $store.pipelines;
</script>
```

---

## Component Migration Examples

### Simple Counter Component

**Before (Svelte 4)**:
```svelte
<script>
  export let initial = 0;
  let count = initial;
  let doubled;

  $: doubled = count * 2;
</script>

<button on:click={() => count++}>
  Count: {count}, Doubled: {doubled}
</button>
```

**After (Svelte 5)**:
```svelte
<script>
  let { initial = 0 } = $props();
  let count = $state(initial);
  let doubled = $derived(count * 2);
</script>

<button onclick={() => count++}>
  Count: {count}, Doubled: {doubled}
</button>
```

### Component with Effects

**Before (Svelte 4)**:
```svelte
<script>
  import { onMount } from 'svelte';

  export let userId;
  let user;

  $: loadUser(userId);

  async function loadUser(id) {
    user = await fetch(`/api/users/${id}`).then(r => r.json());
  }

  onMount(() => {
    console.log('Mounted');
    return () => console.log('Unmounted');
  });
</script>
```

**After (Svelte 5)**:
```svelte
<script>
  let { userId } = $props();
  let user = $state(null);

  $effect(() => {
    async function loadUser() {
      user = await fetch(`/api/users/${userId}`).then(r => r.json());
    }
    loadUser();
  });

  $effect(() => {
    console.log('Mounted');
    return () => console.log('Unmounted');
  });
</script>
```

---

## Event Handling Changes

### Before (Svelte 4)
```svelte
<button on:click={handleClick}>Click me</button>
<input on:input={handleInput} />
```

### After (Svelte 5)
```svelte
<button onclick={handleClick}>Click me</button>
<input oninput={handleInput} />
```

**Note**: Lowercase event names (onclick, oninput, etc.)

---

## Our Project Components

### Compatibility Status

✅ **Already Compatible** (no changes needed):
- Store files (`pipelines.ts`, `auth.ts`)
- API client files
- Most layout components

⚠️ **May Need Updates**:
- Components using `export let` → migrate to `$props()`
- Components using `$:` → migrate to `$derived()` or `$effect()`
- Components using `on:event` → change to `onevent`

---

## Migration Strategy

Our components are mostly simple and use stores, so migration is minimal:

1. **Stores remain unchanged** - `pipelinesStore`, `authStore` work as-is
2. **Template syntax mostly unchanged** - `{variable}`, `{#if}`, `{#each}` still work
3. **Main changes**:
   - Event handlers: `on:click` → `onclick`
   - If components use `export let`, migrate to `$props()`
   - If using `$:` for derived values, can migrate to `$derived()` (optional for now)

---

## Benefits of Svelte 5

1. **Better Performance**: Fine-grained reactivity, smaller bundle sizes
2. **Clearer Intent**: `$state()` is explicit about what's reactive
3. **Better TypeScript**: Improved type inference
4. **Easier to Reason**: Explicit dependencies in `$derived()` and `$effect()`
5. **Smaller Runtime**: ~30% smaller than Svelte 4

---

## Testing

### Before Testing
```bash
cd frontend
npm install  # Install Svelte 5 dependencies
```

### Run Tests
```bash
npm run check  # TypeScript and Svelte checks
npm run build  # Production build
npm run dev    # Development server
```

---

## Rollback Plan

If issues arise, rollback is simple:

```bash
cd frontend
git checkout package.json
npm install
```

---

## Resources

- [Svelte 5 Release Notes](https://svelte.dev/blog/svelte-5-release)
- [Svelte 5 Migration Guide](https://svelte.dev/docs/svelte/v5-migration-guide)
- [Runes Documentation](https://svelte.dev/docs/svelte/runes)

---

## Status

- ✅ Package.json updated
- ✅ svelte.config.js updated (runes enabled)
- ✅ Vite and SvelteKit updated
- ⏳ Components are mostly compatible (stores-based, minimal changes needed)
- ⏳ Testing pending after `npm install`

---

**Note**: Our application uses stores for state management, which are fully compatible with Svelte 5. Most components should work without changes. The main update needed is changing `on:event` to `onevent`.

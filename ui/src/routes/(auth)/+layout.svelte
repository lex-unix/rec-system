<script lang="ts">
  import { goto } from '$app/navigation';
  import { user } from '$lib/stores';
  import { onMount } from 'svelte';

  onMount(() => {
    $user && goto('/issues');
  });
</script>

<main class="flex items-center justify-center py-32">
  <div class="flex w-full max-w-sm flex-col gap-2 px-5">
    <slot />
  </div>
</main>

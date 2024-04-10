<script lang="ts">
  import '../app.css';
  import { Toaster } from '$components';
  import type { User } from '$lib/types';
  import { user } from '$lib/stores';
  import { onMount } from 'svelte';

  let show = false;

  onMount(async () => {
    const response = await fetch('http://localhost:8000/users/me', {
      credentials: 'include'
    });
    if (response.ok) {
      const json: User = await response.json();
      $user = json;
    }
    show = true;
  });
</script>

{#if show}
  <slot />
{/if}

<Toaster />

<style>
  :global(.no-scrollbar::-webkit-scrollbar) {
    display: none;
  }

  :gloabl(.no-scrollbar) {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
</style>

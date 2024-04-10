<script lang="ts">
  import { goto } from '$app/navigation';
  import { user } from '$lib/stores';
  import { onMount } from 'svelte';

  let show = false;
  onMount(() => {
    !$user && goto('/login');
    show = true;
  });
</script>

{#if show}
  <slot />
{/if}

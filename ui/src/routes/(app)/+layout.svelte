<script lang="ts">
  import { goto } from '$app/navigation';
  import { user } from '$lib/stores';
  import { onMount } from 'svelte';

  onMount(() => {
    !$user && goto('/login');
  });
</script>

<slot />

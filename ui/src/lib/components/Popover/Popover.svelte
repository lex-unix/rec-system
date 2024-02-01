<script context="module" lang="ts">
  export type Size = 'sm' | 'md' | 'lg';
</script>

<script lang="ts">
  import { setContext } from 'svelte';
  import { createPopover } from '@melt-ui/svelte';

  const ctx = createPopover({ forceVisible: true });
  setContext('popover', ctx);
</script>

<slot />

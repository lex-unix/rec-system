<script lang="ts">
  import { createDialog } from '@melt-ui/svelte';
  import { setContext } from 'svelte';

  export function show() {
    $open = true;
  }

  export function dismiss() {
    $open = false;
  }

  const ctx = createDialog({
    forceVisible: true
  });

  setContext('drawer', ctx);

  const {
    states: { open }
  } = ctx;
</script>

<slot />

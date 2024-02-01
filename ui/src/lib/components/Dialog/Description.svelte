<script lang="ts">
  import { getContext } from 'svelte';
  import { type Dialog, melt } from '@melt-ui/svelte';

  const {
    elements: { description }
  } = getContext<Dialog>('dialog');
</script>

<p use:melt={$description} class="text-navy-400">
  <slot />
</p>

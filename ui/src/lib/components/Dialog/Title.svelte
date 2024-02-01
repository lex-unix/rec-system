<script lang="ts">
  import { getContext } from 'svelte';
  import { type Dialog, melt } from '@melt-ui/svelte';

  const {
    elements: { title }
  } = getContext<Dialog>('dialog');
</script>

<h2 use:melt={$title} class="text-lg font-semibold text-navy-100 md:text-xl">
  <slot />
</h2>

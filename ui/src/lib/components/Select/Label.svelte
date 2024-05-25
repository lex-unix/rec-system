<script lang="ts">
  import { getContext } from 'svelte';
  import { type Select, melt } from '@melt-ui/svelte';
  import { cn } from '$lib';

  let className = '';
  export { className as class };

  const {
    elements: { label }
  } = getContext<Select>('select');
</script>

<label use:melt={$label} class={cn('mb-2 block text-navy-400', className)}>
  <slot />
</label>

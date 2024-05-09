<script lang="ts">
  import { cn } from '$lib/cn';
  import { getContext } from 'svelte';

  let className: string = '';
  export { className as class };

  const id = getContext<string>('id');
</script>

<label for={id} id="{id}-label" class={cn('text-navy-300', className)}>
  <slot />
</label>

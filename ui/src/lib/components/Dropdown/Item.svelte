<script lang="ts">
  import { createEventDispatcher, getContext } from 'svelte';
  import { type DropdownMenu, melt } from '@melt-ui/svelte';
  import { cn } from '$lib';

  let className: string = '';
  export { className as class };

  const dispatch = createEventDispatcher();

  function select() {
    dispatch('select');
  }

  const {
    elements: { item }
  } = getContext<DropdownMenu>('dropdown');
</script>

<button
  use:melt={$item}
  on:click={select}
  class={cn(
    'flex min-h-7 items-center rounded px-2 py-2 opacity-70 focus:outline-none data-[highlighted]:bg-navy-800 data-[highlighted]:opacity-100',
    className
  )}
>
  <slot />
</button>

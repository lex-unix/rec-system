<script lang="ts">
  import { cn } from '$lib';
  import { createEventDispatcher } from 'svelte';
  import type { Icon as LucideIcon } from 'lucide-svelte';
  import type { ComponentType } from 'svelte';

  type Icon = ComponentType<LucideIcon>;

  export let leftIcon: Icon | undefined = undefined;
  export let rightIcon: Icon | undefined = undefined;
  export let type: 'button' | 'submit' | 'reset' = 'button';
  let className: string = '';
  export { className as class };

  const dispatch = createEventDispatcher();

  function click() {
    dispatch('click');
  }
</script>

<button
  {type}
  on:click={click}
  class={cn(
    'flex items-center gap-2 rounded-md border border-navy-200/10 bg-navy-800 px-4 py-3 font-medium leading-none opacity-70 transition hover:opacity-100 focus:outline-none focus-visible:opacity-100 focus-visible:ring-2 focus-visible:ring-[#479EFA]',
    className
  )}
>
  <svelte:component this={leftIcon} class="square-4" />
  <span>
    <slot />
  </span>
  <svelte:component this={rightIcon} class="square-4" />
</button>

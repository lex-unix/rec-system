<script lang="ts">
  import { getContext } from 'svelte';
  import { type Dialog, melt } from '@melt-ui/svelte';
  import { cn } from '$lib';
  import { fly } from 'svelte/transition';

  let className = '';
  export { className as class };

  const {
    elements: { overlay, content, portalled },
    states: { open }
  } = getContext<Dialog>('drawer');
</script>

{#if $open}
  <div use:melt={$portalled}>
    <div use:melt={$overlay} class="fixed inset-0 z-40 bg-black/10" />
    <div
      use:melt={$content}
      transition:fly={{
        x: -350,
        duration: 250,
        opacity: 1
      }}
      class={cn(
        'fixed left-0 top-0 z-40 h-screen w-full max-w-[350px] bg-navy-900 p-6',
        className
      )}
    >
      <slot />
    </div>
  </div>
{/if}

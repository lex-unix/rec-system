<script lang="ts">
  import { getContext } from 'svelte';
  import { type Dialog, melt } from '@melt-ui/svelte';
  import { cn } from '$lib';
  import { XIcon } from 'lucide-svelte';

  let className = '';
  export { className as class };

  const {
    elements: { close }
  } = getContext<Dialog>('drawer');
</script>

<button
  use:melt={$close}
  class={cn(
    'absolute inline-flex items-center justify-center rounded-full p-1.5 text-navy-400 hover:bg-navy-800 hover:text-navy-300 focus:outline-none focus:ring-2 focus:ring-navy-700',
    className
  )}
  aria-label="Close"
>
  <XIcon class="square-4" />
</button>

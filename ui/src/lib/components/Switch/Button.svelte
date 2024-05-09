<script lang="ts">
  import { getContext } from 'svelte';
  import { melt, type Switch } from '@melt-ui/svelte';
  import { cn } from '$lib/cn';

  let className: string = '';
  export { className as class };

  const {
    elements: { root, input }
  } = getContext<Switch>('switch');
  const id = getContext<string>('id');
</script>

<button
  {id}
  use:melt={$root}
  class={cn(
    'relative h-6 rounded-full border border-navy-200/20 bg-navy-700 transition-colors data-[state=checked]:bg-green-400',
    className
  )}
  aria-labelledby="{id}-label"
>
  <span class="thumb block rounded-full bg-white transition" />
</button>
<input use:melt={$input} />

<style>
  button {
    --w: 2.75rem;
    --padding: 0.125rem;
    width: var(--w);
  }

  .thumb {
    --size: 1.25rem;
    width: var(--size);
    height: var(--size);
    transform: translateX(var(--padding));
  }

  :global([data-state='checked']) .thumb {
    transform: translateX(calc(var(--w) - var(--size) - var(--padding)));
  }
</style>

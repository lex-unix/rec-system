<script lang="ts">
  import { formatTime } from '$lib';

  export let me: boolean;
  export let date: Date;

  function scrollToLast(node: HTMLElement) {
    const parent = node.parentNode;
    if (!parent) return;

    const parenetChildren = parent.children;
    if (!parenetChildren) return;

    const isLast =
      Array.from(parenetChildren).indexOf(node) === parenetChildren.length - 1;
    if (isLast) {
      node.scrollIntoView({ behavior: 'smooth' });
    }
  }
</script>

<div
  use:scrollToLast
  class="flex min-w-0 max-w-[58%] flex-col justify-center {me
    ? 'self-end'
    : 'self-start'}"
>
  <span class="rounded-md border border-navy-200/10 bg-navy-800 p-2">
    <slot />
  </span>
  <div class="pt-1 text-xs text-gray-400 {me ? 'pr-0.5 text-right' : 'pl-0.5'}">
    {formatTime(date)}
  </div>
</div>

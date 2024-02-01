<script lang="ts">
  import { cn } from '$lib';
  import type { HTMLInputTypeAttribute } from 'svelte/elements';

  export let value: string = '';
  export let placeholder: string | undefined = undefined;
  export let required: boolean = false;
  export let id: string;
  export let name: string;
  export let type: HTMLInputTypeAttribute = 'text';
  let className = '';
  export { className as class };

  function change(
    e: Event & { currentTarget: EventTarget & HTMLInputElement }
  ) {
    value = e.currentTarget.value;
  }
</script>

<input
  {id}
  {name}
  {type}
  {value}
  {required}
  {placeholder}
  autocomplete="off"
  spellcheck="false"
  class={cn(
    'h-10 w-full max-w-[420px] rounded-md border border-navy-200/10 bg-navy-800 px-3 py-2 text-navy-50 placeholder:text-navy-500 hover:border-navy-200/25 focus:border-navy-200/25 focus:outline-none focus:ring-2 focus:ring-navy-600',
    className
  )}
  on:input={change}
/>

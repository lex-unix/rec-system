<script lang="ts">
  import { SearchIcon } from 'lucide-svelte';
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  function search(
    e: Event & { currentTarget: EventTarget & HTMLInputElement }
  ) {
    const input = e.target as HTMLInputElement;
    dispatch('search', { search: input.value });
  }
</script>

<div
  class="relative h-10 w-full rounded-md border border-navy-200/10 focus-within:border-navy-200/25"
>
  <div class="absolute left-3 top-1/2 -translate-y-1/2">
    <SearchIcon class="text-navy-400 square-4" />
  </div>
  <input
    type="search"
    class="h-full w-full bg-transparent pl-10 placeholder:text-navy-400 focus:outline-none"
    placeholder="Пошук..."
    on:input={search}
  />
</div>

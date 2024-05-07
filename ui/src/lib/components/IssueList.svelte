<script lang="ts">
  import { page } from '$app/stores';
  import { createEventDispatcher } from 'svelte';
  import type { Issue } from '$lib/types';
  import { issueType } from '$lib/issues';

  export let issues: Issue[];

  const dispatch = createEventDispatcher();

  function select() {
    dispatch('select');
  }
</script>

<ul class="list-none space-y-1 pb-4 pt-4">
  {#each issues as { id, type, description }}
    <li>
      <a
        on:click={select}
        href="/issues/{id}"
        class="line-clamp-1 block w-full rounded-md px-5 py-3 hover:bg-navy-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-[#479EFA]"
        class:active={$page.params.id
          ? parseInt($page.params.id) === id
          : false}
      >
        <div class="flex items-center justify-between">
          <p class="capitalize">
            {issueType[type]}
          </p>
        </div>
        <p class="line-clamp-1 text-navy-400">{description}</p>
      </a>
    </li>
  {/each}
</ul>

<style lang="postcss">
  .active {
    background: theme(colors.navy.800);
  }
</style>
